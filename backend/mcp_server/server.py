# backend/mcp_server/server.py
"""
基于 MCP 协议的独立工具服务器。

通过 stdio 传输暴露以下工具（Function Calling 风格）：
  - get_constitution_recommendations: 知识图谱体质推荐
  - search_symptoms: 症状全文检索
  - get_acupoint_prescription: 穴位处方
  - retrieve_similar_cases: RAG 相似证型案例召回
  - get_assessment_scores: 根据测评 ID 查询问卷得分、主次体质与判定说明
  - get_conditioning_plan: 获取与问卷辨识报告一致的专属调理方案（6大类/AI增强推荐优先）

启动方式：
  python backend/mcp_server/server.py

Flask 后端通过 MCPClient 以子进程方式拉起本服务并调用工具。
依赖：从环境变量读取 NEO4J_* 配置；RAG 数据目录默认为 data/rag。

性能注意：
  为了让子进程尽快响应 initialize / tools/list 握手（避免客户端 30/60s 超时），
  py2neo / torch / sentence-transformers 等重型依赖一律在首次工具调用时才 import
  并加载（lazy init），不在模块 import 阶段加载。

编码注意（Windows 必看）：
  MCP 协议要求 stdio 为 UTF-8，但 Windows 控制台默认是 GBK/CP936。
  若不强制 UTF-8，中文日志会让客户端读取 stdout 时触发 UnicodeDecodeError，
  进而导致客户端 cancel scope 异常、CancelledError、握手失败。
  所以本文件在任何 import 之前就把 stdout/stderr reconfigure 为 UTF-8，
  并在 mcp_client 一侧设置 PYTHONIOENCODING=utf-8 做双重保险。
"""
import json
import os
import sys
from typing import Optional

# 在任何 import / 打印之前强制 UTF-8。放在最顶部（紧跟 import sys 之后）。
# Python 3.7+ 支持 reconfigure(encoding=...)。
for _stream_name in ('stdout', 'stderr'):
    _stream = getattr(sys, _stream_name, None)
    if _stream is not None and callable(getattr(_stream, 'reconfigure', None)):
        try:
            _stream.reconfigure(encoding='utf-8')
        except Exception:  # pragma: no cover - 平台差异兜底
            pass

import logging

# 让本进程能 import backend.app.*
_BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _BACKEND_DIR not in sys.path:
    sys.path.insert(0, _BACKEND_DIR)

from mcp.server.fastmcp import FastMCP

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [MCP-SERVER] %(name)s %(levelname)s %(message)s',
                    # 日志走 stderr（MCP JSON-RPC 帧走 stdout，互不干扰）
                    stream=sys.stderr)
logger = logging.getLogger(__name__)

# 依赖（全部 lazy init）
_graph = None
_kg_retriever = None
_case_retriever = None
_Config = None  # noqa: N816


def _get_config():
    """延迟读取 app.config.Config（import 路径较重）。"""
    global _Config
    if _Config is None:
        from app.config import Config as _Cfg  # noqa: N811
        _Config = _Cfg
    return _Config


def _get_graph():
    global _graph
    if _graph is None:
        from py2neo import Graph
        cfg = _get_config()
        _graph = Graph(cfg.NEO4J_URI, auth=(cfg.NEO4J_USER, cfg.NEO4J_PASSWORD))
        logger.info("MCP Server 已连接 Neo4j")
    return _graph


def _get_kg_retriever():
    global _kg_retriever
    if _kg_retriever is None:
        from app.services.rag_service import KGRetriever
        _kg_retriever = KGRetriever(_get_graph())
    return _kg_retriever


def _get_case_retriever():
    global _case_retriever
    if _case_retriever is None:
        from app.services.rag.case_retriever import CaseRetriever
        _case_retriever = CaseRetriever()
        _case_retriever.load()
    return _case_retriever


mcp = FastMCP("tcm-kg-server")


