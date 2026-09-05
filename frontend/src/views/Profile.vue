<template>
  <div class="space-y-8 pb-20">
    <!-- User Info -->
    <div class="bg-white rounded-sm shadow-lg p-8 border border-border relative">
      <div class="absolute top-0 right-0 opacity-5 text-9xl font-serif -mt-10 -mr-10 pointer-events-none text-primary">
        我
      </div>
      <div class="flex items-center space-x-6">
        <div class="w-20 h-20 bg-[#f5f0e6] rounded-full flex items-center justify-center border-2 border-primary">
          <User class="w-10 h-10 text-primary" />
        </div>
        <div>
          <h2 class="text-3xl font-serif font-bold text-secondary mb-2">{{ user?.username }}</h2>
          <p class="text-primary font-serif">欢迎来到中医体质辨识系统</p>
        </div>
      </div>
      <div class="mt-8 flex justify-end">
        <button @click="logout" class="flex items-center text-red-700 hover:text-red-900 font-serif border border-red-200 px-4 py-2 rounded-sm hover:bg-red-50">
          <LogOut class="w-4 h-4 mr-2" /> 退出登录
        </button>
      </div>
    </div>

    <!-- History -->
    <div class="bg-white rounded-sm shadow-lg p-8 border border-border">
      <h3 class="text-2xl font-serif font-bold text-secondary mb-6 flex items-center border-b-2 border-border pb-3">
        <FileText class="w-6 h-6 mr-3 text-primary" /> 辨识记录
      </h3>
      <div v-if="loading" class="text-center py-10 text-primary">加载中...</div>
      <div v-else-if="history.length" class="space-y-4">
        <router-link
          v-for="h in history"
          :key="h.id"
          :to="`/result/${h.id}`"
          class="block bg-paper rounded-sm p-5 border border-[#c0b298] hover:shadow-md group"
        >
          <div class="flex justify-between items-center">
            <div>
              <div class="flex items-center space-x-3 mb-2">
                <span class="bg-[#8b3a3a] text-white px-3 py-1 rounded-sm text-sm font-serif">
                  {{ constitutionNames[h.primary] }}
                </span>
                <span v-if="h.secondary?.length" class="text-[#6b5c51] text-sm font-serif">
                  兼夹: {{ h.secondary.map(s => constitutionNames[s]).join('、') }}
                </span>
              </div>
              <p class="text-primary text-sm font-serif">
                测评时间: {{ new Date(h.createdAt).toLocaleString('zh-CN') }}
              </p>
            </div>
            <ChevronRight class="w-6 h-6 text-[#c0b298] group-hover:text-primary transition-colors" />
          </div>
        </router-link>
      </div>
      <div v-else class="text-center py-12 bg-paper rounded-sm border border-dashed border-[#c0b298]">
        <p class="text-primary font-serif text-lg mb-4">暂无辨识记录</p>
        <router-link to="/" class="inline-block bg-primary text-white px-6 py-2 rounded-sm font-serif hover:bg-secondary">
          去测评
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useUserStore } from '@/store'
import { useRouter } from 'vue-router'
import { User, LogOut, FileText, ChevronRight } from 'lucide-vue-next'
import axios from '@/api'

const userStore = useUserStore()
const router = useRouter()
const history = ref([])
const loading = ref(true)

const user = computed(() => userStore.user)

const constitutionNames = {
  pinghe: '平和质', qixu: '气虚质', yangxu: '阳虚质', yinxu: '阴虚质',
  tanshi: '痰湿质', shire: '湿热质', xueyu: '血瘀质', qiyu: '气郁质', tebing: '特禀质'
}

onMounted(async () => {
  if (!user.value) {
    router.push('/auth')
    return
  }
  try {
    const res = await axios.get(`/api/user/${user.value.id}/history`)
    history.value = res.data
  } catch (error) {
    if (error.response?.status === 401) {
      userStore.logout()
      router.push('/auth')
    }
  } finally {
    loading.value = false
  }
})

const logout = () => {
  userStore.logout()
  router.push('/')
}
</script>