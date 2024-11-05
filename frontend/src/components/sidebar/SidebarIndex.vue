<script setup lang="ts">
import SideMenu from "@/components/sidebar/SideMenu.vue";
import router from "@/router";
import { useCustomStore } from "@/stores";

const store = useCustomStore();
</script>

<template>
  <div class="fixed lg:relative z-20 top-0 left-0 flex h-full overflow-hidden">
    <Transition>
      <div
        v-show="store.menuShow"
        role="button"
        class="h-screen w-screen bg-gray-500/50 hidden md:block lg:hidden"
        @click="store.toggleMenuShow()"
      ></div>
    </Transition>

    <div
      :class="{
        'fixed lg:relative top-0 left-0 h-full flex flex-col justify-between py-2 px-4 transition-all': true,
        '-translate-x-full lg:translate-x-0 bg-base-200 lg:bg-base-200/50 shadow-md': true,
        '!-translate-x-0': store.menuShow,
        'lg:!w-20': store.menuMinify,
      }"
      class="w-full md:w-1/2 lg:w-72"
    >
      <div class="flex items-center justify-between relative">
        <div
          role="button"
          class="flex items-center gap-2"
          @click="router.push('/'), store.toggleMenuShow()"
        >
          <div class="indicator">
            <span
              v-if="store.isDebug"
              class="indicator-item indicator-middle indicator-center material-symbols-outlined"
            >
              build
            </span>
            <span class="flex-shrink-0 material-symbols-outlined text-primary text-5xl">
              circle
            </span>
          </div>

          <div
            class="shrink-0 text-xl font-semibold leading-7 normal-case"
            :class="{ 'visible lg:invisible': store.menuMinify }"
          >
            NoneBot
          </div>
        </div>

        <button
          :class="{
            'btn btn-sm btn-square btn-ghost flex items-center justify-center': true,
            'block lg:hidden': true,
          }"
          @click="store.toggleMenuShow()"
        >
          <span class="material-symbols-outlined text-2xl"> arrow_back_ios_new </span>
        </button>
      </div>

      <SideMenu />
    </div>
  </div>
</template>

<style scoped>
.material-symbols-outlined {
  font-variation-settings:
    "FILL" 0,
    "wght" 300,
    "GRAD" -25,
    "opsz" 48;
}

.v-enter-active,
.v-leave-active {
  transition: opacity 150ms ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}
</style>
