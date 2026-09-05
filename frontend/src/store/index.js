import { defineStore } from 'pinia'
import axios from '@/api'

export const useUserStore = defineStore('user', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('tcm_user')) || null
  }),
  actions: {
    setUser(user) {
      this.user = user
      localStorage.setItem('tcm_user', JSON.stringify(user))
    },
    logout() {
      this.user = null
      localStorage.removeItem('tcm_user')
    },
    async verifySession() {
      if (!this.user) return false
      try {
        await axios.get(`/api/auth/user/${this.user.id}/verify`)
        return true
      } catch {
        this.logout()
        return false
      }
    }
  }
})