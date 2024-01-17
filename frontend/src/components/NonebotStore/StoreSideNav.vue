<script setup lang="ts">
import FilterNav from "@/components/NonebotStore/FilterNav.vue";

import { ref, watch } from "vue";
import { appStore } from "@/store/global";
import { nonebotExtensionStore } from "@/store/extensionStore";

const tagOfAuthorInput = ref(""),
  tagOfLabelInput = ref("");

const extStore = nonebotExtensionStore();

const checkDelete = (e: KeyboardEvent) => {
  const { searchTags, removeSearchTag } = nonebotExtensionStore();

  if (e.key === "Backspace" && !extStore.searchInput) {
    const lastTag = searchTags[searchTags.length - 1];
    removeSearchTag(lastTag);
  }
};

const checkTagOfAuthorInput = (e: KeyboardEvent) => {
  if (e.key === "Enter") {
    nonebotExtensionStore().addSearchTag({
      label: "author",
      text: tagOfAuthorInput.value,
    });
    tagOfAuthorInput.value = "";
  }
};

const checkTagOfLabelInput = (e: KeyboardEvent) => {
  if (e.key === "Enter") {
    nonebotExtensionStore().addSearchTag({
      label: "tag",
      text: tagOfLabelInput.value,
    });
    tagOfLabelInput.value = "";
  }
};

const doSearch = async () => {
  await nonebotExtensionStore().updateDataBySearch(appStore().choiceProject.project_id);
};

watch(
  () => extStore.searchInput,
  async () => {
    await doSearch();
  },
);

watch(
  () => nonebotExtensionStore().searchTags.length,
  async () => {
    await doSearch();
  },
);
</script>

<template>
  <div
    :class="{
      'shrink-0 h-full w-72 bg-base-300 flex flex-col flex-nowrap p-2 pb-6 pt-12 md:pt-0': true,
      'transition-all ease-in-out translate-x-0 md:!translate-x-0': true,
      '!translate-x-[-18rem]': !nonebotExtensionStore().sideNavShow,
    }"
  >
    <div class="p-2 flex justify-between items-center">
      <div class="h-8 w-full flex items-center">
        <div class="h-7 w-7 mr-2 rounded bg-base-100 flex items-center justify-center">
          <span class="material-symbols-outlined"> space_dashboard </span>
        </div>
        <div class="font-semibold">拓展商店</div>
      </div>
      <div class="h-8 grid grid-cols-2 md:grid-cols-1 gap-4 flex items-center">
        <div
          role="button"
          class="flex items-center justify-center h-7 w-7 rounded hover:bg-base-100 duration-150 hover:ease-in-out"
          @click="nonebotExtensionStore().updateData(appStore().choiceProject.project_id)"
        >
          <span class="material-symbols-outlined"> refresh </span>
        </div>

        <div class="h-full w-7 flex items-center visible md:hidden">
          <span
            role="button"
            class="material-symbols-outlined"
            @click="nonebotExtensionStore().switchNavVisible()"
          >
            close
          </span>
        </div>
      </div>
    </div>

    <div class="p-2">
      <div
        class="w-full p-1.5 flex flex-wrap items-center bg-white rounded-lg gap-x-0.5 gap-y-0.5"
      >
        <div
          role="button"
          v-for="tag in nonebotExtensionStore().searchTags"
          class="badge badge-primary"
          @click="nonebotExtensionStore().removeSearchTag(tag)"
        >
          <span v-if="tag.label === 'author'">author:@{{ tag.text }}</span>
          <span v-else-if="tag.label === 'tag'">tag:{{ tag.text }}</span>
          <span v-else>is:{{ tag.label }}</span>
        </div>
        <input
          v-model="extStore.searchInput"
          @keydown="checkDelete"
          type="text"
          placeholder="键入以搜索"
          class="input input-xs input-ghost !outline-none flex-1 text-sm p-0 min-w-1"
        />
      </div>
    </div>

    <div class="p-2 flex gap-2">
      <div class="dropdown">
        <div tabindex="0" role="button" class="btn btn-xs btn-outline btn-primary">
          <div class="flex gap-1 items-center">
            <span class="material-symbols-outlined text-base"> person </span>
            作者
          </div>
        </div>
        <div
          tabindex="0"
          class="dropdown-content z-[1] p-2 shadow bg-base-100 rounded-lg"
        >
          <input
            @keydown="checkTagOfAuthorInput"
            v-model="tagOfAuthorInput"
            placeholder="请键入"
            class="input input-sm input-bordered"
          />
        </div>
      </div>

      <div class="dropdown">
        <div tabindex="0" role="button" class="btn btn-xs btn-outline btn-primary">
          <div class="flex gap-1 items-center">
            <span class="material-symbols-outlined text-base"> sell </span>
            标签
          </div>
        </div>
        <div
          tabindex="0"
          class="dropdown-content z-[1] p-2 shadow bg-base-100 rounded-lg"
        >
          <input
            @keydown="checkTagOfLabelInput"
            v-model="tagOfLabelInput"
            placeholder="请键入"
            class="input input-sm input-bordered"
          />
        </div>
      </div>
    </div>

    <FilterNav />
  </div>
</template>
