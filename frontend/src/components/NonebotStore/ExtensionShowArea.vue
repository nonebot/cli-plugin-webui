<script setup lang="ts">
import ExtensionCard from "@/components/NonebotStore/ExtensionCard.vue";
import PluginIcon from "@/components/Icons/PluginIcon.vue";
import AdapterIcon from "@/components/Icons/AdapterIcon.vue";
import DriverIcon from "@/components/Icons/DriverIcon.vue";
import MenuIcon from "@/components/Icons/MenuIcon.vue";

import { ref, computed, watch, onMounted } from "vue";
import { hideScrollBarWhileSwiping } from "@/utils/scrollbar";
import { nonebotExtensionStore } from "@/store/extensionStore";
import { appStore } from "@/store/global";

const titleItems = {
  plugin: { tip: "插件", icon: PluginIcon },
  adapter: { tip: "适配器", icon: AdapterIcon },
  driver: { tip: "驱动器", icon: DriverIcon },
};

const nowPage = ref(0);
const pages = ref<any[]>([]);
const bar = ref<HTMLElement>();
const content = ref<HTMLElement>();

const getTitle = computed(() => {
  switch (nonebotExtensionStore().choiceClass) {
    case "adapter":
      return titleItems.adapter;
    case "driver":
      return titleItems.driver;
    default:
      return titleItems.plugin;
  }
});

const turnPage = (page: number | string) => {
  if (typeof page !== "number") {
    return;
  }

  if (page >= 0) {
    nowPage.value = page;
  } else {
    nowPage.value = 0;
  }

  if (page >= nonebotExtensionStore().totalPage) {
    nowPage.value = nonebotExtensionStore().totalPage;
  }
};

const generatePageNumbers = (
  currentPage: number,
  totalPages: number,
  maxVisiblePages: number,
) => {
  pages.value = [];
  const range = (start: number, end: number) => {
    const result = [];
    start = start > 0 ? start : 1;
    for (let i = start; i <= end; i++) {
      result.push(i);
    }
    return result;
  };
  if (totalPages < maxVisiblePages) {
    pages.value.push(...range(1, totalPages));
  } else if (currentPage >= 3 && currentPage < totalPages - 3) {
    const left = currentPage;
    const right = currentPage + 2;

    pages.value.push(1, "...", ...range(left, right), "...", totalPages);
  } else if (currentPage >= totalPages - 5) {
    pages.value.push(1, "...", ...range(totalPages - 3, totalPages));
  } else {
    pages.value.push(...range(1, 4), "...", totalPages);
  }
};

generatePageNumbers(nowPage.value, nonebotExtensionStore().totalPage, 7);

onMounted(() => {
  hideScrollBarWhileSwiping(bar.value!, content.value!);
});

watch(
  () => nonebotExtensionStore().totalPage,
  () => {
    nowPage.value = 0;
    generatePageNumbers(nowPage.value, nonebotExtensionStore().totalPage, 7);
  },
);

watch(nowPage, () => {
  if (appStore().choiceProject.project_id) {
    nonebotExtensionStore().updateData(
      appStore().choiceProject.project_id,
      nowPage.value,
    );
  }

  generatePageNumbers(nowPage.value, nonebotExtensionStore().totalPage, 7);
});
</script>

<template>
  <div class="h-full w-full flex flex-col flex-nowarp">
    <div
      ref="bar"
      :class="{
        'h-12 w-full pl-6 pr-6 pt-3 pb-3': true,
        'z-[5] border-b border-[hsl(var(--b3))] bg-base-100 flex items-center md:shadow-none absolute md:relative': true,
        'translate-y-0 md:!translate-y-0 transition-all ease-in-out': true,
      }"
    >
      <div class="flex items-center">
        <component :is="getTitle.icon" class="h-6 w-6 mr-2" />
        <div class="text-lg font-bold whitespace-nowrap">
          {{ getTitle.tip }}
        </div>
        <div class="text-sm whitespace-nowrap">
          （共 {{ nonebotExtensionStore().totalItem }} 个结果）
        </div>
        <span
          v-if="nonebotExtensionStore().requesting"
          class="loading loading-spinner loading-md whitespace-nowrap"
        ></span>
      </div>

      <div class="w-full"></div>

      <MenuIcon
        role="button"
        class="h-9 w-9 visible md:hidden"
        @click="nonebotExtensionStore().switchNavVisible()"
      />
    </div>

    <div
      ref="content"
      class="custom-y-scrollbar overflow-y-scroll grow p-6 pt-[4.5rem] md:pt-6"
    >
      <div class="grid xs:grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        <TransitionGroup name="extension-card">
          <ExtensionCard
            v-for="(data, index) in nonebotExtensionStore().storeData"
            :key="data.module_name"
            :item-data="data"
            :style="{ 'transition-delay': `${index * 30}ms` }"
          />
        </TransitionGroup>
      </div>

      <Transition>
        <div
          v-if="nonebotExtensionStore().totalPage > 1"
          class="flex justify-center items-center pt-6"
        >
          <div class="join">
            <button
              :class="{
                'join-item btn btn-sm': true,
                'btn-disabled': nowPage <= 0,
              }"
              @click="turnPage(nowPage - 1)"
            >
              «
            </button>

            <button
              v-for="page in pages"
              :class="{
                'join-item btn btn-sm': true,
                'btn-active': page - 1 === nowPage,
              }"
              @click="turnPage(page - 1)"
            >
              {{ page }}
            </button>

            <button
              :class="{
                'join-item btn btn-sm': true,
                'btn-disabled':
                  nowPage === nonebotExtensionStore().totalPage - 1,
              }"
              @click="turnPage(nowPage + 1)"
            >
              »
            </button>
          </div>
        </div>
      </Transition>
    </div>
  </div>
</template>

<style>
.extension-card-move,
.extension-card-enter-active,
.extension-card-leave-active {
  transition: all 100ms ease;
}

.extension-card-enter-from,
.extension-card-leave-to {
  opacity: 0;
}

.extension-card-leave-active {
  position: absolute;
}
</style>