<script setup lang="ts">
import { useNoneBotStore, useCustomStore } from '@/stores'

const store = useNoneBotStore()
const customStore = useCustomStore()
</script>

<template>
  <div class="badge-items flex items-center gap-2">
    <div v-if="customStore.isDebug" class="badge badge-warning">开发模式</div>
    <div v-if="store.selectedBot" class="badge badge-ghost">
      当前实例: {{ store.selectedBot?.project_name }}
    </div>
    <div v-if="store.selectedBot" class="badge badge-ghost">
      当前环境: {{ store.selectedBot?.use_env }}
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
