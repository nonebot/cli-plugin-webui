<script setup lang="ts">
import GeneralConfigTemplate from "@/components/SettingPage/GeneralConfigTemplate.vue";

import { settingStore } from "@/store/setting";
import { hideScrollBarWhileSwiping } from "@/utils/scrollbar";
import { onMounted, ref } from "vue";

const bar = ref<HTMLElement>();
const content = ref<HTMLElement>();

onMounted(() => {
  hideScrollBarWhileSwiping(bar.value!, content.value!);
});
</script>

<template>
  <div class="h-full w-full flex flex-col flex-nowrap">
    <div
      ref="bar"
      :class="{
        'h-12 w-full pl-6 pr-6 pt-3 pb-3': true,
        'z-[5] border-b border-[hsl(var(--b3))] bg-base-100 flex items-center md:shadow-none absolute md:relative': true,
        'translate-y-0 md:!translate-y-0 transition-all ease-in-out': true,
      }"
    >
      <div class="flex items-center">
        <span class="material-symbols-outlined mr-2"> settings </span>
        <div class="text-lg font-bold whitespace-nowrap">设置</div>
      </div>

      <div class="w-full"></div>

      <span
        role="button"
        class="material-symbols-outlined flex items-center visible md:hidden"
        @click="settingStore().switchNavVisible()"
      >
        menu
      </span>
    </div>

    <div
      ref="content"
      class="custom-y-scrollbar w-full p-6 overflow-y-auto pt-[4.5rem] md:pt-6"
    >
      <div id="show-area-top"></div>

      <GeneralConfigTemplate :config="settingStore().webuiConfigList" />
      <GeneralConfigTemplate :config="settingStore().projectMetaConfigList" />
      <GeneralConfigTemplate :config="settingStore().nonebotConfigList" />
      <GeneralConfigTemplate :config="settingStore().pluginConfigList" />
    </div>
  </div>
</template>
