<script setup lang="ts">
import Notification from '@/components/header/Notification.vue'
import BotChoose from '@/components/header/BotChoose.vue'
import Status from '@/components/header/Status.vue'

const toggleTheme = (theme: 'light' | 'dark') => {
  document.documentElement.setAttribute('data-theme', theme)
}
</script>

<template>
  <div class="h-16 px-4 xl:px-8 py-2 flex justify-between">
    <div class="h-full flex items-center">
      <div class="max-w-xs text-sm breadcrumbs">
        <ul>
          <li>Long text 1</li>
          <li>Long text 2</li>
        </ul>
      </div>
    </div>
    <div class="h-full flex justify-end items-center gap-4">
      <Status />

      <button class="btn btn-sm btn-ghost btn-square">
        <label class="swap swap-rotate">
          <input type="checkbox" />

          <span class="swap-on fill-current material-symbols-outlined" @click="toggleTheme('dark')">
            dark_mode
          </span>
          <span
            class="swap-off fill-current material-symbols-outlined"
            @click="toggleTheme('light')"
          >
            light_mode
          </span>
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
