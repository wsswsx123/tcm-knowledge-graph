import { createRouter, createWebHistory } from 'vue-router'
// 路由懒加载：每个页面独立 chunk，首屏只加载问卷页，显著减小首包体积
import Questionnaire from '@/views/Questionnaire.vue'

const Result = () => import('@/views/Result.vue')
const Profile = () => import('@/views/Profile.vue')
const Recommendation = () => import('@/views/Recommendation.vue')
const GraphView = () => import('@/views/GraphView.vue')
const Auth = () => import('@/views/Auth.vue')
const Admin = () => import('@/views/Admin.vue')
const AgentChat = () => import('@/views/AgentChat.vue')

const routes = [
  { path: '/', component: Questionnaire },
  { path: '/result/:id', component: Result },
  { path: '/profile', component: Profile },
  { path: '/recommendation', component: Recommendation },
  { path: '/graph', component: GraphView },
  { path: '/auth', component: Auth },
  { path: '/admin', component: Admin },
  { path: '/agent', component: AgentChat },
  // 兜底：未匹配的路径统一回到问卷首页，避免渲染成空白页
  { path: '/:pathMatch(.*)*', redirect: '/' },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router