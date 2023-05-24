import { createRouter, createWebHistory } from "vue-router";

import IndexPage from "@/components/IndexPage.vue";
import PluginManage from "@/components/PluginManage.vue";

const routes = [
  {
    path: "/",
    component: IndexPage,
  },
  {
    path: "/plugin",
    component: PluginManage,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
