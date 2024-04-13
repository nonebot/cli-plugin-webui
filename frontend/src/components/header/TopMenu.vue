<script setup lang="ts">
import Notification from '@/components/header/Notification.vue'
import BotChoose from '@/components/header/BotChoose.vue'

const toggleTheme = (e: Event) => {
  const target = e.target as HTMLInputElement
  const theme = target.value
  document.documentElement.classList.toggle('dark', theme === 'dark')
}
</script>

<template>
  <div class="h-16 flex px-4 xl:px-8 py-2">
    <div class="h-full w-full flex items-center">
      <div class="max-w-xs text-sm breadcrumbs">
        <ul>
          <li>Long text 1</li>
          <li>Long text 2</li>
        </ul>
      </div>
    </div>
    <div class="h-full w-full flex justify-end items-center gap-4">
      <div class="badge badge-ghost">当前实例: 114514</div>

      <button class="btn btn-sm btn-ghost btn-square">
        <label class="swap swap-rotate">
          <input type="checkbox" class="theme-controller" value="dark" />

          <span class="swap-on fill-current material-symbols-outlined"> dark_mode </span>
          <span class="swap-off fill-current material-symbols-outlined"> light_mode </span>
        </label>
      </button>

      <Notification />

      <BotChoose />

      <button class="btn btn-sm btn-ghost btn-square">
        <span class="material-symbols-outlined"> tune </span>
      </button>
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
