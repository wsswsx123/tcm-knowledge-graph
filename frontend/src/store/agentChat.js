import { defineStore } from 'pinia'
import axios from '@/api'
import { reportUserEvent } from '@/utils/telemetry'

const STORAGE_KEY = 'tcm_agent_chat_v1'

/** SSE 进度阶段 → 用户可读文案 */
const STREAM_LABELS = {
  intent: '已理解你的意图',
  symptom_done: '已提取你的症状与情况',
  constitution_start: '体质推理中（RAG 召回 + CoT 推理）...',
  constitution_done: '体质推理完成',
  plan_start: '正在生成个性化调理方案...',
}

/** 从 localStorage 取 JWT（与 api/index.js 拦截器同源逻辑，供 fetch 使用）。 */
function _authHeader() {
  try {
    const stored = localStorage.getItem('tcm_user')
    if (!stored) return null
    const user = JSON.parse(stored)
    return user && user.token ? { Authorization: `Bearer ${user.token}` } : null
  } catch (e) {
    return null
  }
}

/** 从 localStorage 读取上次持久化的会话（JSON，失败则返回空对象）。 */
function _loadPersisted() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return {}
    const obj = JSON.parse(raw) || {}
    if (typeof obj !== 'object') return {}
    return obj
  } catch (e) {
    console.warn('[agentChat] 本地会话缓存读取失败，已忽略：', e)
    return {}
  }
}

function _persist(state) {
  try {
    localStorage.setItem(
      STORAGE_KEY,
      JSON.stringify({
        sessionId: state.sessionId,
        messages: state.messages,
        seed_source: state.seed_source || null,
        savedAt: Date.now(),
      })
    )
  } catch (e) {
    // localStorage 满 / 禁用 / 私有模式等情况不阻断功能
    console.warn('[agentChat] 本地会话缓存写入失败：', e)
  }
}

