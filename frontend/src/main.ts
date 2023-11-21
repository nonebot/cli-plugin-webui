import App from "@/App.vue";

import { createApp } from "vue";
import { registerPlugins } from "@/plugins";
import { webuiConfig } from "@/config";

import "@/style.css";

webuiConfig.init();

const app = createApp(App);

registerPlugins(app);

app.mount("#app");