@mcp.tool()
def get_constitution_recommendations(constitution: Optional[str] = None) -> dict:
    """根据体质代码(如 qixu/yangxu/tanshi)从知识图谱查询推荐方案，包含穴位、食材、运动、疗法、注意事项。"""
    constitution = (constitution or '').strip()
    if not constitution:
        return {'error': 'constitution 必填（如 qixu/yangxu/tanshi）'}
    return _get_kg_retriever().get_recommendations(constitution)


@mcp.tool()
def search_symptoms(query: Optional[str] = None) -> list:
    """在知识图谱中全文检索症状节点，辅助症状定位。"""
    query = (query or '').strip()
    if not query:
        return []
    return _get_kg_retriever().search_symptoms(query, limit=5)


@mcp.tool()
def get_acupoint_prescription(constitution: Optional[str] = None) -> dict:
    """根据体质代码生成穴位处方，返回穴位名称、定位、操作方法。"""
    constitution = (constitution or '').strip()
    if not constitution:
        return {'error': 'constitution 必填（如 qixu/yangxu/tanshi）'}
    recs = _get_kg_retriever().get_recommendations(constitution)
    acupoints = recs.get('acupoints', [])
    return {
        'constitution': constitution,
        'acupoints': acupoints,
        'summary': f"针对 {constitution} 体质推荐 {len(acupoints)} 个穴位",
    }


@mcp.tool()
def retrieve_similar_cases(symptoms: Optional[list] = None,
                           tongue: Optional[str] = None,
                           pulse: Optional[str] = None) -> list:
    """基于症状、舌象、脉象文本特征，通过向量召回检索相似证型案例。

    参数容错：小模型 Function Calling 常把未采集的舌/脉传成 null，
    FastMCP 按签名生成 pydantic 校验，非 Optional 的 str 不接受 None，
    会把校验错误当普通文本返回（调用方误判为"调用成功"）。
    这里显式声明 Optional 并在函数内归一化，保证 null 也能正常检索。
    """
    if not isinstance(symptoms, list):
        symptoms = []
    tongue = (tongue or "").strip()
    pulse = (pulse or "").strip()
    symptoms_text = "；".join(str(s) for s in symptoms if str(s).strip())
    return _get_case_retriever().retrieve(symptoms_text, tongue=tongue, pulse=pulse)


# ---------- 体质代码 -> 中文名映射（MCP 工具内共享，不依赖 backend.app 避免循环 import）----------

_MCP_NAMES_MAP = {
    'pinghe': '平和质',
    'qixu': '气虚质',
    'yangxu': '阳虚质',
    'yinxu': '阴虚质',
    'tanshi': '痰湿质',
    'shire': '湿热质',
    'xueyu': '血瘀质',
    'qiyu': '气郁质',
    'tebing': '特禀质',
}


