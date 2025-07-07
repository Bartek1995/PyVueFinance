import axios from 'axios'
import router from '@/router'
import { useAuthStore } from '@/stores/auth'

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
})
// Set common headers for all requests

api.interceptors.response.use(
  response => response,
  error => {
    if (error.response && error.response.status === 401) {
      const auth = useAuthStore()
      auth.logout()
      router.push({ name: 'Login', query: { next: router.currentRoute.value.fullPath } })
    }
    return Promise.reject(error)
  }
)

export default api
