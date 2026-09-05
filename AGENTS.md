# AGENTS.md

本文件为在本项目中工作的 AI agent 和协作者提供约定。请优先遵循本文件，其次参考 `README.md`。

## 项目概览

这是一个中医体质辨识与养生推荐系统，采用前后端分离架构：

- `backend/`: Flask REST API，负责用户认证、问卷测评、推荐、知识图谱查询、多 Agent 问诊（症状/体质/方案三级协同 + 置信度门控 + 幻觉抑制）与 MCP 工具服务。
- `frontend/`: Vue 3 + Vite 单页应用，负责问卷、结果、推荐、知识图谱可视化和多 Agent 问诊可视化界面。
- `data/`: MySQL 与 Neo4j 初始化脚本、知识图谱生成脚本，以及 RAG 案例库 / 向量索引 / 临床评测样本。
- `backend/models/`: 本地大模型文件目录，体积较大，通常不要改动或提交。
- `start.bat` / `stop.bat`: Windows 下的一键启动和停止脚本。

核心外部服务：

- MySQL 8.0: 用户、题目、测评结果等结构化数据。
- Neo4j 4.4+: 体质、穴位、食材、运动等知识图谱。
- Qwen2.5-3B-Instruct 或 Ollama: AI 问题解释、追问、结果解读和推荐增强。

## 常用命令

### 后端

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

默认后端地址为 `http://127.0.0.1:5000`。

### 前端

```bash
cd frontend
npm install
npm run dev
npm run build
```

默认前端开发地址为 `http://127.0.0.1:5173`。前端通过 Vite 代理访问 `/api`，代理目标在 `frontend/vite.config.js` 中配置。

### 一键启动

Windows 环境可在项目根目录执行：

```bat
start.bat
```

脚本会尝试启动后端 Flask 服务和前端 Vite 服务。

### Docker 一键部署

```bash
docker compose up -d --build
```

编排见根目录 `docker-compose.yml`：MySQL / Neo4j / Ollama / 后端 / 前端，并自动初始化数据与模型。
后端容器用 `gunicorn` 单 worker 启动（会话状态当前在进程内存，多 worker 需先落 Redis）；依赖为 `backend/requirements-docker.txt`（CPU 版，不含本地 Transformers 权重）。

## 目录职责

后端主要结构：

- `backend/run.py`: Flask 应用入口。
- `backend/app/__init__.py`: 应用工厂、扩展初始化和蓝图注册。
- `backend/app/config.py`: 数据库、Neo4j、AI 模型和运行配置（`.env` 驱动）。
- `backend/app/middleware.py`: 请求ID 透传、请求日志、统一错误响应。
- `backend/app/logging_config.py`: 结构化 JSON 日志 + 文件轮转。
- `backend/app/models/`: MySQL 与 Neo4j 数据模型。
- `backend/app/routes/`: API 蓝图。
  - `auth.py`: 注册、登录等认证接口。
  - `assessment.py`: 问卷题目、测评提交和历史记录。
  - `recommend.py`: 推荐接口。
  - `graph.py`: 知识图谱查询接口。
  - `admin.py`: 后台图谱管理接口。
  - `ai_assessment.py`: AI 解释、追问、解读、推荐增强接口。
  - `agents.py`: 多 Agent 对话、会话重置、工具列表接口。
  - `observability.py`: 存活/就绪探针、指标、OpenAPI/Swagger 接口。
- `backend/app/services/`: 核心业务逻辑。
  - `constitution.py`: 体质评分和判定算法（问卷测评）。
  - `rag_service.py`: Neo4j 检索与基础推荐。
  - `ai_service.py`: AI 调用统一封装。
  - `model_loader.py`: 本地模型加载与卸载。
  - `agents/`: 多 Agent 架构。
    - `master_agent.py`: 主控仲裁，调度三级 Agent 与多轮会话状态。
    - `symptom_agent.py`: 症状分析（提取结构化症状/舌象/脉象）。
    - `constitution_agent.py`: 体质推理（RAG 召回 + CoT + 置信度校准）。
    - `plan_agent.py`: 方案生成（调用图谱工具 + 实体锚定）。
    - `base_agent.py`: Agent 基类（LLM 接入、Function Calling、JSON 解析、降级）。
  - `prompts/cot_templates.py`: 三级 Agent 的 CoT Few-shot 提示词模板。
  - `rag/`: RAG 检索链路。
    - `case_retriever.py`: 案例检索器（构建/加载向量库，对外 retrieve()）。
    - `embeddings.py`: 句向量后端（sentence-transformer / TF-IDF）。
    - `vector_store.py`: 向量库（FAISS / NumPy 暴力检索 + 持久化）。
    - `multimodal_features.py`: 舌象/脉象文本特征拼接。
  - `tools/`: Function Calling 工具层。
    - `registry.py`: 统一工具注册表（重试、超时、日志、MCP/本地双模式）。
    - `kg_tools.py` / `acupoint_tools.py` / `rag_tools.py`: 图谱/穴位/RAG 工具。
  - `confidence.py`: 置信度阈值拒答机制（低于阈值触发澄清）。
  - `grounding.py`: 方案幻觉抑制（实体锚定到知识图谱）。
  - `observability.py`: 运行时观测与五级容错状态。
  - `kg_fallback.py`: Neo4j 不可用时的静态知识底库。
  - `session_store.py`: 会话状态存储（Redis / 内存 fallback）。
