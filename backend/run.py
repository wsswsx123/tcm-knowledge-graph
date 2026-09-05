# backend/run.py (增强版)
from app import create_app
from app.routes.ai_assessment import init_ai_services
import logging

app = create_app()

# 初始化AI服务
with app.app_context():
    init_ai_services(app)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(debug=True, host='0.0.0.0', port=5000)