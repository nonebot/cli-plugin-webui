import { createRouter, createWebHistory } from "vue-router";

import LoginPage from "@/components/LoginPage.vue";
import IndexView from "@/components/IndexView.vue";
import HomePage from "@/components/HomePage.vue";
import NonebotStore from "@/components/NonebotStore.vue";
import FileExplorer from "@/components/FileExplorer.vue";
import SettingPage from "@/components/SettingPage.vue";

import { checkTokenValidity } from "./client";
import { notice } from "@/utils/notification";
import { appStore as store } from "@/store/global";

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
        name: "Store",
        path: "/store",
        component: NonebotStore,
      },
      {
        name: "FileExplorer",
        path: "/file",
        component: FileExplorer,
      },
      {
        name: "Setting",
        path: "/setting",
        component: SettingPage,
      },
    ],
  },
];

export const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach(async (to) => {
  const login = await checkTokenValidity();
  if (!login && to.name !== "Login") {
    notice.warning("登陆凭证失效");
    router.push("/login");
  }
  if (!store().choiceProject.project_id && to.path !== "/" && to.path !== "/login") {
    router.push("/");
    notice.warning("请先选择一项实例");
    return false;
  }
});
