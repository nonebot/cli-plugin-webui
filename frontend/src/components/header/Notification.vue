<script setup lang="ts">
import { ref } from 'vue'

import Drawer from '@/components/Drawer.vue'
import { useToastStore } from '@/stores'

const store = useToastStore()

const drawerRef = ref<InstanceType<typeof Drawer> | null>(null)
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
      <div v-if="store.toasts.length" class="grid gap-2">
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

          <div v-if="toast.from" class="text-xs text-base-content/50">
            {{ toast.from ? `From: ${toast.from}` : '' }}
          </div>
        </div>
      </div>
      <div v-else class="text-center">暂无消息</div>
    </template>

    <template v-slot:drawer-footer>
      <div v-if="store.toasts.length">
        <div class="bg-base-content/10 h-px"></div>
        <button class="w-full rounded-none btn btn-lg btn-ghost" @click="store.clear()">
          清除所有
        </button>
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
