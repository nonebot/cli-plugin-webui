<script setup lang="ts">
import { ref } from 'vue'

import Drawer from '@/components/Drawer.vue'

const drawerRef = ref<InstanceType<typeof Drawer> | null>(null)
</script>

<template>
  <Drawer ref="drawerRef">
    <template v-slot:button>
      <button class="btn btn-sm btn-ghost btn-square" @click="drawerRef?.showDrawer()">
        <div class="indicator">
          <span class="indicator-item badge badge-primary font-normal text-white">4</span>
          <span class="material-symbols-outlined"> notifications </span>
        </div>
      </button>
    </template>

    <template v-slot:drawer-title>消息列表</template>

    <template v-slot:drawer-body>
      <div class="grid gap-2 h-full">
        <div class="flex items-center transition bg-base-200/50 hover:bg-base-200 rounded-lg p-4">
          <!-- icon -->
          <div class="shrink-0">
            <span class="material-symbols-outlined text-info text-3xl"> info </span>
          </div>
          <div class="w-full flex flex-col px-2">
            <div class="font-medium">测试通知</div>
            1145141919810
          </div>
          <button class="btn btn-sm btn-square btn-ghost font-normal">
            <span class="material-symbols-outlined"> close </span>
          </button>
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
