<template>
  <div class="bg-paper rounded-sm shadow-lg p-8 md:p-12 border border-border max-w-md mx-auto mt-10 relative">
    <div class="absolute top-0 left-0 w-8 h-8 border-t-2 border-l-2 border-primary m-2"></div>
    <div class="absolute top-0 right-0 w-8 h-8 border-t-2 border-r-2 border-primary m-2"></div>
    <div class="absolute bottom-0 left-0 w-8 h-8 border-b-2 border-l-2 border-primary m-2"></div>
    <div class="absolute bottom-0 right-0 w-8 h-8 border-b-2 border-r-2 border-primary m-2"></div>

    <h2 class="text-3xl font-serif font-bold text-secondary mb-4 text-center tracking-widest">
      {{ isLogin ? '用户登录' : '用户注册' }}
    </h2>
    <div class="flex items-center justify-center space-x-4 mb-8">
      <div class="h-[1px] w-12 bg-primary"></div>
      <span class="text-primary font-serif">❖</span>
      <div class="h-[1px] w-12 bg-primary"></div>
    </div>

    <div v-if="error" class="bg-red-50 text-red-700 p-3 rounded-sm mb-6 text-center font-serif border border-red-200">
      {{ error }}
    </div>

    <form @submit.prevent="handleSubmit" class="space-y-6">
      <div>
        <label class="block text-secondary font-serif mb-2">用户名</label>
        <input
          v-model="username"
          type="text"
          class="w-full p-3 bg-white border border-[#c0b298] rounded-sm focus:outline-none focus:border-primary font-serif"
          required
        />
      </div>
      <div>
        <label class="block text-secondary font-serif mb-2">密码</label>
        <input
          v-model="password"
          type="password"
          class="w-full p-3 bg-white border border-[#c0b298] rounded-sm focus:outline-none focus:border-primary font-serif"
          required
        />
      </div>
      <button
        type="submit"
        class="w-full bg-primary hover:bg-secondary text-white font-serif text-lg py-3 rounded-sm transition-colors tracking-widest"
      >
        {{ isLogin ? '登 录' : '注 册' }}
      </button>
    </form>

    <div class="mt-6 text-center">
      <button @click="isLogin = !isLogin" class="text-primary hover:text-secondary font-serif underline">
        {{ isLogin ? '没有账号？点击注册' : '已有账号？点击登录' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import {ref} from 'vue'
import {useUserStore} from '@/store'
import {useRouter} from 'vue-router'
import axios from 'axios'

const isLogin = ref(true)
const username = ref('')
const password = ref('')
const error = ref('')
const userStore = useUserStore()
const router = useRouter()

const handleSubmit = async () => {
  error.value = ''
  const endpoint = isLogin.value ? '/api/auth/login' : '/api/auth/register'
  try {
    const res = await axios.post(endpoint, {username: username.value, password: password.value})
    userStore.setUser(res.data)
    router.push('/profile')
  } catch (err) {
    const e = err.response?.data?.error
    error.value = (typeof e === 'object' && e ? e.message : e) || '发生错误'
  }
}
</script>