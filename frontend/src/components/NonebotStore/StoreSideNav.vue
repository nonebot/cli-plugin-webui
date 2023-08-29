<script setup lang="ts">
import StoreSearch from "@/components/NonebotStore/StoreSearch.vue";
import FilterNav from "@/components/NonebotStore/FilterNav.vue";
import ExtensionIcon from "../Icons/ExtensionIcon.vue";
import RefreshIcon from "@/components/Icons/RefreshIcon.vue";
import CloseIcon from "../Icons/CloseIcon.vue";

import { nonebotExtensionStore } from "@/store/extensionStore";
</script>

<template>
  <div
    :class="{
      'shrink-0 h-full w-72 bg-base-300 flex flex-col flex-nowarp p-2 pb-6 pt-12 md:pt-0': true,
      'transition-all ease-in-out translate-x-0 md:!translate-x-0': true,
      '!translate-x-[-18rem]': !nonebotExtensionStore().sideNavShow,
    }"
  >
    <div class="p-2 flex justify-between items-center">
      <div class="h-8 w-full flex items-center">
        <div
          class="h-7 w-7 mr-2 rounded bg-base-100 flex items-center justify-center"
        >
          <ExtensionIcon class="h-6 w-6" />
        </div>
        <div class="font-semibold">拓展商店</div>
      </div>
      <div class="h-8 grid grid-cols-2 md:grid-cols-1 gap-4">
        <div
          role="button"
          class="h-full w-7 flex items-center justify-center rounded-lg hover:bg-neutral-content duration-150 hover:ease-in-out"
          @click="nonebotExtensionStore().refresh()"
        >
          <RefreshIcon class="h-5 w-5 rounded-lg" />
        </div>

        <div class="h-full w-7 flex items-center visible md:hidden">
          <CloseIcon
            role="button"
            class="h-6 w-6"
            @click="nonebotExtensionStore().switchNavVisible()"
          />
        </div>
      </div>
    </div>

    <StoreSearch />
    <FilterNav />
  </div>
</template>
