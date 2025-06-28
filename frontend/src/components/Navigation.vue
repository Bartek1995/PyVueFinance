<script setup>
import { RouterLink } from 'vue-router'

defineProps({
  drawer: {
    type: Boolean,
    required: true,
  },
  'onUpdate:drawer': {
    type: Function,
    required: true,
  },
})

const navItems = [
  { title: 'Home', icon: 'mdi-home', to: '/' },
  { title: 'Companies', icon: 'mdi-domain', to: '/companies' },
  { title: 'Add Company', icon: 'mdi-magnify', to: '/company-search' }
]
</script>

<template>
  <v-navigation-drawer
    :model-value="drawer"
    @update:model-value="$emit('update:drawer', $event)"
    app
    permanent
    width="220"
  >
    <v-list>
      <v-list-item>
        <v-list-item-title class="text-h6 font-weight-bold"> PyVueFinance </v-list-item-title>
      </v-list-item>
      <v-divider />
      <v-list-item
        v-for="item in navItems"
        :key="item.title"
        :to="item.to"
        link
        component="RouterLink"
      >
        <v-list-item-icon>
          <v-icon>{{ item.icon }}</v-icon>
        </v-list-item-icon>
        <v-list-item-title>{{ item.title }}</v-list-item-title>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>
