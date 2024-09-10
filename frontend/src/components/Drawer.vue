<script setup lang="ts">
// TODO: 优化组件使用体验

import { ref } from 'vue'

const isShow = ref(false)

defineExpose({
  showDrawer: () => {
    isShow.value = true
  },
  hiddenDrawer: () => {
    hiddenDrawer()
  }
})

const hiddenDrawer = () => {
  isShow.value = false
}
</script>

<template>
  <slot name="button"></slot>

  <div class="fixed z-50 top-0 left-0 flex h-full overflow-hidden">
    <Transition>
      <div
        v-show="isShow"
        role="button"
        class="h-screen w-screen bg-gray-500/50"
        @click="hiddenDrawer"
      ></div>
    </Transition>

    <div
      :class="{
        'fixed top-0 right-0 z-50 h-screen bg-base-100 shadow-2xl w-2/5 xl:w-1/4 transition shrink-0 flex flex-col': true,
        'translate-x-0 opacity-100': isShow,
        'translate-x-full opacity-0': !isShow
      }"
    >
      <!-- Drawer Header -->
      <div class="h-16 px-6 shrink-0 flex items-center justify-between">
        <span class="text-xl font-semibold">
          <slot name="drawer-title"></slot>
        </span>
        <div class="btn btn-sm btn-square btn-ghost" @click="hiddenDrawer">
          <span class="material-symbols-outlined"> arrow_forward_ios </span>
        </div>
      </div>

      <div class="bg-base-content/10 h-px"></div>

      <div class="flex flex-col overflow-y-scroll h-full px-6 py-4">
        <!-- Drawer Body -->
        <slot name="drawer-body"></slot>
      </div>

      <!-- Drawer Footer -->
      <slot name="drawer-footer"></slot>
    </div>
  </div>
</template>

<style scoped>
.v-enter-active,
.v-leave-active {
  transition: opacity 150ms ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}

.material-symbols-outlined {
  font-variation-settings:
    'FILL' 0,
    'wght' 300,
    'GRAD' 0,
    'opsz' 24;
}
</style>
