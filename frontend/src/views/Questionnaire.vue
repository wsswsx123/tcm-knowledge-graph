<!-- frontend/src/views/Questionnaire.vue -->
<template>
  <div class="bg-white rounded-sm shadow-lg p-4 md:p-5 border border-border relative overflow-hidden">
    <!-- 装饰角 -->
    <div class="absolute top-0 left-0 w-10 h-10 border-t-2 border-l-2 border-primary m-2 z-10"></div>
    <div class="absolute top-0 right-0 w-10 h-10 border-t-2 border-r-2 border-primary m-2 z-10"></div>
    <div class="absolute bottom-0 left-0 w-10 h-10 border-b-2 border-l-2 border-primary m-2 z-10"></div>
    <div class="absolute bottom-0 right-0 w-10 h-10 border-b-2 border-r-2 border-primary m-2 z-10"></div>

    <!-- 左侧大装饰（太极图等） -->
    <div class="absolute left-0 top-1/2 -translate-y-1/2 hidden xl:flex flex-col items-center space-y-5 text-primary/20 z-10">
      <span class="text-9xl">☯</span>
      <div class="writing-vertical-rl text-3xl font-serif tracking-widest">中医体质·辨证论治</div>
    </div>

    <!-- 右侧大装饰 -->
    <div class="absolute right-0 top-1/2 -translate-y-1/2 hidden xl:flex flex-col items-center space-y-5 text-primary/20 z-10">
      <span class="text-9xl">❦</span>
      <span class="text-8xl">🧪</span>
      <div class="writing-vertical-rl text-3xl font-serif tracking-widest">望闻问切·天人合一</div>
    </div>

    <!-- 顶部梅花装饰 -->
    <div class="absolute top-4 left-4 text-primary/30 text-6xl hidden md:block z-10">❦</div>
    <div class="absolute top-4 right-4 text-primary/30 text-6xl hidden md:block z-10">❦</div>

    <!-- 标题区 -->
    <h2 class="text-4xl md:text-5xl font-serif font-bold text-secondary mb-3 text-center relative">
      <span class="absolute left-0 top-1/2 -translate-y-1/2 text-primary/20 text-3xl hidden md:inline-block">☯</span>
      体质辨识问卷
      <span class="absolute right-0 top-1/2 -translate-y-1/2 text-primary/20 text-3xl hidden md:inline-block">☯</span>
    </h2>
    <div class="flex items-center justify-center space-x-4 mb-4">
      <div class="h-[1px] w-16 bg-primary"></div>
      <span class="text-primary font-serif text-2xl">❖</span>
      <div class="h-[1px] w-16 bg-primary"></div>
    </div>

    <!-- 中医箴言轮播 -->
    <div class="bg-paper border-l-4 border-primary p-4 mb-6 rounded-r-lg max-w-lg mx-auto">
      <div class="flex items-center justify-center space-x-3">
        <span class="text-primary text-2xl">🍃</span>
        <p class="text-primary font-serif text-base md:text-lg italic">{{ currentSaying }}</p>
        <span class="text-primary text-2xl">🍃</span>
      </div>
    </div>

    <p class="text-[#6b5c51] font-serif text-center text-base md:text-lg mb-5">
      请根据您近一年的体验和感觉，如实回答以下问题。
      <span class="block text-sm md:text-base mt-1 text-primary">点击问题旁的
        <HelpCircle class="w-5 h-5 inline" /> 图标可获取解释</span>
    </p>

    <!-- 问卷类型切换 -->
    <div class="flex justify-center mb-8">
      <div class="inline-flex bg-[#f5f0e6] rounded-full p-1 border border-border">
        <button
          @click="switchType('short')"
          :class="[
            'px-8 py-2 rounded-full font-serif text-base md:text-lg transition-all',
            questionnaireType === 'short'
              ? 'bg-primary text-white shadow-md'
              : 'text-[#6b5c51] hover:text-secondary'
          ]"
        >
          精简版 (36题)
        </button>
        <button
          @click="switchType('full')"
          :class="[
            'px-8 py-2 rounded-full font-serif text-base md:text-lg transition-all',
            questionnaireType === 'full'
              ? 'bg-primary text-white shadow-md'
              : 'text-[#6b5c51] hover:text-secondary'
          ]"
        >
          完整版 (72题)
        </button>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="text-center py-12 text-primary font-serif text-lg">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
      加载问卷中...
    </div>

    <!-- 加载错误提示 -->
    <div v-else-if="loadError" class="text-center py-12 text-red-500 font-serif">
      <p>{{ loadError }}</p>
      <button
        @click="fetchQuestions"
        class="mt-4 bg-primary text-white px-6 py-2 rounded-lg hover:bg-secondary transition-colors"
      >
        重试
      </button>
    </div>

    <!-- 问卷内容 -->
    <template v-else-if="Object.keys(questions).length > 0">
      <div v-for="(qs, ctype, idx) in questions" :key="ctype" class="mb-12">
        <div class="flex items-center mb-5">
          <div class="w-1 h-6 bg-primary mr-3"></div>
          <h3 class="text-2xl md:text-3xl font-serif font-semibold text-secondary">
            {{ getSectionTitle(idx) }}
          </h3>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-x-10 gap-y-8">
          <div v-for="(q, qIdx) in qs" :key="q.id">
            <AIQuestionHelper
              :question="{
                id: q.id,
                content: q.content,
                constitution_type: ctype,
                constitution_name: constitutionNames[ctype]
              }"
              :model-value="answers[ctype]?.[qIdx]"
              @update:model-value="setAnswer(ctype, qIdx, $event)"
              @need-followup="checkFollowup"
            />
          </div>
        </div>
      </div>

      <!-- 底部进度和提交 -->
      <div class="mt-14 text-center">
        <div class="max-w-md mx-auto mb-6">
          <div class="flex justify-between text-base text-primary mb-1">
            <span>答题进度</span>
            <span>{{ progress }}%</span>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-2">
            <div
              class="bg-primary rounded-full h-2 transition-all duration-300"
              :style="{ width: progress + '%' }"
            ></div>
          </div>
        </div>

        <div v-if="errorMsg" class="mb-6 p-4 bg-red-50 border border-red-200 text-red-600 rounded-sm font-serif inline-block">
          {{ errorMsg }}
        </div>

        <!-- AI追问区域 -->
        <div v-if="Array.isArray(followupQuestions) && followupQuestions.length > 0" class="mb-6 p-6 bg-amber-50 rounded-lg border border-amber-200">
          <h4 class="text-xl font-serif font-bold text-amber-800 mb-4 flex items-center">
            <Sparkles class="w-6 h-6 mr-2" /> 为了更好地判断，请再回答几个问题
          </h4>
          <div v-for="(q, index) in followupQuestions" :key="index" class="mb-4">
            <p class="font-serif text-gray-700 text-base mb-2">{{ q }}</p>
            <div class="flex gap-2">
              <button
                v-for="val in 5"
                :key="val"
                @click="answerFollowup(index, val)"
                :class="[
                  'px-4 py-2 rounded-full text-base md:text-lg border transition-all',
                  followupAnswers[index] === val
                    ? 'bg-amber-600 text-white border-amber-600'
                    : 'bg-white text-gray-600 border-gray-300 hover:bg-amber-50'
                ]"
              >
                {{ ['没有','很少','有时','经常','总是'][val-1] }}
              </button>
            </div>
          </div>
          <button
            @click="submitFollowup"
            :disabled="!canSubmitFollowup"
            class="mt-4 bg-amber-600 text-white px-6 py-2 rounded-lg hover:bg-amber-700 disabled:opacity-50 text-base"
          >
            提交补充回答
          </button>
        </div>

        <!-- 提交按钮 -->
        <button
          @click="submit"
          :disabled="submitting || !isComplete"
          :class="[
            'font-serif text-xl md:text-2xl py-3 px-12 rounded-sm shadow-lg transition-all border-2',
            submitting || !isComplete
              ? 'bg-[#c0b298] text-white border-[#c0b298] cursor-not-allowed'
              : 'bg-secondary hover:bg-[#3e3a39] text-paper hover:shadow-xl border-primary hover:border-secondary'
          ]"
        >
          {{ submitting ? '提交中...' : '提交辨识' }}
        </button>
      </div>
    </template>

    <div v-else class="text-center py-12 text-[#c0b298] font-serif text-lg">
      暂无问卷数据，请稍后再试或联系管理员。
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store'
import { HelpCircle, Sparkles } from 'lucide-vue-next'
import axios from '@/api'
import AIQuestionHelper from '@/components/AIQuestionHelper.vue'