def _mcp_build_reason(primary, secondary, scores, names_map=None):
    """MCP 内联版 build_assessment_reason，逻辑与 constitution.py 保持一致。"""
    if names_map is None:
        names_map = _MCP_NAMES_MAP
    scores = scores or {}
    pinghe = float(scores.get('pinghe', 0) or 0)
    others = {k: float(v or 0) for k, v in scores.items() if k != 'pinghe'}
    biased_yes = [k for k, v in others.items() if v >= 40]
    biased_tend = [k for k, v in others.items() if 30 <= v < 40]

    def _fmt(keys):
        return "、".join(f"{names_map.get(k, k)}={others.get(k, scores.get(k, 0))}" for k in keys)

    if pinghe >= 60 and all(v < 30 for v in others.values()):
        return f"平和质得分 {pinghe}≥60，其余体质均<30，判为平和质（标准）"
    if pinghe >= 60 and all(v < 40 for v in others.values()) and biased_tend:
        return (f"平和质={pinghe}≥60 且其余体质均<40，其中 {_fmt(biased_tend)} "
                f"归入 30≤score<40 倾向类作为兼夹倾向")
    if biased_yes:
        primary_name = names_map.get(primary, primary)
        yes_str = _fmt(biased_yes)
        secondary_raw = secondary or []
        secondary_names = [names_map.get(s, s) for s in secondary_raw if s]
        sec_clause = ""
        sec_clean = [n for n in secondary_names if n != primary_name]
        if sec_clean:
            sec_clause = f"，{'、'.join(sec_clean)}为兼夹"
        extra_tend = [t for t in biased_tend if t not in biased_yes]
        tend_extra = f"；另 {_fmt(extra_tend)} 为 30≤score<40 的倾向项" if extra_tend else ""
        return f"平和质 {pinghe}<60；{yes_str} 均≥40，判为 {primary_name} 为主{sec_clause}{tend_extra}"
    if biased_tend:
        primary_name = names_map.get(primary, primary)
        sec_names = [names_map.get(s, s) for s in (secondary or []) if s and s != primary]
        sec_clause = f"，{'、'.join(sec_names)}为兼夹倾向" if sec_names else ""
        return f"平和质 {pinghe}<60；{_fmt(biased_tend)} 均为 30≤score<40，判为 {primary_name} 为主{sec_clause}"
    if pinghe >= 60:
        return f"平和质得分 {pinghe}≥60，其余体质均<30，判为平和质（标准）"
    return f"平和质 {pinghe}<60，且其余体质均<30，综合判为 {names_map.get(primary, primary)}（接近正常范围）"


@mcp.tool()
def get_assessment_scores(assessment_id: Optional[int] = None) -> dict:
    """
    根据王琦量表问卷测评 ID 查询得分详情与体质判定说明。

    参数:
      assessment_id: 测评结果主键（整数）

    返回:
      { assessment_id, primary, primary_name, secondary, secondary_names, scores:{ctype:float}, reason:str }
      若测评不存在返回 { error: 'assessment not found' }。
    """
    if assessment_id is None:
        return {'error': 'assessment_id 必填'}
    # 用 raw pymysql 连接 DB（避免 import backend.app 造成循环依赖）
    import pymysql  # lazy import
    db_user = os.environ.get('DB_USER', 'root')
    db_password = os.environ.get('DB_PASSWORD', '123456')
    db_host = os.environ.get('DB_HOST', 'localhost')
    try:
        db_port = int(os.environ.get('DB_PORT', '3306'))
    except (TypeError, ValueError):
        db_port = 3306
    db_name = os.environ.get('DB_NAME', 'tcm_kg')

    conn = None
    try:
        conn = pymysql.connect(
            host=db_host, port=db_port, user=db_user,
            password=db_password, database=db_name,
            charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor,
        )
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, primary_type, secondary_types, scores "
                "FROM assessment_results WHERE id = %s LIMIT 1",
                (int(assessment_id),)
            )
            row = cur.fetchone()
        if not row:
            return {'error': 'assessment not found'}

        # 解析字段（secondary_types / scores 存 JSON 文本或 NULL）
        primary = row.get('primary_type') or 'pinghe'
        sec_raw = row.get('secondary_types')
        if isinstance(sec_raw, str) and sec_raw.strip():
            try:
                secondary = json.loads(sec_raw)
                if not isinstance(secondary, list):
                    secondary = []
            except (TypeError, ValueError, json.JSONDecodeError):
                secondary = []
        elif isinstance(sec_raw, list):
            secondary = sec_raw
        else:
            secondary = []

        scores_raw = row.get('scores')
        if isinstance(scores_raw, str) and scores_raw.strip():
            try:
                scores = json.loads(scores_raw)
                if not isinstance(scores, dict):
                    scores = {}
            except (TypeError, ValueError, json.JSONDecodeError):
                scores = {}
        elif isinstance(scores_raw, dict):
            scores = scores_raw
        else:
            scores = {}

        # 确保 scores 值为 float
        scores = {k: float(v) for k, v in scores.items()}

        primary_name = _MCP_NAMES_MAP.get(primary, primary)
        secondary_names = [_MCP_NAMES_MAP.get(s, s) for s in secondary]
        reason = _mcp_build_reason(primary, secondary, scores, _MCP_NAMES_MAP)

        return {
            'assessment_id': int(row.get('id') or assessment_id),
            'primary': primary,
            'primary_name': primary_name,
            'secondary': secondary,
            'secondary_names': secondary_names,
            'scores': scores,
            'reason': reason,
        }
    except Exception as e:
        logger.warning(f"MCP get_assessment_scores 查询失败: {e}")
        return {'error': f'assessment query failed: {e}'}
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception:
                pass