export const useAgentChatStore = defineStore('agentChat', {
  state: () => {
    const cached = _loadPersisted()
    return {
      /** 当前会话 ID；null 表示全新会话 */
      sessionId: cached.sessionId || null,
      /** 前端显示消息：[{ role, content, response, error, traceExpanded }] */
      messages: Array.isArray(cached.messages) ? cached.messages : [],
      /** 恢复状态：pending | done | failed | idle（组件 onMounted 前为 idle） */
      restoreStatus: 'idle',
      /** 问卷测评 seed 元数据：成功 seedFromAssessment 后写入；失败/null 表示未锚定 */
      seed_source: cached.seed_source || null,
      /** 是否在发送（或 seed）中，用于 UI spinner 与防重复提交 */
      loading: false,
      /** 当前请求的 AbortController，用于"停止生成" */
      abortController: null,
      /** SSE 流式进度：当前阶段 key 与展示文案（null 表示未在流式传输中） */
      streamStage: null,
      streamLabel: null,
      /** 最近一次错误消息；组件可读取后自行清空 */
      error: null,
      /** F10：最近一次发送的用户输入，供"重发"按钮复用 */
      lastUserInput: '',
    }
  },

  getters: {
    hasSession: (s) => Boolean(s.sessionId && s.messages.length),
    isSeeded: (s) => Boolean(s.seed_source && s.seed_source.assessment_id),
  },

  actions: {
    /** 保存到 store 并同步持久化到 localStorage。traceExpanded 默认折叠，还原时不展开。 */
    appendMessage(msg) {
      const normalized = {
        role: msg.role,
        content: msg.content || '',
        response: msg.response || null,
        error: Boolean(msg.error),
        traceExpanded: false,
      }
      this.messages.push(normalized)
      _persist(this.$state)
    },

    /** 更新 sessionId 并立即持久化。首次 chat 返回后调用。 */
    setSessionId(id) {
      if (id && id !== this.sessionId) {
        this.sessionId = id
        _persist(this.$state)
      }
    },

    /** 替换整条消息列表（后端恢复时用）。 */
    replaceMessages(messages) {
      this.messages = (Array.isArray(messages) ? messages : []).map((m) => ({
        role: m.role,
        content: m.content || '',
        response: m.response || null,
        error: Boolean(m.error),
        traceExpanded: false,
      }))
      _persist(this.$state)
    },

    /** 清空 seed_source 并持久化。 */
    clearSeedSource() {
      this.seed_source = null
      _persist(this.$state)
    },

    /**
     * 基于问卷测评 ID seed 一个会话：后端会把体质判定结果和问卷得分塞给 Master Agent，
     * 之后的对话不再重复做"症状采集 / 体质推理"，直接进入方案追问 / 细节解释阶段。
     *
     * @param {number} assessmentId
     * @param {{sessionId?:string|null, replaceSession?:boolean}} [options]
     */
    async seedFromAssessment(assessmentId, options = {}) {
      if (this.loading) return
      const { sessionId = null, replaceSession = false } = options || {}

      let prevMessages = null
      let prevSessionId = null
      if (replaceSession) {
        prevMessages = this.messages.slice()
        prevSessionId = this.sessionId
        // 不清 localStorage，等接口成功再替换；先仅替换内存态
        this.messages = []
        this.sessionId = null
      }

      this.loading = true
      this.error = null

      try {
        const body = { assessment_id: Number(assessmentId) }
        const sid = sessionId || this.sessionId
        if (sid) body.session_id = sid

        const res = await axios.post('/api/agents/seed_from_assessment', body)
        const data = (res && res.data) || {}
        const { session_id, seeded, seed_source } = data

        if (session_id) this.sessionId = session_id
        if (seed_source && typeof seed_source === 'object') {
          this.seed_source = { ...seed_source, seededAt: Date.now() }
        } else if (seeded === true) {
          // 兼容后端没返回 seed_source 但返回 seeded=true 的情况
          this.seed_source = {
            assessment_id: Number(assessmentId),
            primary: '',
            primary_name: '',
            secondary: [],
            secondary_names: [],
            scores: null,
            reason: null,
            seededAt: Date.now(),
          }
        }

        // 若原来的最后一条助手消息 stage==='seeded'，就不重复追加
        const last = this.messages.length ? this.messages[this.messages.length - 1] : null
        const alreadySeededMsg = Boolean(last && last.role === 'assistant' && last.response && last.response.stage === 'seeded')
        if (!alreadySeededMsg && this.seed_source) {
          const ss = this.seed_source
          const ssId = ss.assessment_id ?? assessmentId
          const primaryName = ss.primary_name || '主体质'
          const secondaryText =
            ss.secondary_names && ss.secondary_names.length
              ? '；兼夹 ' + ss.secondary_names.join('、')
              : ''
          this.appendMessage({
            role: 'assistant',
            content: `已根据第 #${ssId} 号问卷测评结果初始化：主 ${primaryName}${secondaryText}`,
            response: {
              stage: 'seeded',
              seed_source: {
                assessment_id: ss.assessment_id ?? assessmentId,
                primary: ss.primary || '',
                primary_name: ss.primary_name || '',
                secondary: ss.secondary || [],
                secondary_names: ss.secondary_names || [],
                scores: ss.scores || null,
                reason: ss.reason || null,
              },
              session_id: this.sessionId || session_id || null,
            },
            error: false,
          })
        }

        _persist(this.$state)
        reportUserEvent('assessment_seeded', {
          assessment_id: Number(assessmentId),
          primary: this.seed_source && this.seed_source.primary,
        })
        return { sessionId: this.sessionId, seedSource: this.seed_source, seeded: true }
      } catch (err) {
        // 回滚 replaceSession 造成的内存清空
        if (replaceSession) {
          this.messages = prevMessages || []
          this.sessionId = prevSessionId || null
        }
        const status = err && err.response ? err.response.status : 0
        const errPayload = (err && err.response && err.response.data && err.response.data.error) || {}
        let msg = ''
        if (status === 401) {
          msg = '请先登录后再导入问卷测评结果。'
        } else if (status === 403) {
          msg = '不是你的问卷测评，无法导入。'
        } else if (status === 404) {
          msg = '该问卷测评不存在。'
        } else {
          msg = (typeof errPayload === 'object' ? errPayload.message : errPayload) || err.message || '导入问卷测评失败'
        }
        this.error = { message: msg, code: status || (errPayload && errPayload.code) || 'seed_error' }
        reportUserEvent('seed_error', { status, code: this.error.code })
        throw Object.assign(err || new Error(msg), { userMessage: msg, status })
      } finally {
        this.loading = false
      }
    },

    /**
     * 发送一条用户消息：优先走 SSE 流式端点（阶段级进度实时可见），
     * 流式不可用（网络/代理不支持）时自动回退普通 POST。
     * 成功/失败都会把结果 appendMessage 写入本地持久化。
     * @param {string} text
     * @param {{signal?:AbortSignal}} [opts]
     */
    async sendMessage(text, opts = {}) {
      const content = typeof text === 'string' ? text.trim() : ''
      if (!content) return
      if (this.loading) return

      this.loading = true
      this.error = null
      this.streamStage = null
      this.streamLabel = null
      this.lastUserInput = content   // F10：供重发按钮复用
      this.appendMessage({ role: 'user', content })

      // 重复提问检测（P2-4 埋点）：与上一条用户消息相同则记录，便于后续迭代发现"澄清效率"问题
      try {
        const prevUser = [...this.messages].reverse().find((m) => m.role === 'user')
        if (prevUser && prevUser.content === content) {
          reportUserEvent('duplicate_question', { text_len: content.length }, { debounceMs: 800 })
        }
      } catch (e) { /* 埋点失败不影响发送 */ }

      // 创建可中断的请求控制器（"停止生成"按钮触发）
      const ctrl = (typeof AbortController !== 'undefined') ? new AbortController() : null
      this.abortController = ctrl
      try {
        const payload = { user_input: content }
        if (this.sessionId) payload.session_id = this.sessionId
        let data = null
        try {
          data = await this._sendMessageStream(payload, ctrl)
        } catch (streamErr) {
          if (ctrl && ctrl.signal && ctrl.signal.aborted) throw streamErr
          // 流式失败（网关不支持 SSE、超时等）→ 回退普通 POST
          console.warn('[agentChat] 流式端点不可用，回退普通请求：', streamErr?.message || streamErr)
          data = await this._sendMessagePlain(payload, ctrl)
        }
        if (data.session_id) this.setSessionId(data.session_id)
        // stage='answer' 时直接把后端生成的自然语言回答作为气泡文本（前端按纯文本渲染）
        const bubbleContent =
          data.natural_reply ||
          (data.stage === 'answer' ? (data.answer_text || '')
          : data.stage === 'plan' ? '已生成调理方案'
          : data.stage === 'refined_plan' ? '已根据你的情况调整方案'
          : data.stage === 'seeded' ? '已锚定问卷测评'
          : data.stage === 'drift_warning' ? '体质可能有变化，建议重测'
          : data.stage === 'no_assessment' ? '请先做体质量表'
          : (data.clarification || '请补充信息'))
        this.appendMessage({
          role: 'assistant',
          content: bubbleContent,
          response: data,
          error: false,
        })
        reportUserEvent('message_sent', {
          stage: data.stage || 'unknown',
          escalate: Boolean(data.escalate),
          rejected: Boolean(data.stage === 'clarify'),
        })
      } catch (err) {
        // 用户主动点"停止"
        if (ctrl && ctrl.signal && ctrl.signal.aborted) {
          this.appendMessage({
            role: 'assistant',
            content: '已停止生成。您可以继续提问或让我重新生成方案。',
            response: null,
            error: false,
          })
          this.error = null
          return
        }
        const e = err && err.response && err.response.data ? err.response.data.error : null
        const msg = (typeof e === 'object' && e ? e.message : e) || (err && err.message) || '请求失败'
        const status = err && err.response ? err.response.status : 0
        let userMsg = msg
        if (status === 401) {
          userMsg = '请先登录后再使用多智能体问诊（右上角或个人中心登录）。'
        } else if (status === 429) {
          userMsg = '请求过于频繁，请稍后再试。'
        }
        this.appendMessage({
          role: 'assistant',
          content: userMsg,
          response: null,
          error: true,
        })
        this.error = { message: userMsg, code: status || (typeof e === 'object' && e && e.code) || 'chat_error' }
        reportUserEvent('message_error', { status, code: this.error.code })
        throw Object.assign(err || new Error(userMsg), { userMessage: userMsg, status })
      } finally {
        this.abortController = null
        this.loading = false
        this.streamStage = null
        this.streamLabel = null
      }
    },

    /** 普通 POST（回退路径）：与原实现等价。 */
    async _sendMessagePlain(payload, ctrl) {
      const config = { signal: ctrl ? ctrl.signal : undefined }
      const res = await axios.post('/api/agents/chat', payload, config)
      return (res && res.data) || {}
    },

    /**
     * SSE 流式路径：POST /api/agents/chat_stream，消费 progress/result/error 事件。
     * EventSource 原生不支持 POST，这里用 fetch + ReadableStream 手工解析 SSE 帧。
     * 返回最终 result 事件 data；服务端/网络错误抛出（由调用方决定回退）。
     */
    async _sendMessageStream(payload, ctrl) {
      const headers = { 'Content-Type': 'application/json', ...( _authHeader() || {}) }
      const res = await fetch('/api/agents/chat_stream', {
        method: 'POST',
        headers,
        body: JSON.stringify(payload),
        signal: ctrl ? ctrl.signal : undefined,
      })
      if (!res.ok || !res.body) {
        let msg = `流式端点响应异常 (${res.status})`
        if (res.status === 401) msg = '请先登录后再使用多智能体问诊。'
        throw new Error(msg)
      }

      const reader = res.body.getReader()
      const decoder = new TextDecoder('utf-8')
      let buffer = ''
      let finalData = null
      let streamError = null

      const _handleEvent = (eventName, dataStr) => {
        let data = null
        try { data = JSON.parse(dataStr) } catch (e) { return }
        if (eventName === 'progress') {
          this.streamStage = data.stage || null
          this.streamLabel = STREAM_LABELS[data.stage] || null
        } else if (eventName === 'result') {
          finalData = data
        } else if (eventName === 'error') {
          streamError = new Error((data && data.message) || 'Agent 对话失败')
        }
      }

      while (true) {
        const { done, value } = await reader.read()
        if (done) break
        buffer += decoder.decode(value, { stream: true })
        // SSE 帧以空行分隔
        let sep
        while ((sep = buffer.indexOf('\n\n')) >= 0) {
          const frame = buffer.slice(0, sep)
          buffer = buffer.slice(sep + 2)
          let eventName = 'message'
          const dataLines = []
          for (const line of frame.split('\n')) {
            if (line.startsWith('event:')) eventName = line.slice(6).trim()
            else if (line.startsWith('data:')) dataLines.push(line.slice(5).trim())
          }
          if (dataLines.length) _handleEvent(eventName, dataLines.join('\n'))
        }
      }

      if (streamError) throw streamError
      if (!finalData) throw new Error('流式响应未返回结果')
      return finalData
    },

    /** 停止当前正在生成的回复（P0-3：可中断）。 */
    stop() {
      if (this.abortController) {
        try { this.abortController.abort() } catch (e) { /* noop */ }
      }
    },

    /** 快速追问预设文本：与 sendMessage 等价，先做基础校验。 */
    async askQuick(presetText) {
      const text = typeof presetText === 'string' ? presetText.trim() : ''
      if (!text) return
      if (!this.sessionId && !this.seed_source) {
        const err = new Error('会话未初始化，请先导入问卷测评或开始一次对话。')
        this.error = { message: err.message, code: 'no_session' }
        throw err
      }
      return this.sendMessage(text)
    },

    /**
     * 自动基于当前用户【最近一次】测评 seed 会话。
     * 进 /agent 页时若本地没有 seed_source 就调一次：
     *   - 成功：自动 seed，用户直接进入问诊
     *   - 从没测过：返回 {need_assessment:true}，前端显示引导卡片
     */
    async seedLatest() {
      if (this.seed_source && this.seed_source.assessment_id) return { seeded: true }
      try {
        const body = {}
        if (this.sessionId) body.session_id = this.sessionId
        const res = await axios.post('/api/agents/seed_latest', body)
        const data = (res && res.data) || {}
        if (data.seeded && data.seed_source) {
          if (data.session_id) this.sessionId = data.session_id
          this.seed_source = { ...data.seed_source, seededAt: Date.now() }
          const ss = this.seed_source
          this.appendMessage({
            role: 'assistant',
            content: `已自动锚定最近一次测评（#${ss.assessment_id} ${ss.primary_name}）`,
            response: {
              stage: 'seeded',
              seed_source: {
                assessment_id: ss.assessment_id,
                primary: ss.primary,
                primary_name: ss.primary_name,
                secondary: ss.secondary || [],
                secondary_names: ss.secondary_names || [],
                scores: ss.scores || null,
                reason: ss.reason || null,
              },
              session_id: this.sessionId,
            },
            error: false,
          })
          _persist(this.$state)
          return { seeded: true }
        }
        return { seeded: false, need_assessment: true, message: data.message || '' }
      } catch (err) {
        console.warn('[agentChat] seed_latest 失败：', err?.message || err)
        return { seeded: false, error: true }
      }
    },

    /**
     * 组件挂载时调用：若本地有 sessionId，先展示本地缓存气泡，
     * 再向 /api/agents/state/:sessionId 请求后端权威状态做一致性兜底。
     * 若后端 state 存在且比本地新，则用后端覆盖（解决 Flask 重启导致的进程内存丢失问题）。
     * 若后端 state 不存在（会话超时/后端重启），仍保留本地气泡作为展示，但继续发送会被视为新会话并生成新 ID。
     */
    async restoreFromBackend() {
      this.restoreStatus = 'pending'
      if (!this.sessionId) {
        this.restoreStatus = 'done'
        return { restored: false, reason: 'no session id' }
      }
      try {
        const res = await axios.get(`/api/agents/state/${encodeURIComponent(this.sessionId)}`)
        const data = res.data || {}
        const backendMsgs = data.chat_messages || []
        // 后端消息数 ≥ 本地：说明后端有更完整（或相等）的状态，以后端为准覆盖
        if (Array.isArray(backendMsgs) && backendMsgs.length >= this.messages.length) {
          this.replaceMessages(backendMsgs)
        }
        this.restoreStatus = 'done'
        return { restored: true, count: this.messages.length, source: 'backend' }
      } catch (err) {
        // 404 = 会话失效（后端重启/TTL过期），仍保留本地气泡给用户查看，只是状态标 failed
        const code = err.response?.data?.error?.code
        if (code === 'not_found') {
          console.info('[agentChat] 后端会话已失效，使用本地气泡作为只读展示')
          this.restoreStatus = 'failed'
          return { restored: true, count: this.messages.length, source: 'local', stale: true }
        }
        // 其它错误（401 / 网络等）：同样回退本地，不抛异常让组件继续渲染
        console.warn('[agentChat] 会话恢复失败：', err?.message || err)
        this.restoreStatus = 'failed'
        return { restored: true, count: this.messages.length, source: 'local', error: true }
      }
    },

    /** F10：失败重发——用上次用户输入重跑一次（错误气泡上的"重发"按钮调用）。 */
    async retryLast() {
      const text = this.lastUserInput
      if (!text || this.loading) return
      // 去掉最后一条错误气泡，再重发
      if (this.messages.length && this.messages[this.messages.length - 1].error) {
        this.messages.pop()
      }
      await this.sendMessage(text)
    },

    /** 重置：清空 store + localStorage，并尝试删除后端会话（失败不影响）。 */
    async reset() {
      const sid = this.sessionId
      this.sessionId = null
      this.messages = []
      this.seed_source = null
      this.restoreStatus = 'idle'
      this.loading = false
      this.error = null
      try {
        localStorage.removeItem(STORAGE_KEY)
      } catch (e) {
        console.warn('[agentChat] 清空本地缓存失败：', e)
      }
      if (sid) {
        try {
          await axios.post('/api/agents/reset', { session_id: sid })
        } catch (e) {
          console.warn('[agentChat] 后端重置失败（已清空本地）：', e)
        }
      }
      reportUserEvent('session_reset', { had_session: Boolean(sid) })
    },
  },
})
