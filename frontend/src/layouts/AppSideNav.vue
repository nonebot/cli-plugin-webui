<script setup lang="ts">
import NonebotIcon from "@/components/svgs/NonebotIcon.vue";
import PluginIcon from "@/components/svgs/PluginIcon.vue";
import { ref } from "vue";
import { routerTo, isEqual } from "@/core/utils";
import { globalStore } from "@/store/app";

interface navItem {
  tip: string;
  icon: any;
  to: string;
}

const navList: navItem[] = [
  { tip: "主页", icon: NonebotIcon, to: "/" },
  { tip: "插件列表", icon: PluginIcon, to: "/plugin" },
];
const activeNav = ref(null as navItem | null);

const nowRoute = window.location.pathname;
const _activeNav: navItem = navList.find((navItem) => nowRoute === navItem.to)!;
if (activeNav) {
  activeNav.value = _activeNav;
}

const setActiveNav = (item: navItem) => {
  if (globalStore().choiceProjectID === "") {
    return;
  }

  activeNav.value = item;
};
</script>

<template>
  <div class="side-nav">
    <ul class="w-full menu p-0 [&_li>*]:rounded-none">
      <li
        :class="{ 'side-nav-active': isEqual(nav, activeNav) }"
        v-for="nav in navList"
        :key="nav.tip"
        @click="setActiveNav(nav), routerTo(nav.to)"
      >
        <a
          class="nav-custom-style tooltip tooltip-right flex items-center justify-center"
          :data-tip="nav.tip"
        >
          <component :is="nav.icon" class="nav-icon h-9 w-9" />
        </a>
      </li>
    </ul>
  </div>
</template>

<style>
.side-nav {
  height: 100%;
  width: 55px;

  display: flex;
  flex-direction: column;
  align-items: center;

  background: hsl(var(--b2));
}

.side-nav > ul > li {
  opacity: 0.35;

  transition: opacity 0.2s ease-in-out;
}

.side-nav > ul > li:hover {
  opacity: 1;
}

.nav-custom-style {
  max-width: 55px;

  padding-left: 0;
  padding-right: 0;
}

.side-nav
  .menu
  :where(
    li:not(.menu-title):not(.disabled) > *:not(ul):not(details):not(.menu-title)
  ):active {
  background-color: initial;
}

.side-nav
  .menu
  :where(
    li:not(.menu-title):not(.disabled) > *:not(ul):not(details):not(.menu-title)
  ):hover {
  background-color: initial;
}

.side-nav-active {
  opacity: 1 !important;
}
</style>
