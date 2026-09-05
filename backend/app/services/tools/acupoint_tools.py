# backend/app/services/tools/acupoint_tools.py
"""穴位处方工具：基于体质生成穴位处方。"""
import logging

from .registry import get_registry
from ..rag_service import KGRetriever

logger = logging.getLogger(__name__)


def register_acupoint_tools(registry):
    """注册穴位处方相关工具。"""

    def get_acupoint_prescription(constitution: str) -> dict:
        """
        根据体质生成穴位处方，返回穴位列表与操作方法。

        参数:
          constitution: 体质代码
        """
        if not constitution:
            return {"error": "constitution 不能为空"}
        graph = registry.graph
        if graph is None:
            raise RuntimeError("Neo4j 图谱连接未注入")

        retriever = KGRetriever(graph)
        recs = retriever.get_recommendations(constitution)
        acupoints = recs.get('acupoints', [])
        # 组织成处方结构
        prescription = {
            'constitution': constitution,
            'acupoints': acupoints,
            'summary': f"针对 {constitution} 体质推荐 {len(acupoints)} 个穴位",
        }
        return prescription

    registry.register(
        name='get_acupoint_prescription',
        description='根据体质代码生成穴位处方，返回穴位名称、定位、操作方法。用于养生方案中的穴位调理部分。',
        parameters={
            'type': 'object',
            'properties': {
                'constitution': {
                    'type': 'string',
                    'description': '体质代码：pinghe/qixu/yangxu/yinxu/tanshi/shire/xueyu/qiyu/tebing'
                }
            },
            'required': ['constitution']
        },
        func=get_acupoint_prescription,
        category='acupoint'
    )
