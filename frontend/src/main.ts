import { createApp } from "vue";
import "@/style.css";
import App from "@/App.vue";
import { registerPlugins } from "@/plugins";

import "@/api/authenticationInterceptor";
import { ToastWrapper } from "@/utils/notification";
import { webuiConfig } from "@/config";

webuiConfig.init();

const app = createApp(App);

registerPlugins(app);

app.mount("#app");

export const globalLog = new ToastWrapper("WebUI");
