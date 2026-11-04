<template>
  <div class="space-y-8 pb-20">
    <!-- 医疗免责声明（合规） -->
    <MedicalDisclaimer />
    <!-- 未登录状态 -->
    <div v-if="!userStore.user" class="bg-white rounded-sm shadow-lg p-12 border border-border text-center mt-10">
      <h2 class="text-3xl font-serif font-bold text-secondary mb-6 tracking-widest">调理方案推荐</h2>
      <p class="text-primary font-serif text-lg mb-8">请先登录以获取您的专属调理方案</p>
      <router-link to="/auth" class="inline-block bg-primary text-white px-8 py-3 rounded-sm font-serif text-lg hover:bg-secondary">
        去登录
      </router-link>
    </div>

    <!-- 加载状态 -->
    <div v-else-if="loading" class="text-center py-20 text-primary">正在为您生成专属方案...</div>

    <!-- 无结果状态 -->
    <div v-else-if="!latestResult" class="bg-white rounded-sm shadow-lg p-12 border border-border text-center mt-10">
      <h2 class="text-3xl font-serif font-bold text-secondary mb-6 tracking-widest">调理方案推荐</h2>
      <p class="text-primary font-serif text-lg mb-8">您还没有进行过体质辨识，暂时无法生成方案</p>
      <router-link to="/" class="inline-block bg-primary text-white px-8 py-3 rounded-sm font-serif text-lg hover:bg-secondary">
        开始辨识
      </router-link>
    </div>

    <!-- 有结果状态 -->
    <div v-else class="bg-white rounded-sm shadow-lg p-8 md:p-10 border border-border relative overflow-hidden">
      <div class="absolute top-0 right-0 opacity-5 text-9xl font-serif -mt-10 -mr-10 pointer-events-none text-primary">
        养
      </div>

      <h2 class="text-3xl font-serif font-bold text-secondary mb-4 tracking-widest text-center">专属调理方案</h2>
      <div class="flex items-center justify-center space-x-4 mb-6">
        <div class="h-[1px] w-12 bg-primary"></div>
        <span class="text-primary font-serif">❖</span>
        <div class="h-[1px] w-12 bg-primary"></div>
      </div>

      <!-- 中医格言轮播 -->
      <div class="bg-paper border-l-4 border-primary p-3 mb-8 rounded-r-lg max-w-md mx-auto">
        <div class="flex items-center justify-center space-x-2">
          <span class="text-primary text-lg">🍃</span>
          <p class="text-primary font-serif text-sm italic">{{ currentSaying }}</p>
          <span class="text-primary text-lg">🍃</span>
        </div>
      </div>

      <!-- 基于您最近一次的辨识结果 -->
      <div class="text-center mb-10">
        <p class="text-[#6b5c51] font-serif text-lg mb-6">基于您最近一次的辨识结果：</p>

        <div class="grid md:grid-cols-2 gap-6 max-w-5xl mx-auto">
          <!-- 主体质卡片 -->
          <div class="bg-gradient-to-br from-primary/15 to-paper rounded-xl p-6 border border-primary/40 shadow-lg">
            <div class="flex items-center justify-between mb-3">
              <span class="text-sm font-serif text-primary/80">主体质 · 得分最高</span>
              <span class="bg-primary text-white text-xs px-3 py-1 rounded-full">★ 重点关注</span>
            </div>
            <div class="text-4xl font-serif font-bold text-primary mb-2">{{ topTwo[0]?.name || '无数据' }}</div>
            <div class="flex items-baseline gap-2 mb-2">
              <span class="text-5xl font-black text-secondary">{{ topTwo[0]?.score || 0 }}%</span>
              <span class="text-base text-gray-500">转化分</span>
            </div>
            <div class="mt-3 w-full bg-gray-200 rounded-full h-3">
              <div class="bg-primary rounded-full h-3" :style="{ width: (topTwo[0]?.score || 0) + '%' }"></div>
            </div>
            <p class="text-sm text-gray-600 mt-3">{{ topTwo[0]?.score > 0 ? '偏颇程度较高，建议优先调理' : '暂无有效测评数据' }}</p>
          </div>

          <!-- 第二体质卡片 -->
          <div v-if="topTwo[1] && topTwo[1].score > 0" class="bg-gradient-to-br from-amber-50 to-paper rounded-xl p-6 border border-amber-200 shadow-lg">
            <div class="flex items-center justify-between mb-3">
              <span class="text-sm font-serif text-primary/80">兼夹倾向 · 得分第二</span>
              <span class="bg-amber-100 text-amber-700 text-xs px-3 py-1 rounded-full">⚡ 需留意</span>
            </div>
            <div class="text-4xl font-serif font-bold text-secondary mb-2">{{ topTwo[1].name }}</div>
            <div class="flex items-baseline gap-2 mb-2">
              <span class="text-5xl font-black text-amber-700">{{ topTwo[1].score }}%</span>
              <span class="text-base text-gray-500">转化分</span>
            </div>
            <div class="mt-3 w-full bg-gray-200 rounded-full h-3">
              <div class="bg-amber-500 rounded-full h-3" :style="{ width: topTwo[1].score + '%' }"></div>
            </div>
            <p class="text-sm text-gray-600 mt-3">已有倾向，及早干预可防偏颇</p>
          </div>

          <!-- 无第二体质时显示健康提示 -->
          <div v-else class="bg-paper rounded-xl p-6 border border-dashed border-primary/40 flex flex-col items-center justify-center text-[#c0b298] font-serif shadow-sm">
            <span class="text-5xl mb-3">🌸</span>
            <span class="text-lg">其他体质倾向不明显</span>
            <span class="text-sm mt-2">继续保持良好生活习惯，定期测评</span>
            <div class="mt-3 w-full bg-gray-200 rounded-full h-2">
              <div class="bg-green-500 rounded-full h-2" style="width: 80%"></div>
            </div>
            <span class="text-xs mt-2 text-gray-500">平和质倾向良好</span>
          </div>
        </div>

        <div class="mt-8">
          <router-link :to="`/result/${latestResult.id}`" class="inline-flex items-center text-primary hover:text-secondary font-serif border-b border-primary/30 pb-1 transition-all text-lg">
            查看完整报告 <ArrowRight class="w-5 h-5 ml-1" />
          </router-link>
        </div>
      </div>

      <!-- 主体质的调理方案 -->
      <div v-if="recommendations && topTwo[0]?.score > 0" class="mt-8">
        <h3 class="text-2xl font-serif font-bold text-secondary mb-6 text-center border-b-2 border-border pb-3">
          针对【{{ topTwo[0].name }}】的调理方案
        </h3>
        <div class="grid md:grid-cols-3 gap-8">
          <div>
            <h4 class="text-xl font-serif font-bold text-primary mb-6 flex items-center border-b-2 border-border pb-3">
              <Wind class="w-6 h-6 mr-3" /> 经络穴位调理
            </h4>
            <div class="space-y-5">
              <div v-for="(a,i) in recommendations.acupoints" :key="i" class="bg-paper rounded-sm p-5 border-l-4 border-[#b8860b] shadow-sm">
                <p class="font-serif font-bold text-secondary text-xl mb-2">{{ a.name }}</p>
                <p class="text-base text-[#6b5c51] mb-1 font-serif"><span class="font-semibold text-primary">【取穴】</span>{{ a.location }}</p>
                <p class="text-base text-[#6b5c51] mb-1 font-serif"><span class="font-semibold text-primary">【方法】</span>{{ a.method }}</p>
                <p v-if="a.reason" class="text-sm text-amber-700 mt-2 bg-amber-50 p-2 rounded">
                  <span class="font-semibold">✨ 小贴士：</span>{{ a.reason }}
                </p>
              </div>
              <p v-if="!recommendations.acupoints?.length" class="text-[#c0b298] italic font-serif">暂无穴位推荐</p>
            </div>
          </div>
          <div>
            <h4 class="text-xl font-serif font-bold text-primary mb-6 flex items-center border-b-2 border-border pb-3">
              <Apple class="w-6 h-6 mr-3" /> 药膳食疗推荐
            </h4>
            <div class="space-y-5">
              <div v-for="(f,i) in recommendations.foods" :key="i" class="bg-paper rounded-sm p-5 border-l-4 border-[#556b2f] shadow-sm">
                <p class="font-serif font-bold text-secondary text-xl mb-2">{{ f.name }}</p>
                <p class="text-base text-[#6b5c51] mb-1 font-serif"><span class="font-semibold text-primary">【性味】</span>{{ f.nature }}</p>
                <p class="text-base text-[#6b5c51] mb-1 font-serif"><span class="font-semibold text-primary">【功效】</span>{{ f.effect }}</p>
                <p v-if="f.reason" class="text-sm text-amber-700 mt-2 bg-amber-50 p-2 rounded">
                  <span class="font-semibold">✨ 小贴士：</span>{{ f.reason }}
                </p>
              </div>
              <p v-if="!recommendations.foods?.length" class="text-[#c0b298] italic font-serif">暂无食疗推荐</p>
            </div>
          </div>
          <div>
            <h4 class="text-xl font-serif font-bold text-primary mb-6 flex items-center border-b-2 border-border pb-3">
              <Activity class="w-6 h-6 mr-3" /> 运动方案推荐
            </h4>
            <div class="space-y-5">
              <div v-for="(e,i) in recommendations.exercises" :key="i" class="bg-paper rounded-sm p-5 border-l-4 border-[#4682b4] shadow-sm">
                <p class="font-serif font-bold text-secondary text-xl mb-2">{{ e.name }}</p>
                <p class="text-base text-[#6b5c51] mb-1 font-serif"><span class="font-semibold text-primary">【功效】</span>{{ e.effect }}</p>
                <p class="text-base text-[#6b5c51] mb-1 font-serif"><span class="font-semibold text-primary">【方法】</span>{{ e.method }}</p>
                <p v-if="e.reason" class="text-sm text-amber-700 mt-2 bg-amber-50 p-2 rounded">
                  <span class="font-semibold">✨ 小贴士：</span>{{ e.reason }}
                </p>
              </div>
              <p v-if="!recommendations.exercises?.length" class="text-[#c0b298] italic font-serif">暂无运动推荐</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 第二体质的简短建议 -->
      <div v-if="topTwo[1] && topTwo[1].score > 0 && secondRecs" class="mt-12 pt-8 border-t border-border">
        <h3 class="text-xl font-serif font-bold text-secondary mb-4 text-center">针对【{{ topTwo[1].name }}】的调理建议</h3>
        <div class="grid md:grid-cols-3 gap-6">
          <div v-if="secondRecs.acupoints?.length" class="bg-paper p-4 rounded-lg">
            <h4 class="font-serif font-semibold text-primary mb-2">穴位推荐</h4>
            <ul class="text-sm space-y-1">
              <li v-for="a in secondRecs.acupoints.slice(0,2)" :key="a.name">{{ a.name }}：{{ a.location }}</li>
            </ul>
          </div>
          <div v-if="secondRecs.foods?.length" class="bg-paper p-4 rounded-lg">
            <h4 class="font-serif font-semibold text-primary mb-2">食疗推荐</h4>
            <ul class="text-sm space-y-1">
              <li v-for="f in secondRecs.foods.slice(0,2)" :key="f.name">{{ f.name }}：{{ f.effect }}</li>
            </ul>
          </div>
          <div v-if="secondRecs.exercises?.length" class="bg-paper p-4 rounded-lg">
            <h4 class="font-serif font-semibold text-primary mb-2">运动推荐</h4>
            <ul class="text-sm space-y-1">
              <li v-for="e in secondRecs.exercises.slice(0,2)" :key="e.name">{{ e.name }}：{{ e.method }}</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- ==================== 新增：个性化养生计划按钮和展示 ==================== -->
      <div class="mt-12 pt-8 border-t border-border text-center">
        <button
          @click="generateWellnessPlan"
          :disabled="planLoading"
          class="bg-gradient-to-r from-primary to-secondary text-white px-8 py-3 rounded-full font-serif text-lg shadow-lg hover:shadow-xl transition-all disabled:opacity-50"
        >
          <Sparkles class="inline w-5 h-5 mr-2" />
          {{ planLoading ? '生成中...' : '✨ 生成我的养生计划' }}
        </button>

        <!-- 养生计划展示区域 -->
        <div v-if="wellnessPlan" class="mt-8 text-left bg-paper rounded-xl p-6 border border-primary/30 shadow-inner">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-2xl font-serif font-bold text-secondary">🌸 您的个性化养生计划</h3>
            <button @click="wellnessPlan = ''" class="text-primary hover:text-secondary text-sm">收起</button>
          </div>
          <div class="prose prose-amber max-w-none" v-html="renderedPlan"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, onUnmounted } from 'vue'
