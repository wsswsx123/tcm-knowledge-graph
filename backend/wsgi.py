"""WSGI 入口：gunicorn 生产环境使用。

与 run.py 的初始化逻辑保持一致（创建应用 + 初始化 AI 服务）。
"""
from app import create_app
from app.routes.ai_assessment import init_ai_services

app = create_app()

with app.app_context():
    init_ai_services(app)
