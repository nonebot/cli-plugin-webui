<script setup lang="ts">
import SearchBar from "./SearchBar.vue";
import ExtensionContainer from "./ExtensionContainer.vue";
import Pagination from "./Pagination.vue";
import { useSearchStore } from "./client";
import { onMounted } from "vue";
import { useNoneBotStore, useToastStore } from "@/stores";

const store = useSearchStore(),
  nonebotStore = useNoneBotStore();

const toast = useToastStore();

onMounted(async () => {
  if (!nonebotStore.selectedBot) {
    toast.add("warning", "未选择实例", "", 5000);
    return;
  }
  await store.updateData(nonebotStore.selectedBot.project_id, false);
});
</script>

<template>
  <div class="flex flex-col gap-6">
    <SearchBar />

    <Pagination />

    <ExtensionContainer />

    <Pagination />
  </div>
</template>
