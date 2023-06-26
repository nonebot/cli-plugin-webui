<script setup lang="ts">
import NonebotIcon from "@/components/svgs/NonebotIcon.vue";
import PluginIcon from "@/components/svgs/PluginIcon.vue";
import { ref, computed } from "vue";
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

const toggleMenu = () => {
  globalStore().showMenu = !globalStore().showMenu;
};
const showMenu = computed(() => globalStore().showMenu);
</script>

<template>
  <Transition>
    <div
      v-if="showMenu"
      :class="{
        'z-20 h-full flex': true,
        'max-[390px]:w-full max-[390px]:fixed max-[390px]:backdrop-blur-sm side-nav-backdrop-background': true,
        'max-[390px]:hidden': !showMenu,
      }"
    >
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
      <div
        class="h-full"
        style="width: calc(100% - 55px)"
        @click="toggleMenu()"
      ></div>
    </div>
  </Transition>
</template>

<style>
.v-enter-active,
.v-leave-active {
  transition: opacity 0.2s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}

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

.side-nav-backdrop-background {
  background-color: rgba(128, 128, 128, 0.5);
}
</style>
