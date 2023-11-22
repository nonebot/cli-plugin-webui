<script setup lang="ts">
import { nonebotExtensionStore } from "@/store/extensionStore";
import { appStore } from "@/store/global";

interface CustomDetail {
  tip: string;
  name: string;
  icon: any;
}

const classList: CustomDetail[] = [
  { tip: "插件", name: "plugin", icon: "extension" },
  { tip: "适配器", name: "adapter", icon: "lan" },
  { tip: "驱动器", name: "driver", icon: "electrical_services" },
];

const filterList: CustomDetail[] = [
  { tip: "官方认证", name: "official", icon: "verified" },
  { tip: "测试通过", name: "valid", icon: "check_circle" },
  { tip: "已下载", name: "downloaded", icon: "download" },
  { tip: "近期新增", name: "new", icon: "shadow_add" },
];

const setActiveClass = (cls: string) => {
  nonebotExtensionStore().nowPage = 0;
  nonebotExtensionStore().assignClass(cls);
  if (appStore().choiceProject.project_id) {
    nonebotExtensionStore().updateData(appStore().choiceProject.project_id);
  }
};

const addFilter = (item: CustomDetail) => {
  nonebotExtensionStore().nowPage = 0;
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
          <span class="material-symbols-outlined text-xl leading-5">
            {{ i.icon }}
          </span>
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
          <span class="material-symbols-outlined text-xl leading-5">
            {{ i.icon }}
          </span>
          {{ i.tip }}
        </a>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.material-symbols-outlined {
  font-variation-settings:
    "FILL" 1,
    "wght" 300,
    "GRAD" 0,
    "opsz" 40;
}
</style>
