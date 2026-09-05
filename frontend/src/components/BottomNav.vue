<!-- frontend/src/components/BottomNav.vue -->
<template>
  <div class="fixed bottom-0 left-0 right-0 bg-paper border-t-2 border-border shadow-lg z-50" v-if="show">
    <div class="max-w-4xl mx-auto flex justify-between items-center h-16 px-6">
      <router-link
        v-for="item in items"
        :key="item.path"
        :to="item.path"
        class="flex flex-col items-center justify-center transition-colors"
        :class="[isActive(item.path) ? 'text-red-800' : 'text-primary hover:text-secondary']"
      >
        <component :is="item.icon" class="w-6 h-6" />
        <span class="text-xs font-serif mt-1">{{ item.label }}</span>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { ClipboardList, Leaf, Network, User, Bot } from 'lucide-vue-next'

const route = useRoute()
const show = computed(() => !['/admin', '/result'].some(p => route.path.startsWith(p)))

const items = [
  { path: '/', label: '体质辨识', icon: ClipboardList },
  { path: '/agent', label: '问诊', icon: Bot },
  { path: '/recommendation', label: '调理方案', icon: Leaf },
  { path: '/graph', label: '知识图谱', icon: Network },
  { path: '/profile', label: '我的', icon: User },
]

const isActive = (path) => {
  if (path === '/profile') return route.path.startsWith('/auth') || route.path === '/profile'
  return route.path === path
}
</script>