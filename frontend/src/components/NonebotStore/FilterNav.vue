<script setup lang="ts">
import { nonebotExtensionStore } from "@/store/extensionStore";
import { SearchTag } from "@/api/schemas";
import { appStore } from "@/store/global";

interface CustomDetail {
  tip: string;
  name: string;
  icon: any;
}

interface FilterDetail extends CustomDetail {
  tag: SearchTag;
}

const moduleList: CustomDetail[] = [
  { tip: "插件", name: "plugin", icon: "extension" },
  { tip: "适配器", name: "adapter", icon: "lan" },
  { tip: "驱动器", name: "driver", icon: "electrical_services" },
];

const filterList: FilterDetail[] = [
  {
    tip: "官方认证",
    name: "official",
    icon: "verified",
    tag: {
      label: "official",
    },
  },
  {
    tip: "测试通过",
    name: "valid",
    icon: "check_circle",
    tag: {
      label: "valid",
    },
  },
  {
    tip: "已下载",
    name: "downloaded",
    icon: "download",
    tag: {
      label: "downloaded",
    },
  },
  {
    tip: "近期新增",
    name: "latest",
    icon: "shadow_add",
    tag: {
      label: "latest",
    },
  },
];

const setActiveClass = (cls: string) => {
  nonebotExtensionStore().turnPage(0);
  nonebotExtensionStore().assignClass(cls);
  nonebotExtensionStore().updateData(appStore().choiceProject.project_id);
};

const addFilter = (item: FilterDetail) => {
  nonebotExtensionStore().turnPage(0);
  if (nonebotExtensionStore().searchTags.includes(item.tag)) {
    nonebotExtensionStore().removeSearchTag(item.tag);
  } else {
    nonebotExtensionStore().addSearchTag(item.tag);
  }
};

const checkModule = (module: string) => {
  return nonebotExtensionStore().choiceModule === module;
};

const checkFilter = (item: FilterDetail) => {
  return nonebotExtensionStore().searchTags.includes(item.tag);
};
</script>

<template>
  <div class="w-full">
    <ul class="menu w-full">
      <li>
        <div class="text-sm font-bold pointer-events-none">分类</div>
      </li>
      <li v-for="m in moduleList" @click="setActiveClass(m.name)">
        <a
          :class="{
            'pl-6': true,
            active: checkModule(m.name),
          }"
        >
          <span class="material-symbols-outlined text-xl leading-5">
            {{ m.icon }}
          </span>
          {{ m.tip }}
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
