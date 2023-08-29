<script setup lang="ts">
import { nonebotExtensionStore } from "@/store/extensionStore";
import { appStore } from "@/store/global";
import { ref, watch } from "vue";

const inputValue = ref("");

const doSearch = async () => {
  await nonebotExtensionStore().updateDataBySearch(
    appStore().choiceProject.project_id,
  );
};

watch(inputValue, () => {
  nonebotExtensionStore().searchInput = inputValue.value;
});

watch(
  () => nonebotExtensionStore().searchInput,
  async () => {
    inputValue.value = nonebotExtensionStore().searchInput;
    await doSearch();
  },
);
</script>

<template>
  <div class="w-full p-2">
    <div class="relative">
      <input
        v-model="inputValue"
        type="text"
        placeholder="键入以搜索"
        class="input input-sm rounded w-full"
      />
    </div>
  </div>
</template>
