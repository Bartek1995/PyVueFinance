// src/stores/auth.js
import { defineStore } from 'pinia'
import api from '@/api/apiService'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isLoggedIn: !!localStorage.getItem('access_token'),
    accessToken: localStorage.getItem('access_token') || null,
    refreshToken: localStorage.getItem('refresh_token') || null,
    user: null,
  }),
  actions: {
    async login(username, password) {
      const res = await api.post('token/', { username, password })
      this.accessToken = res.data.access
      this.refreshToken = res.data.refresh
      this.isLoggedIn = true
      localStorage.setItem('access_token', res.data.access)
      localStorage.setItem('refresh_token', res.data.refresh)
      api.defaults.headers.common['Authorization'] = `Bearer ${res.data.access}`
      await this.fetchUser()
    },
    async fetchUser() {
      try {
        const res = await api.get('accounts/me/')
        this.user = res.data
        this.isLoggedIn = true
      } catch (e) {
        this.user = null
        this.isLoggedIn = false
      }
    },
    logout() {
      this.accessToken = null
      this.refreshToken = null
      this.isLoggedIn = false
      this.user = null
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      delete api.defaults.headers.common['Authorization']
    },
    async initialize() {
      // Zawsze ustaw header jeśli masz token po starcie apki!
      if (this.accessToken) {
        api.defaults.headers.common['Authorization'] = `Bearer ${this.accessToken}`
        await this.fetchUser()
      } else {
        this.isLoggedIn = false
        this.user = null
      }
    }
  },
})