import { useUserStore } from '@/store'
import { ArrowRight, Wind, Apple, Activity, Sparkles } from 'lucide-vue-next'
import axios from '@/api'
import MedicalDisclaimer from '@/components/MedicalDisclaimer.vue'
import { marked } from 'marked'   // 需要安装: npm install marked

const userStore = useUserStore()
const latestResult = ref(null)
const recommendations = ref(null)
const secondRecs = ref(null)
const loading = ref(true)
const planLoading = ref(false)
const wellnessPlan = ref('')

const constitutionNames = {
  pinghe: '平和质', qixu: '气虚质', yangxu: '阳虚质', yinxu: '阴虚质',
  tanshi: '痰湿质', shire: '湿热质', xueyu: '血瘀质', qiyu: '气郁质', tebing: '特禀质'
}

const sayings = [
  "上工治未病，不治已病。",
  "春夏养阳，秋冬养阴。",
  "食饮有节，起居有常。",
  "恬淡虚无，真气从之。",
  "正气存内，邪不可干。"
]
const sayingIndex = ref(0)
const currentSaying = computed(() => sayings[sayingIndex.value])
let sayingInterval = null

const topTwo = computed(() => {
  if (!latestResult.value || !latestResult.value.scores) {
    return [{ name: '暂无数据', score: 0 }, null]
  }
  const scores = latestResult.value.scores
  const entries = Object.entries(scores)
    .map(([type, score]) => ({
      name: constitutionNames[type] || type,
      score: Math.round(score),
      type
    }))
    .sort((a, b) => b.score - a.score)
  const first = entries[0] || { name: '无数据', score: 0 }
  const second = entries[1] && entries[1].score > 0 ? entries[1] : null
  return [first, second]
})

