<script setup lang="ts">
import { useRoute } from "vue-router";
import { useCustomStore, useViewHistoryRecorderStore } from "@/stores";
import { defaultRoutes, type NavItem } from "@/router/client";

const currentRoute = useRoute();
const store = useViewHistoryRecorderStore();
const customStore = useCustomStore();

const recordView = (navItem: NavItem) => {
  if (
    store.viewHistory.some((i: NavItem) => i.routeData.path === navItem.routeData.path)
  ) {
    return;
  }
  store.record(navItem);
};
</script>

<template>
  <ul class="h-full pt-8 px-0 menu rounded-box">
    <li
      v-for="navItem in defaultRoutes"
      :key="navItem.name"
      class="mb-2"
      @click="recordView(navItem)"
    >
      <RouterLink
        :to="navItem.routeData.path"
        class="btn btn-block relative overflow-hidden"
        :class="{
          active: navItem.routeData.path === currentRoute.path,
        }"
        @click="customStore.toggleMenuShow()"
      >
        <span class="material-symbols-outlined absolute left-3 flex-shrink-0">{{
          navItem.googleIcon
        }}</span>
        <span
          class="absolute left-14 transition-opacity duration-200"
          :class="
            customStore.menuMinify ? 'lg:opacity-0 lg:pointer-events-none' : 'opacity-100'
          "
          >{{ navItem.name }}</span
        >
      </RouterLink>
    </li>
  </ul>
</template>

<style scoped>
.material-symbols-outlined {
  font-variation-settings:
    "FILL" 0,
    "wght" 300,
    "GRAD" -25,
    "opsz" 48;
}

.menu li > *:not(ul, .menu-title, details, .btn):active,
.menu li > *:not(ul, .menu-title, details, .btn).active,
.menu li > details > summary:active {
  --tw-bg-opacity: 0.2;
  --tw-text-opacity: 0.8;
  background-color: var(--fallback-n, oklch(var(--p) / var(--tw-bg-opacity)));
  color: var(--fallback-nc, oklch(var(--p) / var(--tw-text-opacity)));
}
</style>
