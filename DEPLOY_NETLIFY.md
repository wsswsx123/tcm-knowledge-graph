# Netlify 部署说明

本项目建议采用“Netlify 托管前端 + 独立平台托管 Flask 后端”的方式部署。

## 1. 后端先部署到独立服务

后端依赖 Flask、MySQL、Neo4j，以及本地模型或 Ollama。Netlify 更适合静态前端和轻量函数，不适合直接运行这个完整后端。

可以把 `backend/` 部署到 Render、Railway、云服务器或校内服务器，并配置这些环境变量：

```bash
DATABASE_URL=mysql+pymysql://USER:PASSWORD@HOST:PORT/tcm_health
NEO4J_URI=bolt://HOST:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your-password
SECRET_KEY=your-secret-key
USE_OLLAMA=true
OLLAMA_URL=http://HOST:11434/api/generate
```

后端启动命令：

```bash
cd backend
pip install -r requirements.txt
python run.py
```

生产环境建议使用 Gunicorn、Waitress 或平台自带的 WSGI 启动方式。

## 2. 在 Netlify 部署前端

仓库根目录已经添加 `netlify.toml`，Netlify 会使用：

- Base directory: `frontend`
- Build command: `npm run build`
- Publish directory: `frontend/dist`

在 Netlify 的 Site settings -> Environment variables 中设置：

```bash
VITE_API_BASE=https://你的后端域名
```

如果后端 API 前缀仍是 `/api`，则 `VITE_API_BASE` 只需要填后端根地址，例如：

```bash
VITE_API_BASE=https://tcm-api.example.com
```

## 3. 本地预检查

```bash
cd frontend
npm run build
```

```bash
cd backend
python -m compileall app
```

通过后再在 Netlify 导入 Git 仓库，或用 CLI 执行：

```bash
npx netlify status
npx netlify deploy
npx netlify deploy --prod
```
