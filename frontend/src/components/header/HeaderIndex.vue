<script setup lang="ts">
import TopMenu from '@/components/header/TopMenu.vue'
import TabBar from '@/components/header/TabBar.vue'
</script>

<template>
  <header class="top-0 right-0 w-full">
    <TopMenu />

    <TabBar />
  </header>
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
