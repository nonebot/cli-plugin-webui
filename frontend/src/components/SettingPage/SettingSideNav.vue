<script setup lang="ts">
import SettingSearch from "@/components/SettingPage/SettingSearch.vue";
import ClassifyNav from "@/components/SettingPage/ClassifyNav.vue";

import { getConfig } from "@/components/SettingPage/client";
import { settingStore } from "@/store/setting";
</script>

<template>
  <div
    :class="{
      'shrink-0 h-full w-72 bg-base-300 flex flex-col flex-nowrap p-2 pb-6 pt-12 md:pt-0': true,
      'transition-all ease-in-out translate-x-0 md:!translate-x-0': true,
      '!translate-x-[-18rem]': !settingStore().sideNavShow,
    }"
  >
    <div class="p-2 flex justify-between items-center">
      <div class="h-8 w-full flex items-center">
        <div class="h-7 w-7 mr-2 rounded bg-base-100 flex items-center justify-center">
          <span class="material-symbols-outlined"> settings </span>
        </div>
        <div class="font-semibold">设置</div>
      </div>
      <div class="h-8 grid grid-cols-2 md:grid-cols-1 gap-4 flex items-center">
        <div
          role="button"
          class="flex items-center justify-center h-7 w-7 rounded hover:bg-base-100 duration-150 hover:ease-in-out"
          @click="getConfig()"
        >
          <span class="material-symbols-outlined"> refresh </span>
        </div>

        <div class="h-full w-7 flex items-center visible md:hidden">
          <span
            role="button"
            class="material-symbols-outlined"
            @click="settingStore().switchNavVisible()"
          >
            close
          </span>
        </div>
      </div>
    </div>

    <SettingSearch />
    <ClassifyNav />
  </div>
</template>
