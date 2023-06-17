import type { App } from "vue";
import Vue3Toastify, { toast, type ToastContainerOptions } from "vue3-toastify";
import VueAxios from "vue-axios";
import axios from "axios";

import { router } from "@/router";
import pinia from "@/store";

export function registerPlugins(app: App) {
  app
    .use(router)
    .use(pinia)
    .use(Vue3Toastify, {
      position: toast.POSITION.BOTTOM_RIGHT,
      transition: toast.TRANSITIONS.SLIDE,
    } as ToastContainerOptions)
    .use(VueAxios, axios);
}
