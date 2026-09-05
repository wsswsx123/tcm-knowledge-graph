# P0 设计文档：文档 + 配置地基

日期：2026-09-04
状态：已批准（待落地）

## 背景

`tcm-knowledge-graph` 代码库已实现多 Agent 体质辨识、RAG、MCP、幻觉抑制、五级容错等能力，但：

1. `README.md` 仍描述旧的单模型架构，未覆盖多 Agent / MCP / RAG / 幻觉抑制等真实实现。
2. `AGENTS.md` 的模块清单缺少 `services/agents/`、`services/rag/`、`services/tools/`、`confidence.py`、`grounding.py`、`observability.py`、`mcp_server/`、`evaluation.py` 等。
3. 配置存在硬编码 `SECRET_KEY`，无 `.env` 加载与生产环境告警。
4. 无统一的错误响应形状与请求 ID 追踪。

本阶段（P0）目标：补齐以上工程化地基，全部为**纯增量、零行为破坏**改动。

## 范围（4 个交付物）

### ① 重写 `README.md`
- 一句话定位 + 技术亮点清单
- mermaid 架构图（MasterAgent → 三子 Agent，两侧挂 RAG / Neo4j / MCP）
- 多 Agent 协同流程（含置信度不足→澄清的多轮状态机）
- RAG 检索链路、幻觉抑制机制、五级容错降级表、MCP 协议
- 评测结果（引用 `evaluation_report.json`）
- 快速开始（本地；Docker 占位标注 P2 待补）、项目结构、API 一览、免责声明

### ② 更新 `AGENTS.md`
补充缺失模块职责；验证建议增加 pytest（P1 落地后启用）与 compileall / build。

### ③ 配置地基（`backend/app/config.py` + 新增 `.env.example`）
- 顶部 `load_dotenv()`
- SECRET_KEY 未配置时 `secrets.token_hex(32)` 随机生成 + warning（不再硬编码 `dev-secret-key`）
- 新增 `APP_ENV`；生产环境仍用默认 DB/Neo4j 密码时打 warning
- 保留"Demo 永远可用"：开发默认值保留

### ④ 错误处理 + 请求 ID 中间件（新增 `backend/app/middleware.py`）
- `before_request`：生成/透传 `request_id`
- `after_request`：回写 `X-Request-ID` + 一行请求日志（method/path/status/latency/request_id）
- 全局 `errorhandler`：统一错误 JSON `{ "error": { "code", "message", "request_id" } }`
- 仅动错误路径，成功响应现有结构不变

## 关键决策

1. **配置不迁移 pydantic-settings**：全库大量 `Config.XXX` / `getattr(Config,...)` 类级访问，迁移牵一发动全身，P0 保持 `Config` 类 + `os.environ`。
2. **完整结构化日志/轮转放到 P3**：P0 仅做请求 ID + 统一错误，避免返工。

## 非目标（后续阶段）

- P1：pytest + CI
- P2：Docker / docker-compose
- P3：/health /metrics、结构化 JSON 日志、ObservabilityHub API
- P4：JWT、CORS 白名单、限流、输入校验、OpenAPI
- P5：Alembic 迁移、Redis 会话持久化
- P6：SSE 流式、前端测试、Prompt 版本管理

## 验收标准

- `backend` 通过 `python -m compileall app`
- `README.md` / `AGENTS.md` 准确描述真实架构与模块
- 启动后端后，访问一个不存在路由应返回统一错误 JSON（含 `request_id`），响应头含 `X-Request-ID`
- 未配置 `SECRET_KEY` 时启动有 warning，且密钥为随机值
