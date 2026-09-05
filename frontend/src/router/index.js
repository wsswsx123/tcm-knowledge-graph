import { createRouter, createWebHistory } from 'vue-router'
import Questionnaire from '@/views/Questionnaire.vue'
import Result from '@/views/Result.vue'
import Profile from '@/views/Profile.vue'
import Recommendation from '@/views/Recommendation.vue'
import GraphView from '@/views/GraphView.vue'
import Auth from '@/views/Auth.vue'
import Admin from '@/views/Admin.vue'
import AgentChat from '@/views/AgentChat.vue'

const routes = [
  { path: '/', component: Questionnaire },
  { path: '/result/:id', component: Result },
  { path: '/profile', component: Profile },
  { path: '/recommendation', component: Recommendation },
  { path: '/graph', component: GraphView },
  { path: '/auth', component: Auth },
  { path: '/admin', component: Admin },
  { path: '/agent', component: AgentChat },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router