/**
 * 前端用户行为埋点（P2-4）
 *
 * 上报到 POST /api/agents/events，由后端 observability 聚合，
 * 可在 /api/observability/metrics 的 metrics.user_events 中观测。
 *
 * 设计原则：异步、静默失败、不阻塞业务、不携带个人信息。
 */
import axios from '@/api'

let _queue = Promise.resolve()

/** 串行上报（避免并发堆积），失败静默（localStorage/网络异常均不影响功能）。 */
export function reportUserEvent(event, payload = {}, opts = {}) {
  const { debounceMs = 0, silent = true } = opts
  if (debounceMs > 0) {
    // 高频事件（如重复提问）做 800ms 去抖，只上报一次
    if (reportUserEvent._debounce && reportUserEvent._debounce[event]) {
      return
    }
    reportUserEvent._debounce = reportUserEvent._debounce || {}
    reportUserEvent._debounce[event] = true
    setTimeout(() => {
      if (reportUserEvent._debounce) delete reportUserEvent._debounce[event]
    }, debounceMs)
  }
  _queue = _queue
    .then(() =>
      axios
        .post('/api/agents/events', { event, payload: payload || {} })
        .catch((e) => {
          if (!silent) console.warn('[telemetry] 行为上报失败：', e?.message || e)
        })
    )
    .catch(() => {})
  return _queue
}

export default reportUserEvent
