<script setup lang="ts">
import { useToastStore, type ToastItem } from "@/stores";

defineProps<{ data: ToastItem }>();

const store = useToastStore();
</script>

<template>
  <div class="p-4 bg-base-100 shadow-xl rounded-lg max-w-96 min-w-60 flex flex-col gap-2">
    <div class="flex gap-2 justify-between">
      <div class="flex gap-2 text-wrap">
        <span
          v-if="data.type === 'success'"
          class="material-symbols-outlined text-success"
        >
          check_circle
        </span>
        <span
          v-else-if="data.type === 'error'"
          class="material-symbols-outlined text-error"
        >
          cancel
        </span>
        <span
          v-else-if="data.type === 'info'"
          class="material-symbols-outlined text-info"
        >
          info
        </span>
        <span
          v-else-if="data.type === 'warning'"
          class="material-symbols-outlined text-warning"
        >
          error
        </span>

        <p class="text-sm flex items-center break-all">{{ data.message }}</p>
      </div>
      <div class="btn btn-xs btn-square btn-ghost" @click="store.remove(data.id)">
        <span class="material-symbols-outlined"> close </span>
      </div>
    </div>

    <div v-if="data.from" class="text-xs">From: {{ data.from }}</div>
  </div>
</template>

<style lang="css" scoped>
.material-symbols-outlined {
  font-variation-settings:
    "FILL" 0,
    "wght" 400,
    "GRAD" 0,
    "opsz" 20;
}
</style>
