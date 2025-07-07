<script setup>
import { RouterLink, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { computed } from 'vue'

const props = defineProps({
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
  { title: 'Home', icon: 'mdi-home-outline', to: '/' },
  { title: 'Companies', icon: 'mdi-domain', to: '/companies' },
  { title: 'Add Company', icon: 'mdi-magnify', to: '/company-search' },
]

const auth = useAuthStore()
const username = computed(() => auth.user?.username || 'User')
const userInitial = computed(() => (username.value ? username.value.charAt(0).toUpperCase() : 'U'))
const userEmail = computed(() => auth.user?.email || 'brak@email.com')
const emit = defineEmits(['update:drawer'])
</script>

<template>
  <v-navigation-drawer
    :model-value="props.drawer"
    @update:model-value="emit('update:drawer', $event)"
    app
    width="280"
    class="py-2"
  >
    <!-- AVATAR i user info -->
    <v-list>
      <v-list-item :title="username" :subtitle="userEmail">
        <template #prepend>
          <v-avatar color="primary" size="36">
            <template v-if="auth.user?.avatar">
              <v-img :src="auth.user.avatar" />
            </template>
            <template v-else>
              <span class="text-white text-lg">{{ userInitial }}</span>
            </template>
          </v-avatar>
        </template>
      </v-list-item>
    </v-list>

    <v-divider></v-divider>

    <!-- NAVIGATION -->
    <v-list density="compact" nav>
      <v-list-item
        v-for="item in navItems"
        :key="item.title"
        :to="item.to"
        :prepend-icon="item.icon"
        :title="item.title"
        rounded="xl"
        :component="RouterLink"
        active-class="bg-primary text-primary-contrast"
      ></v-list-item>
    </v-list>

  </v-navigation-drawer>
</template>

<style scoped>
.text-lg {
  font-size: 1.1rem;
}
</style>
