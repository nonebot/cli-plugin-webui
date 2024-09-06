<script setup lang="ts">
import { onUnmounted, ref, watch } from 'vue'

import Drawer from '@/components/Drawer.vue'
import { useToastStore } from '@/stores/ToastStorage'

const store = useToastStore()

const drawerRef = ref<InstanceType<typeof Drawer> | null>(null)
const timers = ref<{ [key: string]: ReturnType<typeof setInterval> }>({})

const time = (timestamp: number) => {
  const now = Date.now()
  const diff = now - timestamp

  const seconds = Math.floor(diff / 1000)
  const minutes = Math.floor(seconds / 60)
  const hours = Math.floor(minutes / 60)
  const days = Math.floor(hours / 24)

  let text = ''
  if (days > 0) {
    text = `${days}d${hours % 24}h${minutes % 60}m`
  } else if (hours > 0) {
    text = `${hours}h${minutes % 60}m`
  } else if (minutes > 0) {
    text = `${minutes}m`
  }

  return !text ? 'recently' : `${text} ago`
}

watch(
  () => store.toasts.length,
  () => {
    store.toasts.forEach((toast) => {
      if (!timers.value[toast.id]) {
        timers.value[toast.id] = setInterval(() => {
          store.remove(toast.id)
        }, 1000)
      }
    })

    Object.keys(timers.value).forEach((timer) => {
      if (!store.toasts.find((toast) => toast.id === timer)) {
        clearInterval(timers.value[timer])
        delete timers.value[timer]
      }
    })
  }
)

onUnmounted(() => {
  Object.values(timers.value).forEach((timer) => clearInterval(timer))
})
</script>

<template>
  <Drawer ref="drawerRef">
    <template v-slot:button>
      <button class="btn btn-sm btn-ghost btn-square" @click="drawerRef?.showDrawer()">
        <div class="indicator">
          <span
            v-if="store.toasts.length"
            class="indicator-item badge badge-primary font-normal text-white"
            >{{ store.toasts.length }}</span
          >
          <span class="material-symbols-outlined"> notifications </span>
        </div>
      </button>
    </template>

    <template v-slot:drawer-title>消息列表</template>

    <template v-slot:drawer-body>
      <div class="grid gap-2">
        <div
          v-for="toast in store.toasts"
          :key="toast.id"
          class="p-4 bg-base-200/50 hover:bg-base-200 rounded-lg transition-colors flex flex-col gap-2"
        >
          <div class="flex gap-2 text-wrap">
            <span
              v-if="toast.type === 'success'"
              class="material-symbols-outlined text-success text-3xl"
            >
              check_circle
            </span>
            <span
              v-else-if="toast.type === 'error'"
              class="material-symbols-outlined text-error text-3xl"
            >
              cancel
            </span>
            <span
              v-else-if="toast.type === 'info'"
              class="material-symbols-outlined text-info text-3xl"
            >
              info
            </span>
            <span
              v-else-if="toast.type === 'warning'"
              class="material-symbols-outlined text-warning text-3xl"
            >
              error
            </span>

            <p class="w-full break-all flex items-center">{{ toast.message }}</p>

            <button
              class="btn btn-sm btn-square btn-ghost font-normal"
              @click="store.remove(toast.id, false)"
            >
              <span class="material-symbols-outlined"> close </span>
            </button>
          </div>

          <div v-if="toast.from || toast.time" class="flex items-center justify-between">
            <div class="text-xs text-base-content/50">
              {{ toast.from ? `From: ${toast.from}` : '' }}
            </div>
            <div class="text-xs text-base-content/50">{{ time(toast.time) }}</div>
          </div>
        </div>
      </div>
    </template>

    <template v-slot:drawer-footer>
      <div>
        <div class="bg-base-content/10 h-px"></div>
        <div class="flex justify-center items-center p-2">
          <button class="btn btn-ghost">清除所有</button>
        </div>
      </div>
    </template>
  </Drawer>
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
