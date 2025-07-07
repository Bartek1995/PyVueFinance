import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import vuetify from './vuetify'
import { createPinia } from 'pinia'
import VueApexCharts from 'vue3-apexcharts'
import { useAuthStore } from '@/stores/auth'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)
app.use(vuetify)
app.use(VueApexCharts)

const auth = useAuthStore()
auth.initialize()

app.mount('#app')
