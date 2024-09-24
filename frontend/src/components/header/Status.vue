<script setup lang="ts">
import { useStatusStore } from '@/stores'

const statusStore = useStatusStore()
</script>

<template>
  <div class="hidden md:flex shrink-0 items-center gap-2 badge-items">
    <div
      v-for="(status, id) of statusStore.statusItems"
      :key="id"
      class="badge"
      :class="status.css"
    >
      {{ status.text }}
    </div>
  </div>
</template>

<style scoped>
.badge-items {
  .badge {
    @apply shrink-0;
  }
}
</style>
