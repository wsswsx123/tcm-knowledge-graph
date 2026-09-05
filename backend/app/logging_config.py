# backend/app/logging_config.py
"""
结构化 JSON 日志 + 文件轮转。

- JsonFormatter：把日志记录序列化为单行 JSON（含 request_id / method / status / latency 等 extra 字段）。
- setup_logging：配置 root logger（控制台 + 轮转文件），供 create_app 调用。
"""
import json
import logging
import os
from logging.handlers import RotatingFileHandler

# 需要在 JSON 输出中透传的额外字段
_EXTRA_FIELDS = (
    'request_id', 'method', 'path', 'status', 'latency',
    'tool', 'mode', 'stage', 'rejected', 'dropped',
)


class JsonFormatter(logging.Formatter):
    def format(self, record):
        data = {
            'ts': self.formatTime(record, '%Y-%m-%dT%H:%M:%S'),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
        }
        for key in _EXTRA_FIELDS:
            if hasattr(record, key):
                data[key] = getattr(record, key)
        if record.exc_info:
            data['exc_info'] = self.formatException(record.exc_info)
        return json.dumps(data, ensure_ascii=False)


def setup_logging(app):
    """配置结构化日志：控制台 + 轮转文件。"""
    level = app.config.get('LOG_LEVEL', 'INFO')
    log_file = app.config.get('LOG_FILE', 'logs/app.log')

    root = logging.getLogger()
    root.setLevel(getattr(logging, level, logging.INFO))
    root.handlers = []

    formatter = JsonFormatter()

    console = logging.StreamHandler()
    console.setFormatter(formatter)
    root.addHandler(console)

    try:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        fh = RotatingFileHandler(
            log_file, maxBytes=10 * 1024 * 1024, backupCount=5, encoding='utf-8'
        )
        fh.setFormatter(formatter)
        root.addHandler(fh)
    except Exception:
        # 文件日志不可用不影响服务启动
        pass
