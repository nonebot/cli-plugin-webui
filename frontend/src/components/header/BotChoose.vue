<script setup lang="ts">
import { ref } from 'vue'

import Drawer from '@/components/Drawer.vue'

const drawerRef = ref<InstanceType<typeof Drawer> | null>(null)
</script>

<template>
  <Drawer ref="drawerRef">
    <template v-slot:button>
      <button class="btn btn-sm btn-ghost btn-square" @click="drawerRef?.showDrawer()">
        <span class="material-symbols-outlined"> robot_2 </span>
      </button>
    </template>

    <template v-slot:drawer-title>实例选择</template>

    <template v-slot:drawer-body>
      <div class="h-full grid gap-2">
        <div
          role="button"
          :class="{
            'flex items-center justify-between gap-4 transition bg-base-200/50 hover:bg-base-200 rounded-lg p-4': true,
            'border-2 border-primary/50 hover:border-primary': true
          }"
        >
          <div class="shrink-0 flex items-center">
            <span class="material-symbols-outlined text-4xl"> deployed_code </span>
          </div>
          <div class="w-full">
            test
            <div class="text-xs opacity-50">114514</div>
          </div>
          <div class="shrink-0 flex gap-2">
            <div class="badge badge-success text-white">运行中</div>
          </div>
        </div>

        <div
          role="button"
          class="flex items-center justify-between gap-4 transition bg-base-200/50 hover:bg-base-200 rounded-lg p-4"
        >
          <div class="shrink-0 flex items-center">
            <span class="material-symbols-outlined text-4xl"> deployed_code </span>
          </div>
          <div class="w-full">
            test
            <div class="text-xs opacity-50">114514</div>
          </div>
          <div class="shrink-0 flex gap-2">
            <!-- <div class="badge badge-error text-white">暂停中</div> -->
          </div>
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
