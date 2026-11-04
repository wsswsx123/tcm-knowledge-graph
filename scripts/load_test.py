"""并发压测：测量 P50/P95/P99 延迟、吞吐与错误率。

不依赖 locust/ab（仅标准库），方便在 CI、内网、面试现场直接跑。
每个工作线程复用一条 HTTP 长连接（keep-alive），贴近浏览器/网关的真实行为，
也避免 Windows 上短连接快速耗尽临时端口导致的大量 URLError。

用法：
  # 默认混合读接口（/health、/metrics、/api/questions）
  python scripts/load_test.py --base-url http://127.0.0.1:5101 --concurrency 20 --requests 800

  # 只压 Agent 对话（LLM 端到端，耗时较长，建议低并发）
  python scripts/load_test.py --base-url http://127.0.0.1:5101 \
      --endpoint /api/agents/chat --method POST \
      --body '{"user_input":"最近总是乏力气短，容易出汗"}' \
      --concurrency 5 --requests 10 --timeout 180

  # 输出 JSON 便于写进 README / 报表
  python scripts/load_test.py ... --json load_result.json

注意：
- 压测前先确认被测服务已预热完成（GET /health/ready 返回 200），
  否则测到的是冷启动成本而不是稳态性能。
- 若服务开启了默认限流（200 次/分钟/IP），大规模压测会大量返回 429，
  此时测的是限流器而非应用吞吐。测吞吐时把 RATE_LIMIT_DEFAULT 临时调大。
"""
import argparse
import http.client
import json
import queue
import re
import statistics
import sys
import threading
import time
import urllib.parse

DEFAULT_MIX = [
    # (method, path, body, weight)
    # 说明：不在默认混合里放 /api/auth/login —— 它被显式限流为 10 次/分钟
    # （安全设计），压测会大量收到 429，掩盖真实吞吐。登录性能请单独用
    # --endpoint /api/auth/login --requests 10 小样本测量。
    ('GET', '/health', None, 30),
    ('GET', '/metrics', None, 20),
    ('GET', '/api/questions', None, 50),
]


def _percentile(sorted_values, p):
    if not sorted_values:
        return 0.0
    k = (len(sorted_values) - 1) * (p / 100.0)
    lo, hi = int(k), min(int(k) + 1, len(sorted_values) - 1)
    return sorted_values[lo] + (sorted_values[hi] - sorted_values[lo]) * (k - lo)


def _normalize_path(path):
    """把用户传入的路径规整成 /xxx。

    主要兼容 Git Bash（MSYS）的路径自动转换：`--endpoint /health` 会被
    改写成 `D:/.../PortableGit/health` 之类的 Windows 路径，直接发出去必然 404。
    """
    if not path:
        return '/'
    normalized = path.replace('\\', '/')
    m = re.search(r'/(?:Portable)?Git/(.*)$', normalized)
    if m:
        normalized = '/' + m.group(1)
    if not normalized.startswith('/'):
        normalized = '/' + normalized
    return normalized


class _Endpoint:
    """目标地址解析 + 长连接管理（每线程一条）。"""

    def __init__(self, base_url, timeout):
        parsed = urllib.parse.urlsplit(base_url)
        self.host = parsed.hostname or '127.0.0.1'
        self.port = parsed.port or (443 if parsed.scheme == 'https' else 80)
        self.https = parsed.scheme == 'https'
        self.timeout = timeout
        self._local = threading.local()

    def _conn(self):
        conn = getattr(self._local, 'conn', None)
        if conn is None:
            cls = http.client.HTTPSConnection if self.https else http.client.HTTPConnection
            conn = cls(self.host, self.port, timeout=self.timeout)
            self._local.conn = conn
        return conn

    def close(self):
        conn = getattr(self._local, 'conn', None)
        if conn is not None:
            try:
                conn.close()
            except Exception:
                pass
            self._local.conn = None

    def request(self, method, path, body):
        """发一次请求；连接断开时重连重试一次。返回 (状态码, 错误)。"""
        payload = json.dumps(body).encode('utf-8') if body is not None else None
        headers = {'Content-Type': 'application/json'} if payload is not None else {}
        for attempt in (1, 2):
            try:
                conn = self._conn()
                conn.request(method, path, body=payload, headers=headers)
                resp = conn.getresponse()
                resp.read()
                return resp.status, None
            except Exception as e:
                self.close()
                if attempt == 2:
                    return 0, type(e).__name__
        return 0, 'unknown'


