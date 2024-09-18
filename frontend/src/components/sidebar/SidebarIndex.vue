<script setup lang="ts">
import SideMenu from '@/components/sidebar/SideMenu.vue'
import { useCustomStore } from '@/stores'

const store = useCustomStore()
</script>

<template>
  <div
    :class="{
      'z-20 h-full shrink-0 flex flex-col justify-between py-2 px-4 transition-all': true,
      'fixed lg:relative -translate-x-full lg:translate-x-0 bg-base-200 lg:bg-base-200/50 w-full lg:w-72': true,
      '!-translate-x-0': store.menuShow,
      'lg:!w-20': store.menuMinify
    }"
  >
    <div class="flex items-center relative gap-2">
      <div class="indicator">
        <span
          v-if="store.isDebug"
          class="indicator-item indicator-middle indicator-center material-symbols-outlined"
        >
          build
        </span>
        <span class="flex-shrink-0 material-symbols-outlined text-primary text-5xl"> circle </span>
      </div>

      <div
        class="shrink-0 text-xl font-semibold leading-7 normal-case"
        :class="{ 'visible lg:invisible': store.menuMinify }"
      >
        NoneBot
      </div>

      <div class="w-full"></div>

      <div
        :class="{ 'btn btn-sm btn-square btn-ghost': true, 'block lg:hidden': true }"
        @click="store.toggleMenuShow()"
      >
        <span class="material-symbols-outlined"> arrow_back_ios </span>
      </div>
    </div>

    <SideMenu />
  </div>
</template>

<style scoped>
.material-symbols-outlined {
  font-variation-settings:
    'FILL' 0,
    'wght' 300,
    'GRAD' -25,
    'opsz' 48;
}
</style>
