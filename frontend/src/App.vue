<script setup>
import { ref } from 'vue'
import Navigation from '@/layouts/Navigation.vue'
import AppBar from '@/layouts/AppBar.vue'
import { RouterView } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const drawer = ref(true)
const auth = useAuthStore()
</script>

<template>
  <v-app>
    <Navigation
      v-if="auth.isLoggedIn"
      :drawer="drawer"
      @update:drawer="drawer = $event"
    />
    <AppBar
      v-if="auth.isLoggedIn"
      :drawer="drawer"
      @update:drawer="drawer = $event"
    />
    <v-main>
      <v-container fluid class="py-6">
        <RouterView />
      </v-container>
    </v-main>
  </v-app>
</template>
