<script setup lang="ts">
import router from '@/router'
import { computed } from 'vue'
import { useCustomStorage } from '@/stores'
import Notification from '@/components/header/Notification.vue'
import BotChoose from '@/components/header/BotChoose.vue'
import Status from '@/components/header/Status.vue'
import WebUISettings from '@/components/header/WebUISettings.vue'

const store = useCustomStorage()

interface RouteItem {
  path: string
  name: string
}

const getBreadcrumbs = computed(() => {
  const path = router.currentRoute.value.path
  const paths = path.split('/').filter((item) => item)
  const routes: RouteItem[] = []
  let routePath = ''
  paths.forEach((item) => {
    routePath += `/${item}`
    routes.push({
      path: routePath,
      name: item
    })
  })
  return routes
})
</script>

<template>
  <div class="h-16 px-4 xl:px-8 py-2 flex justify-between">
    <div class="h-full flex items-center">
      <div class="max-w-xs text-sm breadcrumbs">
        <ul>
          <li v-for="(item, index) in getBreadcrumbs" :key="index">
            <a class="hover:link" @click="router.push(item.path)">{{ item.name }}</a>
          </li>
        </ul>
      </div>
    </div>
    <div class="h-full flex justify-end items-center gap-4">
      <Status />

      <button class="btn btn-sm btn-ghost btn-square">
        <label class="swap swap-rotate">
          <input type="checkbox" />

          <span
            class="swap-on fill-current material-symbols-outlined"
            @click="store.toggleTheme('dark')"
          >
            dark_mode
          </span>
          <span
            class="swap-off fill-current material-symbols-outlined"
            @click="store.toggleTheme('light')"
          >
            light_mode
          </span>
        </label>
      </button>

      <Notification />

      <BotChoose />

      <WebUISettings />
      <button class="btn btn-sm btn-ghost btn-square">
        <span class="material-symbols-outlined text-primary" @click="$router.push('/login')">
          logout
        </span>
      </button>
    </div>
  </div>
</template>

<style scoped>
.material-symbols-outlined {
  font-variation-settings:
    'FILL' 0,
    'wght' 400,
    'GRAD' -25,
    'opsz' 48;
}
</style>
