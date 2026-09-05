import { defineStore } from 'pinia'
import axios from '@/api'

const STORAGE_KEY = 'tcm_agent_chat_v1'

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
      /** 最近一次错误消息；组件可读取后自行清空 */
      error: null,
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
        throw Object.assign(err || new Error(msg), { userMessage: msg, status })
      } finally {
        this.loading = false
      }
    },

    /**
     * 发送一条用户消息（等价原 AgentChat.vue 里的 send() 逻辑）。
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
      this.appendMessage({ role: 'user', content })

      try {
        const payload = { user_input: content }
        if (this.sessionId) payload.session_id = this.sessionId
        const config = opts && opts.signal ? { signal: opts.signal } : undefined
        const res = await axios.post('/api/agents/chat', payload, config)
        const data = (res && res.data) || {}
        if (data.session_id) this.setSessionId(data.session_id)
        this.appendMessage({
          role: 'assistant',
          content: data.stage === 'plan' ? '已生成调理方案' : data.stage === 'seeded' ? '已锚定问卷测评' : (data.clarification || '请补充信息'),
          response: data,
          error: false,
        })
      } catch (err) {
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
        throw Object.assign(err || new Error(userMsg), { userMessage: userMsg, status })
      } finally {
        this.loading = false
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
    },
  },
})
