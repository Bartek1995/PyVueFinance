import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import CompaniesView from '@/views/CompaniesView.vue'
import CompanySearcher from '@/views/CompanySearcher.vue'
import CompanyDetails from '@/views/CompanyDetails.vue'

const routes = [
  { path: '/', name: 'Home', component: HomeView },
  { path: '/companies', name: 'Companies', component: CompaniesView },
  { path: '/company-search', name: 'CompanySearcher', component: CompanySearcher },
  { path: '/company/:ticker', name: 'CompanyDetails', component: CompanyDetails },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
