<template>
  <div class="bg-white rounded-sm shadow-lg p-6 md:p-10 border border-border h-[80vh] relative">
    <div class="absolute top-0 left-0 w-8 h-8 border-t-2 border-l-2 border-primary m-2"></div>
    <div class="absolute top-0 right-0 w-8 h-8 border-t-2 border-r-2 border-primary m-2"></div>
    <div class="absolute bottom-0 left-0 w-8 h-8 border-b-2 border-l-2 border-primary m-2"></div>
    <div class="absolute bottom-0 right-0 w-8 h-8 border-b-2 border-r-2 border-primary m-2"></div>

    <GraphChart v-if="graphData" :data="graphData" style="height: 100%; width: 100%;" />

    <div v-else-if="!error" class="h-full flex flex-col items-center justify-center text-[#c0b298] font-serif">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mb-4"></div>
      <p>图谱加载中...</p>
    </div>

    <div v-if="error" class="absolute inset-0 flex items-center justify-center bg-white/80 z-10">
      <div class="text-center text-red-500">
        <p>{{ error }}</p>
        <button @click="fetchGraph" class="mt-4 px-4 py-2 bg-primary text-white rounded-sm hover:bg-secondary">重试</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import GraphChart from '@/components/GraphChart.vue'
import axios from 'axios'

const graphData = ref(null)
const error = ref(null)

const fetchGraph = async () => {
  try {
    error.value = null
    const res = await axios.get('/api/graph')
    graphData.value = res.data
    if (!res.data.nodes || res.data.nodes.length === 0) {
      console.warn('图谱数据为空')
    }
  } catch (err) {
    console.error('图谱加载失败:', err)
    error.value = err.response?.data?.error || '图谱加载失败，请稍后重试。'
  }
}

onMounted(() => {
  fetchGraph()
})
</script>