const router = useRouter()
const userStore = useUserStore()

const questions = ref({})
const answers = ref({})
const loading = ref(true)
const loadError = ref('')
const submitting = ref(false)
const errorMsg = ref('')
const questionnaireType = ref('short')

const followupQuestions = ref([])
const followupAnswers = ref([])
const currentSessionId = ref('')

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

const constitutionNames = {
  pinghe: '平和质', qixu: '气虚质', yangxu: '阳虚质', yinxu: '阴虚质',
  tanshi: '痰湿质', shire: '湿热质', xueyu: '血瘀质', qiyu: '气郁质', tebing: '特禀质'
}

// 生成通用分组标题，避免直接显示体质类型名称
const getSectionTitle = (index) => {
  // 使用序号，格式为“第X部分”
  return `第${index + 1}部分`
}

const totalQuestions = computed(() => {
  let total = 0
  for (const ctype in questions.value) {
    total += questions.value[ctype].length
  }
  return total
})

const answeredCount = computed(() => {
  let count = 0
  for (const ctype in answers.value) {
    count += answers.value[ctype].filter(v => v > 0).length
  }
  return count
})

const progress = computed(() => {
  if (totalQuestions.value === 0) return 0
  return Math.round((answeredCount.value / totalQuestions.value) * 100)
})

