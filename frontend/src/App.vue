<!-- frontend/src/App.vue -->
<template>
  <div class="min-h-screen bg-paper text-ink pb-20">
    <header class="bg-primary text-paper p-4 shadow-md border-b-4 border-secondary sticky top-0 z-40">
      <div class="w-[98%] mx-auto flex justify-between items-center">
        <!-- 左侧：添加动态阴阳鱼装饰 -->
        <div class="flex items-center space-x-3">
          <div class="hidden sm:block w-8 h-8 rounded-full bg-white/20 flex items-center justify-center text-xl animate-pulse">
            ☯
          </div>
          <router-link to="/" class="text-xl md:text-2xl font-serif font-bold tracking-widest hover:text-[#e8dcc4] flex items-center">
            <span class="mr-2 text-2xl md:text-3xl">☯</span>
            <span class="hidden sm:inline">中医体质辨识与养生推荐</span>
            <span class="sm:hidden">中医体质</span>
          </router-link>
        </div>

        <!-- 右侧：轮播格言 + 图谱管理 -->
        <div class="flex items-center space-x-4">
          <div class="hidden lg:block text-sm italic border-l border-paper/30 pl-3">
            <span class="text-paper/90">{{ currentMotto }}</span>
          </div>
          <router-link to="/admin" class="text-sm border border-paper px-4 py-1.5 rounded-full hover:bg-paper hover:text-primary transition-colors">
            图谱管理
          </router-link>
        </div>
      </div>
    </header>

    <!-- 主内容区：宽度 98%，几乎无左右空白 -->
    <main class="w-[98%] mx-auto p-2 md:p-4">
      <router-view />
    </main>

    <BottomNav />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import BottomNav from './components/BottomNav.vue'

const mottos = [
  "上工治未病，不治已病。",
  "春夏养阳，秋冬养阴。",
  "食饮有节，起居有常。",
  "恬淡虚无，真气从之。",
  "正气存内，邪不可干。"
]
const currentMotto = ref(mottos[0])
let mottoIndex = 0
let interval = null

onMounted(() => {
  interval = setInterval(() => {
    mottoIndex = (mottoIndex + 1) % mottos.length
    currentMotto.value = mottos[mottoIndex]
  }, 4000)
})
onUnmounted(() => {
  if (interval) clearInterval(interval)
})
</script>