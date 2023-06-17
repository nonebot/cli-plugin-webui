import { createRouter, createWebHistory } from "vue-router";

import LoginPage from "@/components/LoginPage.vue";
import IndexView from "@/components/IndexView.vue";
import HomePage from "@/components/HomePage.vue";
import PluginManage from "@/components/PluginManage.vue";

import { checkTokenValidity } from "@/core/authentication/authUtils";
import { globalLog as log } from "@/main";
import { globalStore } from "@/store/app";

const routes = [
  {
    name: "Login",
    path: "/login",
    component: LoginPage,
  },
  {
    name: "WebUI",
    path: "/",
    component: IndexView,
    children: [
      {
        name: "Home",
        path: "/",
        component: HomePage,
      },
      {
        name: "Plugin",
        path: "/plugin",
        component: PluginManage,
      },
    ],
  },
];

export const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach(async (to, from) => {
  const login = await checkTokenValidity();
  if (!login && to.name !== "Login") {
    log.warning("请先验证");
    router.push("/login");
  }

  if (
    globalStore().choiceProjectID === "" &&
    to.path !== "/" &&
    to.path !== "/login"
  ) {
    log.warning("请先选择一项实例");
    return false;
  }
});
