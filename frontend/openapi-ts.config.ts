import { defineConfig } from "@hey-api/openapi-ts";

export default defineConfig({
  client: "@hey-api/client-fetch",
  input: "../openapi.json",
  output: {
    format: "prettier",
    path: "./src/client/api",
  },
  services: {
    asClass: true,
  },
});
