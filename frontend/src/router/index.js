import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import CompaniesView from '@/views/company/CompaniesView.vue'
import CompanySearcher from '@/views/company/CompanySearcher.vue'
import CompanyDetails from '@/views/company/CompanyDetails.vue'
import LoginView from '@/auth/LoginView.vue'

const routes = [
  { path: '/login', component: LoginView, name: 'Login' },
  { path: '/', name: 'Home', component: HomeView, meta: { requiresAuth: true } },
  { path: '/companies', name: 'Companies', component: CompaniesView, meta: { requiresAuth: true } },
  { path: '/company-search', name: 'CompanySearcher', component: CompanySearcher, meta: { requiresAuth: true } },
  { path: '/company/:ticker', name: 'CompanyDetails', component: CompanyDetails, meta: { requiresAuth: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const isLoggedIn = !!localStorage.getItem('access_token')
  if (to.meta.requiresAuth && !isLoggedIn) {
    next({ path: '/login', query: { next: to.fullPath } })
  } else {
    next()
  }
})

export default router
