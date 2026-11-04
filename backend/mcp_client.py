# backend/mcp_client.py
"""
MCP 协议客户端：以子进程方式拉起 mcp_server/server.py，通过 stdio 调用其工具。

设计：
- 后台线程持有 asyncio 事件循环与持久 ClientSession。
- 同步接口 has_tool / call_tool 供 ToolRegistry 调用。
- 连接失败时 has_tool 返回 False，ToolRegistry 自动回退到本地 Python 调用，
  保证 Demo 在无 MCP 环境下依然可用。
"""
import atexit
import asyncio
import json
import logging
import os
import threading
from typing import Any, Dict, Optional, Set

from app.config import Config

logger = logging.getLogger(__name__)


class MCPClient:
    """同步包装的 MCP 客户端。"""

    def __init__(self, command: str = None, script: str = None, cwd: str = None):
        self.command = command or getattr(Config, 'MCP_SERVER_CMD', 'python')
        self.script = script or getattr(Config, 'MCP_SERVER_SCRIPT')
        self.cwd = cwd or os.path.dirname(self.script)
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._thread: Optional[threading.Thread] = None
        self._session = None
        self._stdio_ctx = None
        self._session_ctx = None
        self._tools: Set[str] = set()
        self._connected = False
        self._call_timeout = getattr(Config, 'TOOL_TIMEOUT', 60.0)
        # 连接阶段超时：server.py 首次 import torch/transformers/py2neo 在 Windows
        # 冷启动下可能要 6-10 秒，叠加 Flask debug reloader 双进程资源争抢时
        # 可能到 20-30 秒，所以默认给 60 秒余量；可通过环境变量覆盖。
        self._connect_timeout = float(os.environ.get('MCP_CONNECT_TIMEOUT', '60.0'))
        # 工具级"冷启动超时"——MCP 首工具的 lazy init 成本远高于稳态调用。
        # 正常调用超时仍沿用 TOOL_TIMEOUT 全局，这里不做分层差异；
        # 实际策略是 connect 完成后立刻 warmup，把首包成本吃掉。

    @property
    def connected(self) -> bool:
        return self._connected

    def connect(self, timeout: float = None) -> bool:
        """建立与 MCP Server 的连接。成功返回 True。"""
        timeout = timeout or self._connect_timeout
        self._loop = asyncio.new_event_loop()
        ready = threading.Event()
        err_box = []

        def runner():
            asyncio.set_event_loop(self._loop)
            try:
                self._loop.run_until_complete(self._async_connect(ready, err_box))
                # 保持 loop 运行以承接后续 call_tool
                if self._connected:
                    self._loop.run_forever()
            except Exception as e:
                if not err_box:
                    err_box.append(e)
                ready.set()
            # 注意：asyncio.CancelledError 不是 Exception 的子类，单独捕获
            except BaseException as e:  # noqa: BLE001
                if not err_box:
                    err_box.append(e)
                ready.set()

        logger.info(f"开始连接 MCP Server (cmd={self.command}, timeout={timeout}s)")
        self._thread = threading.Thread(target=runner, daemon=True)
        self._thread.start()
        ok = ready.wait(timeout)
        if not ok:
            logger.warning(
                f"MCP Server 连接超时 ({timeout}s)，工具将回退本地调用。"
                f" 若为 Windows 冷启动可在 .env 中设置 MCP_CONNECT_TIMEOUT=120 放宽。"
            )
            # 主动取消正在进行的连接流程，释放后台线程/子进程资源
            try:
                if self._loop and self._loop.is_running():
                    self._loop.call_soon_threadsafe(self._loop.stop)
            except Exception:
                pass
            return False
        if not self._connected:
            cause = err_box[0] if err_box else "未知原因"
            logger.warning(f"MCP Server 连接失败: {cause}，工具将回退本地调用")
            return False
        logger.info(f"MCP Server 已连接，可用工具: {self._tools}")
        # 注册 atexit：Werkzeug reloader 子进程重启 / Ctrl+C / 正常退出 时，
        # 先优雅关闭事件循环 → 关闭 stdio → MCP Server 子进程感知 EOF 退出。
        # 否则 warmup/任何正在进行的异步协程会收到 CancelledError 后又被包装成
        # KeyboardInterrupt，在 stderr 输出一屏 traceback 吓用户。
        try:
            atexit.register(self.shutdown)
        except Exception as e:  # pragma: no cover
            logger.info(f"注册 atexit 失败（不影响服务）: {e}")
        # 连接成功后立刻做一次后台 warmup（不阻塞 connect 结果）：
        # 调用 1 个 RAG 工具 + 1 个图谱工具，提前触发 MCP Server 侧的
        # py2neo / torch / sentence_transformers / FAISS lazy init。
        # 这样后续真正的用户消息到来时工具调用就是稳态耗时。
        try:
            if self._loop is not None and self._session is not None:
                asyncio.run_coroutine_threadsafe(
                    self._async_warmup(), self._loop
                )
                logger.info("MCP warmup 任务已提交(后台执行)")
        except Exception as e:  # pragma: no cover - warmup 失败不影响功能
            logger.warning(f"MCP warmup 任务提交失败(不影响正常工具调用): {e}")
        return True

    async def _async_connect(self, ready: threading.Event, err_box: list):
        from mcp import ClientSession, StdioServerParameters
        from mcp.client.stdio import stdio_client
        try:
            logger.debug(f"MCP 启动子进程: {self.command} {self.script}")
            # 注入子进程环境变量：
            #   PYTHONIOENCODING=utf-8 : 强制子进程 stdin/stdout/stderr 用 UTF-8，
            #     避免 Windows 默认 GBK(CP936) 控制台输出中文时，客户端按 UTF-8 解析
            #     stdout 抛出 UnicodeDecodeError，进而触发 cancel scope 取消。
            #   PYTHONUNBUFFERED=1   : 让 Python stdout 无缓冲，MCP JSON-RPC 帧即时可达。
            env = os.environ.copy()
            env['PYTHONIOENCODING'] = 'utf-8'
            env['PYTHONUNBUFFERED'] = '1'
            params = StdioServerParameters(command=self.command,
                                           args=[self.script], cwd=self.cwd, env=env)
            self._stdio_ctx = stdio_client(params)
            read, write = await self._stdio_ctx.__aenter__()
            logger.debug("MCP stdio 管道已建立，开始 initialize 握手")
            self._session_ctx = ClientSession(read, write)
            self._session = await self._session_ctx.__aenter__()
            await self._session.initialize()
            logger.debug("MCP initialize 握手成功，开始拉取工具列表")
            tools_resp = await self._session.list_tools()
            self._tools = {t.name for t in tools_resp.tools}
            logger.debug(f"MCP 已获取工具列表: {self._tools}")
            self._connected = True
        except asyncio.CancelledError as e:
            err_box.append(RuntimeError(f"连接阶段被取消（可能是超时触发）: {e}"))
            await self._cleanup()
        except Exception as e:
            err_box.append(e)
            await self._cleanup()
        finally:
            ready.set()

    async def _cleanup(self):
        try:
            if self._session_ctx is not None:
                await self._session_ctx.__aexit__(None, None, None)
        except Exception:
            pass
        try:
            if self._stdio_ctx is not None:
                await self._stdio_ctx.__aexit__(None, None, None)
        except Exception:
            pass
        self._connected = False

    def has_tool(self, name: str) -> bool:
        return self._connected and name in self._tools

    def call_tool(self, name: str, args: Dict[str, Any]) -> Any:
        """同步调用 MCP 工具，返回解析后的 Python 对象。"""
        if not self._connected or self._session is None:
            raise RuntimeError("MCP client 未连接")
        fut = asyncio.run_coroutine_threadsafe(
            self._async_call(name, args), self._loop)
        try:
            return fut.result(timeout=self._call_timeout)
        except Exception as e:
            # TimeoutError / concurrent.futures.TimeoutError 直接 str 会是
            # "工具调用超时(60.0s)"或空串，导致最终 ERROR 日志显示
            # "MCP 工具 xxx 调用失败: "，缺少可读细节。这里统一格式化。
            msg = f"{type(e).__name__}: {e}" if str(e) else type(e).__name__
            logger.error(f"MCP 工具 {name} 调用失败: {msg}")
            raise

    async def _async_call(self, name: str, args: Dict[str, Any]) -> Any:
        result = await self._session.call_tool(name, args)
        # result.content 是 list[TextContent | ...]
        contents = getattr(result, 'content', []) or []
        for c in contents:
            text = getattr(c, 'text', None)
            if text is None:
                continue
            # FastMCP 执行工具失败时（参数校验、工具内部异常），错误文本
            # 以 "Error executing tool xxx: ..." 作为普通 content 返回，
            # JSON-RPC 层本身成功，直接返回会被上层误判为"调用成功"——
            # 例如把校验错误字符串当案例列表传进 Agent，导致
            # 'str' object has no attribute 'get'。这里识别并抛异常，
            # 让 ToolRegistry 走重试 / 回退本地调用。
            if isinstance(text, str) and text.lstrip().startswith('Error executing tool'):
                raise RuntimeError(text.strip()[:300])
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return text
        return None

    async def _async_warmup(self):
        """
        后台预热：尽早触发 MCP Server 子进程的 lazy init。
        调用参数设计成"极小成本"，避免实际 CPU/GPU 争用影响 Flask 主进程。

        重要：Werkzeug debug reloader 子进程在 restart/exit 时会被父进程发送 SIGTERM/退出，
        此时如果 warmup 还在运行，Python 会把 asyncio.CancelledError 包装成 KeyboardInterrupt
        输出大段 traceback 到 stderr（看起来像 fatal error，但其实只是程序正常退出）。
        本函数自己把 CancelledError/SystemExit/KeyboardInterrupt 全部静默吞掉。
        """
        tasks_specs = []
        # RAG 侧：torch + sentence-transformers + FAISS + CaseRetriever
        if 'retrieve_similar_cases' in self._tools:
            tasks_specs.append(
                ('retrieve_similar_cases',
                 {'symptoms': ['乏力'], 'tongue': '', 'pulse': ''})
            )
        # 图谱侧：py2neo.Graph + KGRetriever
        if 'get_constitution_recommendations' in self._tools:
            tasks_specs.append(
                ('get_constitution_recommendations', {'constitution': 'pinghe'})
            )
        if not tasks_specs:
            return
        logger.info("MCP warmup: 开始预热 RAG/图谱资源")
        try:
            # 顺序调用，避免冷启动时 GPU / CUDA / py2neo 一次性抢爆
            for name, kwargs in tasks_specs:
                # warmup 内部允许较长耗时，但不应影响真正用户请求。
                # 用 asyncio.shield 防止外部误取消；超时用 wait_for。
                try:
                    await asyncio.wait_for(
                        self._session.call_tool(name, kwargs),
                        timeout=max(self._call_timeout, 120.0),
                    )
                except asyncio.TimeoutError:
                    logger.info(f"MCP warmup: {name} 超时，跳过（不影响功能）")
                except Exception as sub_e:
                    # KeyboardInterrupt/CancelledError 在这里会被下面的大 except 兜底
                    if isinstance(sub_e, (asyncio.CancelledError,
                                          KeyboardInterrupt, SystemExit)):
                        return
                    logger.info(
                        f"MCP warmup: {name} 非致命错误 {type(sub_e).__name__}，"
                        "跳过（不影响后续工具调用）"
                    )
            logger.info(
                "MCP warmup: 完成，子进程侧 py2neo/torch/FAISS/sentence-transformers 已就绪"
            )
        except (asyncio.CancelledError, KeyboardInterrupt, SystemExit):
            # 典型场景：debug reloader 重启 / Ctrl+C。不是 bug，静默返回即可。
            logger.info("MCP warmup: 进程退出取消，终止预热")
            return
        except Exception as e:
            logger.warning(f"MCP warmup 失败(不影响服务): {e}")

    def shutdown(self):
        """
        优雅关闭后台事件循环与 MCP 管道。
        典型触发：atexit / Werkzeug reloader 子进程重启 / Ctrl+C。
        全部容错，绝不抛异常到进程退出逻辑里去。
        """
        logger.info("MCP client: 开始优雅关闭")
        try:
            if self._loop and self._loop.is_running():
                # 先关闭 session / stdio（会让正在跑的 warmup 收到 CancelledError，
                # 但 warmup 已经自己捕获并静默），再停事件循环。
                asyncio.run_coroutine_threadsafe(self._cleanup(), self._loop)
                # 等一会儿让 cleanup 落到子进程里（管道关 → MCP Server 自己退出）
                self._loop.call_later(1.0, self._loop.stop)
        except Exception as e:  # pragma: no cover
            logger.info(f"MCP client: session cleanup 失败（退出中，忽略）: {e}")
        try:
            if self._thread and self._thread.is_alive():
                self._thread.join(timeout=2.0)
        except Exception as e:  # pragma: no cover
            logger.info(f"MCP client: 后台线程 join 失败（退出中，忽略）: {e}")
        self._connected = False
        logger.info("MCP client: 已关闭")


_client: Optional[MCPClient] = None
_client_init = False


def get_mcp_client() -> Optional[MCPClient]:
    """
    全局单例。仅当 Config.MCP_ENABLED 且连接成功时返回有效 client。
    连接失败返回 None（调用方应回退本地调用）。
    """
    global _client, _client_init
    if _client_init:
        return _client if (_client and _client.connected) else None
    _client_init = True
    if not getattr(Config, 'MCP_ENABLED', True):
        logger.info("MCP 已在配置中禁用，工具走本地调用")
        return None
    _client = MCPClient()
    if _client.connect(timeout=30.0):
        return _client
    _client = None
    return None
