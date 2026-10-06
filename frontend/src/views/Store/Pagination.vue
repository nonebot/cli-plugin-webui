<script setup lang="ts">
import { ref, watch } from "vue";
import { useSearchStore } from "./client";
import { useNoneBotStore } from "@/stores";

const store = useSearchStore(),
  nonebotStore = useNoneBotStore();

const pages = ref<(string | number)[]>([]);

const generatePageNumbers = (
  currentPage: number,
  totalPage: number,
  maxVisiblePages: number,
) => {
  pages.value = [];
  const range = (start: number, end: number) => {
    const result = [];
    start = start > 0 ? start : 1;
    for (let i = start; i <= end; i++) {
      result.push(i);
    }
    return result;
  };
  if (totalPage < maxVisiblePages) {
    pages.value.push(...range(1, totalPage));
  } else if (currentPage >= 4 && currentPage <= totalPage - 3) {
    const left = currentPage - 1;
    const right = currentPage + 1;

    pages.value.push(1, "...", ...range(left, right), "...", totalPage);
  } else if (currentPage >= totalPage - 5) {
    pages.value.push(1, "...", ...range(totalPage - 3, totalPage));
  } else {
    pages.value.push(...range(1, 4), "...", totalPage);
  }
};

generatePageNumbers(store.nowPage, store.totalPage, 7);

watch(
  () => [store.nowPage, store.totalPage],
  () => {
    generatePageNumbers(store.nowPage, store.totalPage, 7);
  },
);
</script>

<template>
  <div class="flex justify-center">
    <div class="flex items-center gap-1 md:gap-2">
      <button
        :class="{
          'btn btn-sm shadow-none px-1': true,
          'btn-disabled': store.nowPage <= 1,
          hidden: store.storeData.length <= 0,
        }"
      >
        <span
          class="material-symbols-outlined"
          @click="
            store.turnPage(store.nowPage - 1, nonebotStore.selectedBot?.project_id ?? '')
          "
        >
          chevron_left
        </span>
      </button>

      <button
        v-for="page in pages"
        :key="page"
        :class="{
          'btn btn-sm shadow-none': true,
          'btn-primary text-base-100': Number(page) === store.nowPage,
        }"
        @click="
          () => {
            if (typeof page === 'number' && nonebotStore.selectedBot) {
              store.turnPage(page, nonebotStore.selectedBot?.project_id);
            }
          }
        "
      >
        {{ page }}
      </button>

      <button
        :class="{
          'btn btn-sm shadow-none px-1': true,
          'btn-disabled': store.nowPage >= store.totalPage,
          hidden: store.storeData.length <= 0,
        }"
        @click="
          store.turnPage(store.nowPage + 1, nonebotStore.selectedBot?.project_id ?? '')
        "
      >
        <span class="material-symbols-outlined"> chevron_right </span>
      </button>
    </div>
  </div>
</template>

<style scoped>
.material-symbols-outlined {
  font-variation-settings:
    "FILL" 0,
    "wght" 300,
    "GRAD" -25,
    "opsz" 24;
}
</style>
