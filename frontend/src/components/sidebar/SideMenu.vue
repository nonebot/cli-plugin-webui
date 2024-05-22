<script setup lang="ts">
import { useRoute } from 'vue-router'
import { useViewHistoryRecorderStore } from '@/stores'
import { defaultRoutes, type NavItem } from '@/router/client'

const route = useRoute()
const store = useViewHistoryRecorderStore()

const getCurrentRoute = () => {
  return route.path
}

const recordView = (route: NavItem) => {
  if (store.viewHistory.some((i: any) => i.routeData.path === route.routeData.path)) {
    return
  }
  store.record(route)
}
</script>

<template>
  <ul class="h-full pt-8 px-4 menu rounded-box">
    <li v-for="route in defaultRoutes" class="mb-2" @click="recordView(route)">
      <details v-if="route.routeData.children">
        <summary>
          <span class="material-symbols-outlined">{{ route.googleIcon }}</span>
          {{ route.name }}
        </summary>
        <ul>
          <li v-for="childRoute in route.routeData.children" class="mb-2">
            {{ childRoute.name }}
          </li>
        </ul>
      </details>
      <RouterLink
        :to="route.routeData.path"
        :class="{ active: route.routeData.path === getCurrentRoute() }"
      >
        <span class="material-symbols-outlined">{{ route.googleIcon }}</span>
        {{ route.name }}
      </RouterLink>
    </li>
  </ul>
</template>

<style scoped>
.material-symbols-outlined {
  font-variation-settings:
    'FILL' 0,
    'wght' 300,
    'GRAD' -25,
    'opsz' 48;
}

.menu li > *:not(ul, .menu-title, details, .btn):active,
.menu li > *:not(ul, .menu-title, details, .btn).active,
.menu li > details > summary:active {
  --tw-bg-opacity: 0.2;
  background-color: var(--fallback-n, oklch(var(--p) / var(--tw-bg-opacity)));
  color: var(--fallback-nc, oklch(var(--p) / var(--tw-text-opacity)));
}
</style>