const isComplete = computed(() => {
  for (const ctype in answers.value) {
    if (answers.value[ctype].includes(0)) return false
  }
  return true
})

const canSubmitFollowup = computed(() => {
  return followupAnswers.value.every(v => v > 0)
})

onMounted(async () => {
  await fetchQuestions()
  currentSessionId.value = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9)
  sayingInterval = setInterval(() => {
    sayingIndex.value = (sayingIndex.value + 1) % sayings.length
  }, 5000)
})

onUnmounted(() => {
  if (sayingInterval) clearInterval(sayingInterval)
})

const fetchQuestions = async () => {
  loading.value = true
  loadError.value = ''
  try {
    const res = await axios.get(`/api/questions?type=${questionnaireType.value}`)
    if (res.data && typeof res.data === 'object') {
      questions.value = res.data
      const init = {}
      for (const ctype in res.data) {
        if (Array.isArray(res.data[ctype])) {
          init[ctype] = Array(res.data[ctype].length).fill(0)
        }
      }
      answers.value = init
    } else {
      throw new Error('返回数据格式不正确')
    }
  } catch (error) {
    console.error('获取问卷失败:', error)
    loadError.value = error.response?.data?.error || '问卷加载失败，请检查网络连接或稍后重试。'
  } finally {
    loading.value = false
  }
}

const switchType = (type) => {
  questionnaireType.value = type
  fetchQuestions()
}

const setAnswer = async (ctype, idx, val) => {
  answers.value[ctype][idx] = val

  try {
    const question = questions.value[ctype][idx]
    await axios.post('/api/assessment/save-answer', {
      userId: userStore.user?.id,
      sessionId: currentSessionId.value,
      questionId: question.id,
      questionContent: question.content,
      constitutionType: ctype,
      answerValue: val,
      isFollowup: false
    })

    if (answeredCount.value > 0 && answeredCount.value % 8 === 0) {
      await checkFollowup()
    }
  } catch (error) {
    console.error('保存答案失败:', error)
  }
}

const checkFollowup = async () => {
  try {
    const res = await axios.post('/api/ai/check-followup', {
      session_id: currentSessionId.value,
      user_id: userStore.user?.id
    })
    const followups = res.data.followups
    if (Array.isArray(followups) && followups.length > 0) {
      followupQuestions.value = followups
      followupAnswers.value = Array(followups.length).fill(0)
    } else {
      followupQuestions.value = []
      followupAnswers.value = []
    }
  } catch (error) {
    console.error('检查追问失败:', error)
    followupQuestions.value = []
    followupAnswers.value = []
  }
}

const answerFollowup = (index, val) => {
  followupAnswers.value[index] = val
}

const submitFollowup = async () => {
  try {
    for (let i = 0; i < followupQuestions.value.length; i++) {
      await axios.post('/api/assessment/save-answer', {
        userId: userStore.user?.id,
        sessionId: currentSessionId.value,
        questionContent: followupQuestions.value[i],
        answerValue: followupAnswers.value[i],
        isFollowup: true
      })
    }
    followupQuestions.value = []
    followupAnswers.value = []
    await checkFollowup()
  } catch (error) {
    console.error('提交追问失败:', error)
  }
}

const submit = async () => {
  if (!isComplete.value) {
    errorMsg.value = '请回答所有问题后再提交！'
    return
  }

  submitting.value = true
  try {
    const res = await axios.post('/api/assessment/submit', {
      answers: answers.value,
      userId: userStore.user?.id,
      sessionId: currentSessionId.value
    })
    router.push(`/result/${res.data.id}`)
  } catch (err) {
    errorMsg.value = '提交失败，请重试。'
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.writing-vertical-rl {
  writing-mode: vertical-rl;
  text-orientation: mixed;
}
</style>