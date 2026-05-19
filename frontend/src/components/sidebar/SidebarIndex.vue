<script setup lang="ts">
import { computed } from "vue";
import SideMenu from "@/components/sidebar/SideMenu.vue";
import router from "@/router";
import { useCustomStore } from "@/stores";

const store = useCustomStore();

const sidebarClasses = computed(() => ({
  "fixed lg:relative top-0 left-0 h-full flex flex-col justify-between py-2 px-4 transition-all": true,
  "overflow-visible lg:overflow-hidden": !store.menuMinify,
  "lg:overflow-visible": store.menuMinify,
  "bg-base-200 lg:bg-base-200/50 shadow-md": true,
  "lg:!w-20": store.menuMinify,
}));
</script>

<template>
  <div class="fixed lg:relative z-20 top-0 left-0 flex h-full">
    <Transition>
      <div
        v-show="store.menuShow"
        role="button"
        class="h-screen w-screen bg-gray-500/50 block lg:hidden"
        @click="store.toggleMenuShow()"
      ></div>
    </Transition>

    <div
      :class="sidebarClasses"
      :style="{ transform: store.menuShow ? 'translateX(0)' : 'translateX(-100%)' }"
      class="w-full md:w-1/2 lg:w-72 lg:!transform-none"
    >
      <div
        :class="{
          'flex items-center relative': true,
          'justify-between': !store.menuMinify,
          'lg:justify-start lg:gap-5': store.menuMinify,
        }"
      >
        <div
          role="button"
          class="flex items-center gap-2 lg:gap-0.5"
          @click="(router.push('/'), store.toggleMenuShow())"
        >
          <div class="relative flex items-center justify-center">
            <span
              v-if="store.isDebug"
              class="absolute z-10 material-symbols-outlined text-2xl"
            >
              build
            </span>
            <span class="flex-shrink-0 material-symbols-outlined text-primary text-5xl">
              circle
            </span>
          </div>

          <div
            class="shrink-0 text-xl font-semibold leading-7 normal-case"
            :class="{ 'visible lg:hidden': store.menuMinify }"
          >
            NoneBot
          </div>
        </div>

        <div class="flex items-center ml-auto">
          <button
            class="btn btn-sm btn-square btn-ghost flex items-center justify-center lg:hidden"
            @click="store.toggleMenuShow()"
          >
            <span class="material-symbols-outlined text-2xl"> arrow_back_ios_new </span>
          </button>
          <button
            :class="{
              'btn btn-sm btn-square btn-ghost hidden lg:flex items-center justify-center': true,
              '-scale-100': store.menuMinify,
            }"
            @click="store.toggleMenuMinify()"
          >
            <span class="material-symbols-outlined text-2xl"> menu_open </span>
          </button>
        </div>
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
