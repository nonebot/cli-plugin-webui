<script setup lang="ts">
import SettingSideNav from "./SettingPage/SettingSideNav.vue";
import SettingShowArea from "./SettingPage/SettingShowArea.vue";

import { getConfig } from "@/components/SettingPage/client";
import { onMounted } from "vue";
import { settingStore } from "@/store/setting";

onMounted(() => {
  getConfig();
});
</script>

<template>
  <div class="overflow-hidden h-full w-full flex">
    <div
      :class="{
        'z-10 h-full w-full top-0 left-0 shrink-0 flex md:w-72 visible md:!visible absolute md:relative': true,
        'transition-all duration-100 ease-in-out': true,
        '!bg-inherit !invisible': !settingStore().sideNavShow,
      }"
      style="background-color: hsl(var(--n) / 0.3)"
    >
      <SettingSideNav />

      <button
        :class="{
          'h-full w-full flex md:hidden opacity-30': true,
          '!hidden': !settingStore().sideNavShow,
        }"
        @click="settingStore().switchNavVisible()"
      ></button>
    </div>

    <SettingShowArea />
  </div>
</template>
