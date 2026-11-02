<script setup lang="ts">
import ExtensionCard from "./ExtensionCard.vue";
import { useSearchStore } from "./client";

const store = useSearchStore();
</script>

<template>
  <div
    v-if="store.storeData.length > 0"
    class="relative grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 grid-rows-auto gap-6"
  >
    <div
      v-if="store.isRequesting"
      class="absolute z-20 top-1/4 right-1/2 flex items-center gap-4 translate-x-1/2 translate-y-1/2"
    >
      搜索中...
      <span class="loading loading-spinner loading-md text-primary"></span>
    </div>
    <div
      v-for="data in store.storeData"
      :key="data.name"
      :class="{ 'blur-sm pointer-events-none': store.isRequesting }"
    >
      <ExtensionCard :data="data" />
    </div>
  </div>
  <div v-else class="text-center">没有结果。</div>
</template>
