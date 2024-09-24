<script setup lang="ts">
import { useRoute } from 'vue-router'
import { useCustomStore, useViewHistoryRecorderStore } from '@/stores'
import { defaultRoutes, type NavItem } from '@/router/client'

const route = useRoute()
const store = useViewHistoryRecorderStore()
const customStore = useCustomStore()

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
  <ul class="h-full pt-8 px-0 menu rounded-box">
    <li v-for="route in defaultRoutes" :key="route.name" class="mb-2" @click="recordView(route)">
      <RouterLink
        :to="route.routeData.path"
        :class="{
          active: route.routeData.path === getCurrentRoute(),
          'btn-block lg:btn-square flex items-center justify-start lg:justify-center':
            customStore.menuMinify
        }"
        @click="customStore.toggleMenuShow()"
      >
        <span class="material-symbols-outlined">{{ route.googleIcon }}</span>
        <span :class="{ 'block lg:hidden': customStore.menuMinify }">{{ route.name }}</span>
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
