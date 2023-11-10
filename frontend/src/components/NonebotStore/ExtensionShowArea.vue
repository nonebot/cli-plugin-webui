<script setup lang="ts">
import ExtensionCard from "@/components/NonebotStore/ExtensionCard.vue";

import { ref, computed, watch, onMounted } from "vue";
import { hideScrollBarWhileSwiping } from "@/utils/scrollbar";
import { nonebotExtensionStore } from "@/store/extensionStore";
import { appStore } from "@/store/global";

const titleItems = {
  plugin: { tip: "插件", icon: "extension" },
  adapter: { tip: "适配器", icon: "lan" },
  driver: { tip: "驱动器", icon: "electrical_services" },
};

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

generatePageNumbers(
  nonebotExtensionStore().nowPage,
  nonebotExtensionStore().totalPage,
  7,
);

onMounted(() => {
  hideScrollBarWhileSwiping(bar.value!, content.value!);
});

watch(
  () => nonebotExtensionStore().totalPage,
  () => {
    nonebotExtensionStore().nowPage;
    generatePageNumbers(
      nonebotExtensionStore().nowPage,
      nonebotExtensionStore().totalPage,
      7,
    );
  },
);

watch(
  () => nonebotExtensionStore().nowPage,
  () => {
    if (appStore().choiceProject.project_id) {
      nonebotExtensionStore().updateData(appStore().choiceProject.project_id);
    }

    generatePageNumbers(
      nonebotExtensionStore().nowPage,
      nonebotExtensionStore().totalPage,
      7,
    );
  },
);
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
        <span class="material-symbols-outlined mr-2">
          {{ getTitle.icon }}
        </span>
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

      <span
        role="button"
        class="material-symbols-outlined flex items-center visible md:hidden"
        @click="nonebotExtensionStore().switchNavVisible()"
      >
        menu
      </span>
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
                'btn-disabled': nonebotExtensionStore().nowPage <= 0,
              }"
              @click="
                nonebotExtensionStore().turnPage(nonebotExtensionStore().nowPage - 1)
              "
            >
              «
            </button>

            <button
              v-for="page in pages"
              :class="{
                'join-item btn btn-sm': true,
                'btn-active': page - 1 === nonebotExtensionStore().nowPage,
              }"
              @click="nonebotExtensionStore().turnPage(page - 1)"
            >
              {{ page }}
            </button>

            <button
              :class="{
                'join-item btn btn-sm': true,
                'btn-disabled':
                  nonebotExtensionStore().nowPage ===
                  nonebotExtensionStore().totalPage - 1,
              }"
              @click="
                nonebotExtensionStore().turnPage(nonebotExtensionStore().nowPage + 1)
              "
            >
              »
            </button>
          </div>
        </div>
      </Transition>
    </div>
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