- `backend/mcp_server/server.py`: 独立 MCP Server（stdio 暴露 4 个工具）。
- `backend/mcp_client.py`: MCP 客户端（子进程拉起 Server，失败回退本地）。
- `backend/evaluation.py`: 50 例临床样本评测脚本（幻觉率/拒答率/延迟）。
- `backend/openapi.json`: OpenAPI 3.0 规范（由 `/openapi.json` 与 `/docs` 提供）。
- `backend/app/utils/security.py`: 密码哈希、JWT 签发/校验、鉴权装饰器。

前端主要结构：

- `frontend/src/main.js`: Vue 应用入口。
- `frontend/src/App.vue`: 根组件。
- `frontend/src/router/`: Vue Router 配置。
- `frontend/src/store/`: Pinia 状态管理。
- `frontend/src/api/index.js`: Axios API 封装。
- `frontend/src/components/`: 可复用组件，如 AI 问题助手、底部导航、图谱图表。
- `frontend/src/views/`: 页面视图，如登录、问卷、结果、推荐、图谱、个人中心、后台管理。
- `frontend/src/index.css`: Tailwind 和全局样式。

## 开发约定

- 保持前后端 API 契约一致。改动后端接口时，同步检查 `frontend/src/api/index.js` 和相关视图调用。
- 后端新增业务逻辑优先放在 `backend/app/services/`，路由文件只做参数校验、调用服务和返回 JSON。
- 后端新增接口应按功能归入现有蓝图；确需新增蓝图时，在 `backend/app/__init__.py` 注册。
- 体质判定相关逻辑集中维护在 `backend/app/services/constitution.py`，避免在路由或前端重复实现评分规则。
- Neo4j 查询与推荐数据拼装优先放在 `rag_service.py`，不要把 Cypher 查询散落到多个路由中。
- AI 生成能力通过 `ai_service.py` 的统一接口接入，保留本地 Transformers 与 Ollama 两种模式的兼容性。
- 前端 API 请求统一通过 `frontend/src/api/index.js` 封装，避免在组件中硬编码完整后端 URL。
- 前端页面组件保持现有 Vue 3 Composition/Options 写法一致；修改 UI 时优先沿用 Tailwind CSS、ECharts 和 Lucide Vue。
- 不要提交或修改生成物与依赖目录，如 `node_modules/`、`venv/`、`__pycache__/`、模型权重文件、前端 `dist/`。

## 配置与数据

- 数据库和模型配置位于 `backend/app/config.py`。处理密码、密钥、模型路径时要避免硬编码真实敏感信息。
- MySQL 初始化脚本为 `data/init_mysql.sql`。
- Neo4j 初始化脚本为 `data/init_neo4j.cypher`。
- 若修改表结构、节点标签、关系类型或字段名，需要同步更新：
  - 后端模型与服务代码。
  - 初始化脚本。
  - 前端展示或管理页面。
  - README 或本文件中的相关说明。

## 验证建议

本项目已有 `backend/evaluation.py` 评测脚本（50 例样本，幻觉率/拒答率/延迟）；pytest 单元测试规划于后续阶段落地。完成改动后至少做以下验证：

- 后端语法检查：

```bash
cd backend
python -m compileall app
```

- 多 Agent 评测：

```bash
cd backend
python evaluation.py
```

- 前端构建检查：

```bash
cd frontend
npm run build
```

- 涉及接口或数据流时，手动启动 MySQL、Neo4j、后端和前端，验证关键页面：
  - 注册/登录。
  - 问卷填写与提交。
  - AI 问题解释或追问。
  - 结果页、推荐页、图谱页。
  - 后台知识图谱管理页。

## Agent 注意事项

- 修改前先阅读相关路由、服务、前端调用和数据脚本，避免只改一侧造成联调失败。
- 如果运行命令需要数据库、Neo4j、模型或网络下载，请在结果中说明哪些验证未能完成。
- 大模型目录和虚拟环境可能很大，搜索文件时排除 `backend/models/`、`frontend/node_modules/`、`venv/` 和 `__pycache__/`。
- README 在部分 Windows 终端可能出现编码显示异常；以源码文件和实际配置为准。
- 回答用户时使用中文，保持说明简洁，并明确列出已修改文件和已执行的验证命令。
