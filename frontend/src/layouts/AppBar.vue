<script setup>
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useTheme } from 'vuetify'
import { useRouter } from 'vue-router'

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

const auth = useAuthStore()
const router = useRouter()
const theme = useTheme()

const username = computed(() => auth.user?.username || 'User')
const avatar = computed(() => auth.user?.avatar || 'https://randomuser.me/api/portraits/men/85.jpg')

const isDark = computed(() => theme.global.current.value.dark)
function toggleTheme() {
  theme.global.name.value = isDark.value ? 'light' : 'dark'
}

function handleLogout() {
  auth.logout()
  router.push('/login')
}
const emit = defineEmits(['update:drawer'])
function toggleDrawer() { emit('update:drawer', !props.drawer) }
</script>

<template>
  <v-app-bar
    flat
    height="64"
    class="border-b px-md-3"
    style="position: fixed; top: 0; left: 0; width: 100%; z-index: 1010;"
    app
  >
    <!-- Hamburger -->
    <v-app-bar-nav-icon
      @click="toggleDrawer"
      class="me-2"
      :aria-label="props.drawer ? 'Zamknij menu' : 'Otwórz menu'"
    />

    <!-- LOGO -->
    <a href="/" class="d-flex align-center" style="text-decoration: none;">
      <v-img
        src="https://upload.wikimedia.org/wikipedia/commons/a/a7/React-icon.svg"
        height="32"
        width="32"
        class="me-3"
        contain
      />
      <span class="text-h6 font-weight-bold">{{ isDark ? 'FinanceApp (dark)' : 'FinanceApp' }}</span>
    </a>

    <v-spacer />

    <!-- Przyciski po prawej -->
    <v-btn variant="text" icon="mdi-bell-outline" title="Powiadomienia" />
    <v-btn variant="text" icon="mdi-cog-outline" title="Ustawienia" />

    <v-btn
      :icon="true"
      class="mx-2"
      @click="toggleTheme"
      :title="isDark ? 'Tryb jasny' : 'Tryb ciemny'"
    >
      <v-icon>{{ isDark ? 'mdi-white-balance-sunny' : 'mdi-weather-night' }}</v-icon>
    </v-btn>

    <!-- Menu usera -->
    <v-menu
      location="bottom end"
      transition="slide-y-transition"
      :close-on-content-click="false"
      min-width="300"
      offset="8"
    >
      <template #activator="{ props }">
        <v-btn icon v-bind="props" size="large">
          <v-avatar size="40">
            <v-img :src="avatar" />
          </v-avatar>
        </v-btn>
      </template>
      <v-card
        rounded="lg"
        :elevation="6"
        width="320"
        :class="theme.global.current.value.dark ? 'v-theme--dark' : 'v-theme--light'"
      >
        <!-- Banner + Avatar -->
        <v-img
          src="https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=600&q=80"
          height="88"
          class="rounded-t-lg"
          cover
        >
          <template #placeholder>
            <div class="bg-surface-light" style="height: 88px;"></div>
          </template>
          <div class="d-flex flex-grow-1 justify-end fill-height align-start pa-2"></div>
        </v-img>
        <div class="text-center mt-n9 mb-2">
          <v-avatar size="72" class="elevation-2 border-md border-surface-light">
            <v-img :src="avatar" />
          </v-avatar>
          <div class="text-h6 mt-2">{{ username }}</div>
        </div>
        <v-divider class="my-2"></v-divider>
        <v-list nav density="compact">
          <v-list-item
            prepend-icon="mdi-view-dashboard-outline"
            title="Dashboard"
            to="/user/dashboard"
            :component="router"
          />
          <v-list-item
            prepend-icon="mdi-bell-outline"
            title="Notifications"
            to="/notifications"
            :component="router"
            append>
            <template #append>
              <v-badge color="error" dot offset-x="4" offset-y="6">
                <span slot="badge"></span>
              </v-badge>
            </template>
          </v-list-item>
          <v-list-item
            prepend-icon="mdi-star-outline"
            title="Sponsorships"
            to="/sponsorships"
            :component="router"
          />
          <v-list-item
            prepend-icon="mdi-card-bulleted-outline"
            title="Subscriptions"
            to="/subscriptions"
            :component="router"
          />
          <v-list-item
            prepend-icon="mdi-cog-outline"
            title="Settings"
            to="/settings"
            :component="router"
          />
          <v-list-item
            prepend-icon="mdi-logout"
            title="Logout"
            class="text-error font-weight-bold"
            @click="handleLogout"
          />
        </v-list>
      </v-card>
    </v-menu>
  </v-app-bar>
</template>

<style scoped>
/* usuń wszelkie ręczne style koloru tła/tekstu tutaj */
</style>
