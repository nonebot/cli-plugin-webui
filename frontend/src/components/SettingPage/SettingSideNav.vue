<script setup lang="ts">
import SettingSearch from "@/components/SettingPage/SettingSearch.vue";
import ClassifyNav from "@/components/SettingPage/ClassifyNav.vue";
import RefreshIcon from "@/components/Icons/RefreshIcon.vue";
import SettingIcon from "../Icons/SettingIcon.vue";
import CloseIcon from "../Icons/CloseIcon.vue";

import { getConfig } from "@/components/SettingPage/client";
import { settingStore } from "@/store/setting";
</script>

<template>
  <div
    :class="{
      'shrink-0 h-full w-72 bg-base-300 flex flex-col flex-nowarp p-2 pb-6 pt-12 md:pt-0': true,
      'transition-all ease-in-out translate-x-0 md:!translate-x-0': true,
      '!translate-x-[-18rem]': !settingStore().sideNavShow,
    }"
  >
    <div class="p-2 flex justify-between items-center">
      <div class="h-8 w-full flex items-center">
        <div
          class="h-7 w-7 mr-2 rounded bg-base-100 flex items-center justify-center"
        >
          <SettingIcon class="h-6 w-6" />
        </div>
        <div class="font-semibold">设置</div>
      </div>
      <div class="h-8 grid grid-cols-2 md:grid-cols-1 gap-4">
        <div
          role="button"
          class="h-full w-7 flex items-center justify-center rounded-lg hover:bg-neutral-content duration-150 hover:ease-in-out"
          @click="getConfig()"
        >
          <RefreshIcon class="h-5 w-5 rounded-lg" />
        </div>

        <div class="h-full w-7 flex items-center visible md:hidden">
          <CloseIcon
            role="button"
            class="h-6 w-6"
            @click="settingStore().switchNavVisible()"
          />
        </div>
      </div>
    </div>

    <SettingSearch />
    <ClassifyNav />
  </div>
</template>