def run(base_url, plan, concurrency, total, timeout):
    """plan: list[(method, path, body)]，长度 = total，由各线程消费。"""
    latencies, statuses, errors = [], {}, {}
    lock = threading.Lock()
    target = _Endpoint(base_url, timeout)
    q = queue.Queue()
    for item in plan:
        q.put(item)

    def worker():
        while True:
            try:
                method, path, body = q.get_nowait()
            except queue.Empty:
                return
            t0 = time.perf_counter()
            status, err = target.request(method, path, body)
            ms = (time.perf_counter() - t0) * 1000
            with lock:
                latencies.append(ms)
                statuses[status] = statuses.get(status, 0) + 1
                if err:
                    errors[err] = errors.get(err, 0) + 1
        target.close()

    t0 = time.perf_counter()
    threads = [threading.Thread(target=worker) for _ in range(concurrency)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    wall = time.perf_counter() - t0

    latencies.sort()
    ok = sum(v for k, v in statuses.items() if 200 <= k < 400)
    client_err = sum(v for k, v in statuses.items() if 400 <= k < 500)
    server_err = sum(v for k, v in statuses.items() if k >= 500)
    failed = server_err + sum(errors.values())
    return {
        'base_url': base_url,
        'concurrency': concurrency,
        'requests': total,
        'wall_seconds': round(wall, 3),
        'rps': round(total / wall, 2) if wall > 0 else 0,
        'success': ok,
        'client_errors': client_err,
        'server_errors': server_err,
        # 错误率只统计服务端故障（5xx + 连接异常）；4xx 属业务语义（限流/未授权）
        'error_rate': round(failed / total, 4) if total else 0,
        'status_codes': {str(k): v for k, v in sorted(statuses.items())},
        'exceptions': errors,
        'latency_ms': {
            'min': round(latencies[0], 1) if latencies else 0,
            'p50': round(_percentile(latencies, 50), 1),
            'p95': round(_percentile(latencies, 95), 1),
            'p99': round(_percentile(latencies, 99), 1),
            'max': round(latencies[-1], 1) if latencies else 0,
            'mean': round(statistics.fmean(latencies), 1) if latencies else 0,
        },
    }


def main():
    ap = argparse.ArgumentParser(description='轻量并发压测（标准库实现）')
    ap.add_argument('--base-url', default='http://127.0.0.1:5101')
    ap.add_argument('--concurrency', type=int, default=20)
    ap.add_argument('--requests', type=int, default=800, help='总请求数')
    ap.add_argument('--timeout', type=float, default=30.0, help='单请求超时（秒）')
    ap.add_argument('--endpoint', help='只压这一个路径（不指定则用默认混合场景）')
    ap.add_argument('--method', default='GET')
    ap.add_argument('--body', help='请求体 JSON 字符串（--endpoint 为 POST 时使用）')
    ap.add_argument('--json', dest='json_out', help='把结果写入 JSON 文件')
    args = ap.parse_args()

    if args.requests <= 0:
        ap.error('--requests 必须大于 0')
    if args.concurrency <= 0:
        ap.error('--concurrency 必须大于 0')

    if args.endpoint:
        body = json.loads(args.body) if args.body else None
        plan = [(args.method.upper(), _normalize_path(args.endpoint), body)] * args.requests
    else:
        pool = []
        for method, path, body, weight in DEFAULT_MIX:
            pool.extend([(method, path, body)] * weight)
        plan = [pool[i % len(pool)] for i in range(args.requests)]

    report = run(args.base_url, plan, args.concurrency, args.requests, args.timeout)

    print(f"目标: {report['base_url']}  并发: {report['concurrency']}  请求: {report['requests']}")
    print(f"耗时: {report['wall_seconds']}s  吞吐: {report['rps']} req/s")
    lat = report['latency_ms']
    print(f"延迟(ms): p50={lat['p50']}  p95={lat['p95']}  p99={lat['p99']}  "
          f"mean={lat['mean']}  max={lat['max']}")
    print(f"状态码: {report['status_codes']}  "
          f"服务端错误率: {report['error_rate'] * 100:.2f}%")
    if report['exceptions']:
        print(f"异常: {report['exceptions']}")

    if args.json_out:
        with open(args.json_out, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"结果已写入 {args.json_out}")

    # 5xx 或连接异常视为失败，便于在 CI 中当门禁用
    if report['error_rate'] > 0.01:
        sys.exit(1)


if __name__ == '__main__':
    main()
