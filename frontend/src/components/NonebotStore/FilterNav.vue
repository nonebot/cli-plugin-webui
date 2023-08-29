<script setup lang="ts">
import OfficialCheckIcon from "@/components/Icons/OfficialCheckIcon.vue";
import CheckCircleIcon from "@/components/Icons/CheckCircleIcon.vue";
import DownloadIcon from "@/components/Icons/DownloadIcon.vue";
import FeatureIcon from "@/components/Icons/FeatureIcon.vue";
import PluginIcon from "@/components/Icons/PluginIcon.vue";
import AdapterIcon from "@/components/Icons/AdapterIcon.vue";
import DriverIcon from "@/components/Icons/DriverIcon.vue";

import { nonebotExtensionStore } from "@/store/extensionStore";
import { appStore } from "@/store/global";

interface CustomDetail {
  tip: string;
  name: string;
  icon: any;
}

const classList: CustomDetail[] = [
  { tip: "插件", name: "plugin", icon: PluginIcon },
  { tip: "适配器", name: "adapter", icon: AdapterIcon },
  { tip: "驱动器", name: "driver", icon: DriverIcon },
];

const filterList: CustomDetail[] = [
  { tip: "官方认证", name: "official", icon: OfficialCheckIcon },
  { tip: "测试通过", name: "valid", icon: CheckCircleIcon },
  { tip: "已下载", name: "downloaded", icon: DownloadIcon },
  { tip: "近期新增", name: "new", icon: FeatureIcon },
];

const setActiveClass = (cls: string) => {
  nonebotExtensionStore().assignClass(cls);
  if (appStore().choiceProject.project_id) {
    nonebotExtensionStore().updateData(appStore().choiceProject.project_id, 0);
  }
};

const addFilter = (item: CustomDetail) => {
  let beforeInput;
  const ft = `is:${item.name}`;
  if (nonebotExtensionStore().searchInput.includes(ft)) {
    const beforeInput = nonebotExtensionStore().searchInput;
    nonebotExtensionStore().searchInput = beforeInput.replace(ft, "").trim();
  } else {
    beforeInput = nonebotExtensionStore().searchInput;
    nonebotExtensionStore().searchInput = `${ft} ${beforeInput}`;
  }
};

const checkFilter = (item: CustomDetail) => {
  const ft = `is:${item.name}`;
  if (nonebotExtensionStore().searchInput.includes(ft)) {
    return true;
  } else {
    return false;
  }
};
</script>

<template>
  <div class="w-full mt-6">
    <ul class="menu w-full">
      <li>
        <div class="text-sm font-bold pointer-events-none">分类</div>
      </li>
      <li v-for="i in classList" @click="setActiveClass(i.name)">
        <a
          :class="{
            'pl-6': true,
            active: nonebotExtensionStore().choiceClass === i.name,
          }"
        >
          <component :is="i.icon" class="h-4 w-4" />
          {{ i.tip }}
        </a>
      </li>
    </ul>

    <ul class="menu w-full">
      <li>
        <div class="font-bold pointer-events-none">筛选</div>
      </li>
      <li v-for="i in filterList" @click="addFilter(i)">
        <a :class="{ 'pl-6': true, active: checkFilter(i) }">
          <component :is="i.icon" class="h-4 w-4" />
          {{ i.tip }}
        </a>
      </li>
    </ul>
  </div>
</template>
