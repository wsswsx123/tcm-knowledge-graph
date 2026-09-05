<!-- frontend/src/views/AgentChat.vue (thin wrapper) -->
<template>
  <AgentChatPanel ref="panelRef" mode="page" @seeded="onSeeded" @error="onError" @session-changed="onSessionChanged" />
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import AgentChatPanel from '@/components/AgentChatPanel.vue'
import { useAgentChatStore } from '@/store/agentChat'

const route = useRoute()
const store = useAgentChatStore()
const panelRef = ref(null)

const onSeeded = (seedSource) => {
  // 可选：页面级埋点 / 其他联动
  console.info('[AgentChat] seeded:', seedSource)
}
const onError = (msg, code) => {
  console.warn('[AgentChat] error:', msg, code)
}
const onSessionChanged = (sid) => {
  console.info('[AgentChat] session changed:', sid)
}

// Bonus：若 URL 带 ?from_assessment=<id>，则自动 seed（如已经 seed 过同 id 则跳过）
onMounted(async () => {
  const fromAssessment = route.query && route.query.from_assessment
  if (!fromAssessment) return
  const id = Number(fromAssessment)
  if (!Number.isFinite(id) || id <= 0) return
  if (store.seed_source && Number(store.seed_source.assessment_id) === id) return
  try {
    await store.seedFromAssessment(id)
  } catch (err) {
    // seed 错误已经写入 store.error，并由 panel 上的 @error 打印；这里静默即可
    const userMsg = (err && err.userMessage) || (err && err.message)
    if (userMsg) onError(userMsg, err && err.status)
  }
})
</script>
