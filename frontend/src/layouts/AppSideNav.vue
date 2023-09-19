<script setup lang="ts">
import NonebotIcon from "@/components/Icons/NonebotIcon.vue";
import ExtensionIcon from "@/components/Icons/ExtensionIcon.vue";
import AccountLightOutlineIcon from "@/components/Icons/AccountLightOutlineIcon.vue";
import SettingIcon from "@/components/Icons/SettingIcon.vue";
// import FileIcon from "@/components/Icons/FileIcon.vue";

import { ref, watch } from "vue";
import MenuIcon from "@/components/Icons/MenuIcon.vue";
import { routerTo } from "@/router/client";
import { appStore } from "@/store/global";

interface navItem {
  tip: string;
  icon: any;
  to: string;
}

const topNavList: navItem[] = [
  { tip: "主页", icon: NonebotIcon, to: "/" },
  { tip: "拓展商店", icon: ExtensionIcon, to: "/store" },
  // { tip: "文件管理", icon: FileIcon, to: "/file" },
];

const buttonNavList: navItem[] = [
  { tip: "登录设置", icon: AccountLightOutlineIcon, to: "/account" },
  { tip: "设置", icon: SettingIcon, to: "/setting" },
];

const activeNav = ref<string>();
const showMenuModal = ref<HTMLDialogElement>();

const nowRoute = window.location.pathname;
const _activeNav: navItem | undefined = topNavList.find(
  (navItem) => nowRoute === navItem.to,
)!;
if (_activeNav) {
  activeNav.value = _activeNav.to;
}

watch(
  () => appStore().nowPath,
  (value) => {
    activeNav.value = value;
  },
);
</script>

<template>
  <div
    class="z-20 h-auto md:h-full w-full fixed md:w-14 pb-6 transition-all ease-in-out translate-y-0"
  >
    <div
      class="fixed h-12 w-full visible md:invisible flex items-center pl-4 pr-4 border-b border-[hsl(var(--b3))] bg-base-100"
    >
      <MenuIcon
        role="button"
        class="h-full w-9 mr-4"
        @click="showMenuModal?.showModal()"
      />

      <div class="pointer-events-none">{{ activeNav }}</div>
    </div>

    <div class="side-nav relative md:fixed invisible md:!visible hidden md:flex">
      <ul class="w-full menu p-0 [&_li>*]:rounded-none">
        <li
          v-for="nav in topNavList"
          :class="{
            'side-nav-active': activeNav === nav.to,
            disabled: nav.to === '/store' && appStore().choiceProject.use_run_script,
          }"
          @click="
            () => {
              if (
                nav.to !== '/store' ||
                !(nav.to === '/store' && appStore().choiceProject.use_run_script)
              ) {
                routerTo(nav.to);
              }
            }
          "
        >
          <a
            class="nav-custom-style tooltip tooltip-right flex items-center justify-center"
            :data-tip="nav.tip"
          >
            <component :is="nav.icon" class="h-9 w-9" />
          </a>
        </li>
      </ul>

      <div class="h-full"></div>

      <ul class="w-full menu p-0 [&_li>*]:rounded-none">
        <li
          v-for="nav in buttonNavList"
          :class="{ 'side-nav-active': activeNav === nav.to }"
          @click="routerTo(nav.to)"
        >
          <a
            class="nav-custom-style tooltip tooltip-right flex items-center justify-center"
            :data-tip="nav.tip"
          >
            <component :is="nav.icon" class="h-9 w-9" />
          </a>
        </li>
      </ul>
    </div>
  </div>

  <dialog ref="showMenuModal" class="modal">
    <form method="dialog" class="modal-box rounded-lg">
      <h3 class="font-bold text-lg">导航</h3>
      <ul class="menu">
        <li v-for="nav in topNavList" @click="routerTo(nav.to), showMenuModal?.close()">
          <a>
            <component :is="nav.icon" class="h-7 w-7" />
            <span>{{ nav.tip }}</span>
            <div class="w-full"></div>
            <span v-if="activeNav === nav.tip" class="badge bg-base-200">当前位置</span>
          </a>
        </li>
        <li
          v-for="nav in buttonNavList"
          @click="routerTo(nav.to), showMenuModal?.close()"
        >
          <a>
            <component :is="nav.icon" class="h-7 w-7" />
            <span>{{ nav.tip }}</span>
            <div class="w-full"></div>
            <span v-if="activeNav === nav.tip" class="badge bg-base-200">当前位置</span>
          </a>
        </li>
      </ul>
    </form>
    <form method="dialog" class="modal-backdrop">
      <button @click="showMenuModal?.close()">close</button>
    </form>
  </dialog>
</template>

<style scoped>
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
  width: 3.5rem;
  flex-direction: column;
  align-items: center;
  padding-bottom: 1.5rem;
  background: hsl(var(--b2));
}

.side-nav > ul > li,
.side-nav > div {
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
  ):hover,
.side-nav
  .menu
  :where(
    li:not(.menu-title):not(.disabled) > *:not(ul):not(details):not(.menu-title)
  ):active {
  background-color: initial;
}

.side-nav .menu li > *:not(ul):not(.menu-title):not(details):active,
.side-nav .menu li > *:not(ul):not(.menu-title):not(details).active,
.side-nav .menu li > details > summary:active,
.side-nav .menu li > *:not(ul):not(.menu-title):not(details):active,
.side-nav .menu li > *:not(ul):not(.menu-title):not(details).active,
.side-nav .menu li > details > summary:active {
  background-color: initial;
}

.side-nav-active {
  opacity: 1 !important;
}
</style>
