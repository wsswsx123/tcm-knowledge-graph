import axios from 'axios'

axios.defaults.baseURL = import.meta.env.VITE_API_BASE || ''

// 请求拦截器：若已登录（本地存有 JWT），自动附加 Authorization 头
axios.interceptors.request.use((config) => {
  try {
    const stored = localStorage.getItem('tcm_user')
    if (stored) {
      const user = JSON.parse(stored)
      if (user && user.token) {
        config.headers = config.headers || {}
        config.headers.Authorization = `Bearer ${user.token}`
      }
    }
  } catch (e) {
    // 解析失败忽略
  }
  return config
})

export default axios
