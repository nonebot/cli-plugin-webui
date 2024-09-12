<script setup lang="ts">
import { useNoneBotStore, useCustomStore } from '@/stores'

const store = useNoneBotStore()
const customStore = useCustomStore()
</script>

<template>
  <div class="badge-items flex items-center gap-2">
    <div v-if="customStore.isDebug" class="badge badge-warning">开发模式</div>
    <div class="badge badge-ghost">当前实例: {{ store.selectedBot?.project_name || '未选择' }}</div>
    <div class="badge badge-ghost">当前环境: {{ store.enabledEnv }}</div>
  </div>
</template>

<style scoped>
.badge-items {
  .badge {
    @apply shrink-0;
  }
}
</style>