@mcp.tool()
def get_conditioning_plan(constitution: Optional[str] = None,
                          assessment_id: Optional[int] = None) -> dict:
    """
    获取与问卷辨识报告页面【口径一致】的专属调理方案 6 大类
    （穴位 / 食疗 / 运动 / 疗法过程 / 养生知识 / 注意事项）。

    参数（二选一，优先 assessment_id）：
      - assessment_id: int   问卷测评主键。命中时直接读取 assessment_results.enhanced_recommendations
                             （AI 增强版，与 Result.vue 页面显示完全相同）；若未增强则回退 Neo4j 基础推荐。
      - constitution:  str   体质代码（qixu/yangxu/...）。未提供 assessment_id 时必填，
                             直接从 Neo4j 知识图谱 / 静态底库取基础推荐。

    返回：
      { source, primary, primary_name, secondary, secondary_names, scores,
        acupoints[], foods[], exercises[], therapy_process[],
        health_knowledge[], precautions[], error? }
    """
    # 优先：assessment_id -> 读 MySQL enhanced_recommendations（和前端 Result 页一致）
    if assessment_id is not None:
        import pymysql  # lazy
        db_user = os.environ.get('DB_USER', 'root')
        db_password = os.environ.get('DB_PASSWORD', '123456')
        db_host = os.environ.get('DB_HOST', 'localhost')
        try:
            db_port = int(os.environ.get('DB_PORT', '3306'))
        except (TypeError, ValueError):
            db_port = 3306
        db_name = os.environ.get('DB_NAME', 'tcm_kg')

        conn = None
        try:
            conn = pymysql.connect(
                host=db_host, port=db_port, user=db_user,
                password=db_password, database=db_name,
                charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor,
            )
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id, primary_type, secondary_types, scores, enhanced_recommendations "
                    "FROM assessment_results WHERE id = %s LIMIT 1",
                    (int(assessment_id),)
                )
                row = cur.fetchone()
            if row:
                def _load_json(raw, default):
                    if isinstance(raw, (dict, list)):
                        return raw
                    if isinstance(raw, str) and raw.strip():
                        try:
                            return json.loads(raw)
                        except (TypeError, ValueError, json.JSONDecodeError):
                            return default
                    return default

                primary = row.get('primary_type') or 'pinghe'
                secondary = _load_json(row.get('secondary_types'), [])
                if not isinstance(secondary, list):
                    secondary = []
                scores = _load_json(row.get('scores'), {})
                if not isinstance(scores, dict):
                    scores = {}
                scores = {k: float(v) for k, v in scores.items()}
                enh = _load_json(row.get('enhanced_recommendations'), None)
                primary_name = _MCP_NAMES_MAP.get(primary, primary)
                secondary_names = [_MCP_NAMES_MAP.get(s, s) for s in secondary if s]

                def _nonempty_enh(e):
                    return (isinstance(e, dict) and any(
                        isinstance(e.get(k), list) and len(e[k])
                        for k in ('acupoints', 'foods', 'exercises', 'therapy_process', 'health_knowledge', 'precautions')
                    ))

                if _nonempty_enh(enh):
                    return {
                        'source': 'assessment_enhanced_recommendations',
                        'assessment_id': int(row.get('id') or assessment_id),
                        'primary': primary,
                        'primary_name': primary_name,
                        'secondary': secondary,
                        'secondary_names': secondary_names,
                        'scores': scores,
                        'acupoints': enh.get('acupoints', []),
                        'foods': enh.get('foods', []),
                        'exercises': enh.get('exercises', []),
                        'therapy_process': enh.get('therapy_process', []),
                        'health_knowledge': enh.get('health_knowledge', []),
                        'precautions': enh.get('precautions', []),
                    }
                # 没有 AI 增强：fallback 主体质基础推荐
                kg = _get_kg_retriever().get_recommendations(primary) or {}
                return {
                    'source': 'assessment_fallback_' + ('neo4j' if any(kg.get(k) for k in ('acupoints', 'foods', 'exercises')) else 'static'),
                    'assessment_id': int(row.get('id') or assessment_id),
                    'primary': primary,
                    'primary_name': primary_name,
                    'secondary': secondary,
                    'secondary_names': secondary_names,
                    'scores': scores,
                    'acupoints': kg.get('acupoints', []),
                    'foods': kg.get('foods', []),
                    'exercises': kg.get('exercises', []),
                    'therapy_process': kg.get('therapy_process', []),
                    'health_knowledge': kg.get('health_knowledge', []),
                    'precautions': kg.get('precautions', []),
                }
        except Exception as e:
            logger.warning(f"MCP get_conditioning_plan(id={assessment_id}) 查询失败: {e}")
            # 失败不直接返回错误：若用户提供了 constitution 继续走下方体质路径
            if not constitution:
                return {'error': f'assessment query failed: {e}'}
        finally:
            if conn is not None:
                try:
                    conn.close()
                except Exception:
                    pass

    # 路径 B：仅指定体质代码（或上面失败且 constitution 有值）→ 知识图谱基础推荐
    if constitution:
        recs = _get_kg_retriever().get_recommendations(constitution) or {}
        source_tag = 'neo4j' if any(recs.get(k) for k in ('acupoints', 'foods', 'exercises')) else 'static'
        return {
            'source': source_tag,
            'primary': constitution,
            'primary_name': _MCP_NAMES_MAP.get(constitution, constitution),
            'secondary': [],
            'secondary_names': [],
            'scores': {},
            'acupoints': recs.get('acupoints', []),
            'foods': recs.get('foods', []),
            'exercises': recs.get('exercises', []),
            'therapy_process': recs.get('therapy_process', []),
            'health_knowledge': recs.get('health_knowledge', []),
            'precautions': recs.get('precautions', []),
        }

    return {'error': '必须提供 constitution 或 assessment_id 至少一个参数'}


if __name__ == "__main__":
    logger.info("MCP Server 启动中(stdio)...")
    try:
        mcp.run()
    except KeyboardInterrupt:
        # Ctrl+C / Werkzeug reloader 重启 / 父进程退出 → 正常终止。
        # 不输出 traceback，避免在用户终端里显得"报错了"。
        logger.info("MCP Server 已退出 (Ctrl+C / 父进程退出)")
    except SystemExit:
        logger.info("MCP Server 已退出 (SystemExit)")
    except Exception as _e:
        # 任何其它异常：记录但避免被 anyio/fastmcp 再次包一层 CancelledError。
        # asyncio.CancelledError 在 Python 3.8+ 是 BaseException，这里不会被 except Exception 捕获；
        # 它的出现只意味着"管道关了 / 父进程不再消费响应"，属于正常生命周期末尾。
        logger.warning(f"MCP Server 异常退出: {type(_e).__name__}: {_e}")
    except BaseException as _be:  # noqa: BLE001 - 兜底 CancelledError 等 Base
        # CancelledError / GeneratorExit 等：属于 stdio 父管道 EOF 引发的正常取消。
        logger.info(f"MCP Server 已退出 ({type(_be).__name__})")
