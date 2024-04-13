<script setup lang="ts">
import SideMenu from '@/components/sidebar/SideMenu.vue'
</script>

<template>
  <div class="w-72 h-full flex-shrink-0 relative bg-base-200/50 flex flex-col justify-between">
    <div class="px-4 py-2 flex items-center">
      <div class="flex items-center">
        <span class="material-symbols-outlined text-primary text-5xl px-2 py-0"> circle </span>
        <div class="text-xl font-semibold leading-7 normal-case">NoneBot</div>
      </div>
    </div>

    <SideMenu />
  </div>
</template>

<style scoped>
.material-symbols-outlined {
  font-variation-settings:
    'FILL' 0,
    'wght' 200,
    'GRAD' -25,
    'opsz' 48;
}
</style>
