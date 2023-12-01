<script setup lang="ts">
import StoreSearch from "@/components/NonebotStore/StoreSearch.vue";
import FilterNav from "@/components/NonebotStore/FilterNav.vue";

import { appStore } from "@/store/global";
import { nonebotExtensionStore } from "@/store/extensionStore";
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

    <StoreSearch />
    <FilterNav />
  </div>
</template>
