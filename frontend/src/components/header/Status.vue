<script setup lang="ts">
import { useNoneBotStore } from '@/stores'

const store = useNoneBotStore()

const isDebug = () => {
  return localStorage.getItem('isDebug') === '1'
}
</script>

<template>
  <div class="badge-items flex items-center gap-2">
    <div v-if="isDebug()" class="badge badge-warning">开发模式</div>
    <div class="badge badge-ghost">当前实例: {{ store.selectedBot?.project_name }}</div>
  </div>
</template>

<style scoped>
.badge-items {
  .badge {
    @apply shrink-0;
  }
}
</style>
