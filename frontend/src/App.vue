<script setup>
import { ref } from 'vue'
import Navigation from './components/Navigation.vue'
import { RouterView } from 'vue-router'

const drawer = ref(true)
</script>

<template>
  <v-app>
    <Navigation v-model:drawer="drawer" />
    <v-app-bar app>
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>PyVueFinance</v-toolbar-title>
      <v-spacer />
    </v-app-bar>
    <v-main>
      <v-container class="py-6" fluid>
        <RouterView />
      </v-container>
    </v-main>
  </v-app>
</template>
