import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import CompaniesView from '@/views/CompaniesView.vue'

const routes = [
  { path: '/', name: 'Home', component: HomeView },
  { path: '/companies', name: 'Companies', component: CompaniesView },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
