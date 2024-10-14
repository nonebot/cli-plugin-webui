<script setup lang="ts">
import router from '@/router'
import { useCustomStore, useToastStore } from '@/stores'
import NotificationItem from '@/components/header/NotificationItem.vue'
import BotChoose from '@/components/header/BotChoose.vue'
import StatusItem from '@/components/header/StatusItem.vue'
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
  <div class="relative h-16 px-4 xl:px-8 py-2 flex justify-end items-center bg-base-100">
    <button
      :class="{
        'z-20 absolute -left-5 size-10 flex items-center justify-center invisible lg:visible': true,
        '-scale-100': store.menuMinify
      }"
      @click="store.toggleMenuMinify()"
    >
      <span class="material-symbols-outlined"> menu_open </span>
    </button>
    <button
      class="visible lg:invisible relative size-10 flex items-center justify-center"
      @click="store.toggleMenuShow()"
    >
      <span class="material-symbols-outlined"> menu </span>
    </button>

    <div class="w-full"></div>

    <div class="h-full flex justify-end items-center gap-4">
      <StatusItem />

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

      <NotificationItem />

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
