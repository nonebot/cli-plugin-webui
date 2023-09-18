<script setup lang="ts">
import GeneralConfigTemplate from "@/components/SettingPage/GeneralConfigTemplate.vue";
import SettingIcon from "../Icons/SettingIcon.vue";
import MenuIcon from "../Icons/MenuIcon.vue";

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
        <SettingIcon class="h-6 w-6 mr-2" />
        <div class="text-lg font-bold whitespace-nowrap">设置</div>
      </div>

      <div class="w-full"></div>

      <MenuIcon
        role="button"
        class="h-9 w-9 visible md:hidden"
        @click="settingStore().switchNavVisible()"
      />
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

<style>
.setting-board-title,
.setting-board-father,
.setting-board-child,
.more-action {
  transition-property: all;
  transition-duration: 150ms;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}

.setting-board-desc {
  font-size: 0.875rem;
  line-height: 1.25rem;
}

.setting-board-title {
  font-size: 1.5rem;
  line-height: 2rem;
  font-weight: 800;
  border-radius: 0.25rem;
}

.setting-board-father-title {
  font-size: 1.25rem;
  line-height: 1.75rem;
  font-weight: 800;
}

.setting-board-child {
  position: relative;
}

.setting-board-child-title {
  position: relative;
  display: flex;
  align-items: center;
}

.setting-board-child-title > span {
  font-weight: 700;
}

.setting-board-child-content {
  padding-top: 1rem;
}

.more-action {
  left: -2.25rem;
  height: 1.25rem;
  width: 1.25rem;
  opacity: 0;
  position: absolute;
}

.more-action:hover {
  border-radius: 0.25rem;
  background: hsl(var(--nc));
}

.setting-board-child:hover .more-action {
  opacity: 1;
}

.setting-board-child-content .form-control .label {
  justify-content: start;
}

.setting-board-child-content .form-control .label .checkbox {
  margin-right: 0.5rem;
}
</style>