const renderedPlan = computed(() => {
  if (!wellnessPlan.value) return ''
  return marked.parse(wellnessPlan.value)
})

const fetchSecondRecommendations = async (type) => {
  if (!type) return
  try {
    const res = await axios.get(`/api/recommend/${type}`)
    secondRecs.value = res.data
  } catch (err) {
    console.error(`获取${type}推荐失败:`, err)
    secondRecs.value = null
  }
}

const generateWellnessPlan = async () => {
  if (!latestResult.value) return
  planLoading.value = true
  try {
    const res = await axios.post('/api/ai/generate-wellness-plan', {
      result_id: latestResult.value.id
    })
    wellnessPlan.value = res.data.plan
  } catch (error) {
    console.error('生成养生计划失败:', error)
    alert('生成失败，请稍后再试')
  } finally {
    planLoading.value = false
  }
}

onMounted(async () => {
  sayingInterval = setInterval(() => {
    sayingIndex.value = (sayingIndex.value + 1) % sayings.length
  }, 5000)

  if (!userStore.user) {
    loading.value = false
    return
  }
  try {
    const resHistory = await axios.get(`/api/user/${userStore.user.id}/history`)
    if (resHistory.data.length) {
      const latestHistory = resHistory.data[0]
      const resDetail = await axios.get(`/api/assessment/${latestHistory.id}`)
      latestResult.value = resDetail.data

      if (resDetail.data.enhanced_recommendations) {
        recommendations.value = resDetail.data.enhanced_recommendations
      } else if (resDetail.data.primary) {
        const resRec = await axios.get(`/api/recommend/${resDetail.data.primary}`)
        recommendations.value = resRec.data
      }

      const second = topTwo.value[1]
      if (second && second.type) {
        await fetchSecondRecommendations(second.type)
      }
    }
  } catch (error) {
    console.error('获取推荐失败:', error)
  } finally {
    loading.value = false
  }
})

onUnmounted(() => {
  if (sayingInterval) clearInterval(sayingInterval)
})
</script>

<style scoped>
/* 确保 Markdown 渲染的样式 */
.prose p {
  margin-bottom: 0.75rem;
}
.prose ul, .prose ol {
  margin-left: 1.5rem;
  margin-bottom: 0.75rem;
}
.prose li {
  margin-bottom: 0.25rem;
}
.prose h1, .prose h2, .prose h3, .prose h4 {
  margin-top: 1rem;
  margin-bottom: 0.5rem;
  font-weight: bold;
}
.prose h3 {
  font-size: 1.25rem;
}
</style>