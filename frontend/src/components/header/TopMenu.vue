<script setup lang="ts">
import router from '@/router'
import { useCustomStore, useToastStore } from '@/stores'
import Notification from '@/components/header/Notification.vue'
import BotChoose from '@/components/header/BotChoose.vue'
import Status from '@/components/header/Status.vue'
import WebUISettings from '@/components/header/WebUISettings.vue'

const store = useCustomStore()
const toast = useToastStore()

const logout = () => {
  localStorage.clear()
  router.push('/login')
  toast.add('success', '已登出', '', 5000)
}
</script>

<template>
  <div class="h-16 px-4 xl:px-8 py-2 flex justify-end bg-base-100">
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
        <span class="material-symbols-outlined text-primary" @click="logout()"> logout </span>
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
