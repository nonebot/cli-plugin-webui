<script setup lang="ts">
import { useRoute } from 'vue-router'
import { useViewHistoryRecorderStore } from '@/stores'
import { defaultRoutes, type RouteItem } from '@/router/client'

const route = useRoute()
const store = useViewHistoryRecorderStore()

const getCurrentRoute = () => {
  return route.path
}

const recordView = (route: RouteItem) => {
  if (store.viewHistory.some((i: any) => i.routeData.path === route.routeData.path)) {
    return
  }
  store.record(route)
}
</script>

<template>
  <ul class="h-full pt-8 px-4 menu rounded-box">
    <li v-for="i in defaultRoutes" class="mb-2" @click="recordView(i)">
      <RouterLink
        :to="i.routeData.path"
        :class="{ active: i.routeData.path === getCurrentRoute() }"
      >
        <span class="material-symbols-outlined">{{ i.googleIcon }}</span>
        {{ i.name }}
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
