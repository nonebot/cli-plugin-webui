<script setup lang="ts">
import { ref, watch } from "vue";
import { routerTo } from "@/router/client";
import { appStore } from "@/store/global";
import { router } from "@/router";

interface navItem {
  tip: string;
  icon: any;
  iconClass?: string[];
  to: string;
  clickedFunc?: () => void;
}

const topNavList: navItem[] = [
  {
    tip: "主页",
    icon: "circle",
    iconClass: ["text-primary"],
    to: "/",
    clickedFunc: () => {
      routerTo("/");
    },
  },
  { tip: "拓展商店", icon: "space_dashboard", to: "/store" },
  // { tip: "文件管理", icon: "file_copy", to: "/file" },
];

const buttonNavList: navItem[] = [{ tip: "设置", icon: "settings", to: "/setting" }];

const activeNav = ref<string>();
const showMenuModal = ref<HTMLDialogElement>();

const nowRoute = window.location.pathname;
const _activeNav: navItem | undefined = topNavList.find(
  (navItem) => nowRoute === navItem.to,
)!;
if (_activeNav) {
  activeNav.value = _activeNav.to;
}

const logout = () => {
  localStorage.removeItem("jwtToken");
  router.push("/login");
  appStore().isAuth = false;
};

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
      <span
        role="button"
        class="material-symbols-outlined text-4xl mr-4"
        @click="showMenuModal?.showModal()"
      >
        menu
      </span>

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
            <span
              class="material-symbols-outlined text-4xl flex items-center"
              :class="nav.iconClass"
            >
              {{ nav.icon }}
            </span>
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
            <span class="material-symbols-outlined text-4xl" :class="nav.iconClass">
              {{ nav.icon }}
            </span>
          </a>
        </li>
        <li @click="logout()">
          <a
            class="nav-custom-style tooltip tooltip-right flex items-center justify-center"
            data-tip="登出"
          >
            <span class="material-symbols-outlined text-4xl"> logout </span>
          </a>
        </li>
      </ul>
    </div>
  </div>

  <dialog ref="showMenuModal" class="modal">
    <div class="modal-box rounded-lg">
      <h3 class="font-bold text-lg">导航</h3>
      <ul class="menu">
        <li v-for="nav in topNavList" @click="routerTo(nav.to), showMenuModal?.close()">
          <a>
            <span class="material-symbols-outlined" :class="nav.iconClass">
              {{ nav.icon }}
            </span>
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
            <span class="material-symbols-outlined" :class="nav.iconClass">
              {{ nav.icon }}
            </span>
            <span>{{ nav.tip }}</span>
            <div class="w-full"></div>
            <span v-if="activeNav === nav.tip" class="badge bg-base-200">当前位置</span>
          </a>
        </li>
        <li @click="logout()">
          <a>
            <span class="material-symbols-outlined"> logout </span>
            <span>登出</span>
          </a>
        </li>
      </ul>
    </div>
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
