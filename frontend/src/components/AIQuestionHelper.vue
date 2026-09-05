<!-- frontend/src/components/AIQuestionHelper.vue -->
<template>
  <div class="relative">
    <div class="flex items-start justify-between">
      <label class="block text-base md:text-lg font-medium text-gray-700 mb-2">
        {{ question.content }}
        <span v-if="question.required" class="text-red-500 ml-1">*</span>
      </label>
      <button
        v-if="showHelpButton"
        @click="toggleExplanation"
        class="ml-2 text-primary hover:text-secondary transition-colors focus:outline-none"
        :disabled="loading"
      >
        <HelpCircle class="w-5 h-5 md:w-6 md:h-6" :class="{ 'animate-pulse': loading }" />
      </button>
    </div>

    <!-- 选项按钮 -->
    <div class="grid grid-cols-5 gap-2 mt-2">
      <button
        v-for="option in options"
        :key="option.value"
        @click="selectOption(option.value)"
        :class="[
          'px-3 py-2 md:px-4 md:py-2 font-serif rounded-full border transition-all text-base md:text-lg',
          selectedValue === option.value
            ? 'bg-primary text-white border-primary shadow-md'
            : 'bg-white text-[#6b5c51] border-[#c0b298] hover:bg-[#f5f0e6] hover:border-primary'
        ]"
      >
        {{ option.label }}
      </button>
    </div>

    <!-- AI解释浮层 -->
    <Transition
      enter-active-class="transition ease-out duration-200"
      enter-from-class="opacity-0 translate-y-1"
      enter-to-class="opacity-100 translate-y-0"
      leave-active-class="transition ease-in duration-150"
      leave-from-class="opacity-100 translate-y-0"
      leave-to-class="opacity-0 translate-y-1"
    >
      <div
        v-if="showExplanation"
        class="absolute z-20 mt-2 w-80 md:w-96 bg-amber-50 rounded-lg shadow-lg border-l-4 border-amber-500 p-4"
        style="right: 0;"
      >
        <div class="flex items-start">
          <Sparkles class="w-5 h-5 text-amber-600 mr-2 flex-shrink-0 mt-0.5" />
          <div>
            <p class="text-sm md:text-base text-gray-800">{{ explanation }}</p>
            <div v-if="example" class="mt-2 text-xs md:text-sm text-gray-600 bg-white/50 p-2 rounded">
              💡 例如：{{ example }}
            </div>
            <div class="mt-3 flex justify-end space-x-2">
              <button
                v-if="!understood"
                @click="markUnderstood"
                class="text-xs md:text-sm bg-amber-600 text-white px-3 py-1 rounded-full hover:bg-amber-700"
              >
                明白了
              </button>
              <button
                @click="askMore"
                class="text-xs md:text-sm text-amber-700 hover:text-amber-900"
              >
                还是不太明白
              </button>
            </div>
          </div>
        </div>

        <div v-if="askingMore" class="mt-3 pt-3 border-t border-amber-200">
          <p class="text-xs md:text-sm text-gray-600 mb-2">您具体哪里不明白？</p>
          <input
            v-model="userQuestion"
            type="text"
            placeholder="输入您的问题..."
            class="w-full px-3 py-2 text-sm md:text-base border border-amber-200 rounded-lg focus:outline-none focus:border-amber-400"
            @keyup.enter="submitQuestion"
          />
          <button
            @click="submitQuestion"
            class="mt-2 text-xs md:text-sm bg-white text-amber-700 px-3 py-1 rounded-full border border-amber-300 hover:bg-amber-50"
          >
            发送
          </button>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { HelpCircle, Sparkles } from 'lucide-vue-next'
import axios from 'axios'

const props = defineProps({
  question: { type: Object, required: true },
  modelValue: { type: Number, default: 0 },
  model: { type: String, default: 'qwen' }   // 接收父组件传递的模型选择
})

const emit = defineEmits(['update:modelValue', 'need-followup'])

const options = [
  { value: 1, label: '没有' },
  { value: 2, label: '很少' },
  { value: 3, label: '有时' },
  { value: 4, label: '经常' },
  { value: 5, label: '总是' }
]

const selectedValue = ref(props.modelValue)
const showExplanation = ref(false)
const explanation = ref('')
const example = ref('')
const loading = ref(false)
const understood = ref(false)
const askingMore = ref(false)
const userQuestion = ref('')
const showHelpButton = ref(true)

const selectOption = (value) => {
  selectedValue.value = value
  emit('update:modelValue', value)
}

const toggleExplanation = async () => {
  if (showExplanation.value) {
    showExplanation.value = false
    return
  }
  showExplanation.value = true
  if (!explanation.value) {
    loading.value = true
    try {
      const res = await axios.post('/api/ai/explain-question', {
        question_id: props.question.id,
        model: props.model   // 传递模型选择
      })
      explanation.value = res.data.explanation
      if (explanation.value.includes('例如')) {
        const parts = explanation.value.split('例如')
        explanation.value = parts[0].trim()
        example.value = parts[1]?.split('。')[0] + '。'
      }
    } catch (error) {
      explanation.value = '暂时无法获取解释，请稍后再试。'
    } finally {
      loading.value = false
    }
  }
}

const markUnderstood = () => {
  understood.value = true
  showExplanation.value = false
}

const askMore = () => {
  askingMore.value = true
}

const submitQuestion = async () => {
  if (!userQuestion.value.trim()) return
  loading.value = true
  try {
    const res = await axios.post('/api/ai/followup-question', {
      question_id: props.question.id,
      user_query: userQuestion.value,
      original_explanation: explanation.value,
      model: props.model   // 传递模型选择
    })
    explanation.value = res.data.answer
    example.value = ''
    userQuestion.value = ''
    askingMore.value = false
  } catch (error) {
    explanation.value = '抱歉，我现在无法回答，请稍后再试。'
  } finally {
    loading.value = false
  }
}

watch(() => props.modelValue, (newVal) => {
  if (newVal !== selectedValue.value) {
    selectedValue.value = newVal
  }
})
</script>