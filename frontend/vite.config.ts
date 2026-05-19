import { fileURLToPath, URL } from "node:url";

import { defineConfig, loadEnv } from "vite";
import vue from "@vitejs/plugin-vue";

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");
  const host = env.NB_WEBUI_HOST || "localhost";
  const port = env.NB_WEBUI_PORT || "12345";

  return {
    plugins: [vue()],
    resolve: {
      alias: {
        "@": fileURLToPath(new URL("./src", import.meta.url)),
      },
    },
    server: {
      proxy: {
        "/api": {
          target: `http://${host}:${port}`,
          changeOrigin: true,
          ws: true,
        },
      },
    },
    build: {
      outDir: "../nb_cli_plugin_webui/dist",
    },
  };
});
