<script setup lang="ts">
import { ref } from "vue";
import { client, AuthService } from "@/client/api";
import router from "@/router";
import { useNoneBotStore, useToastStore } from "@/stores";

const store = useToastStore();
const nonebotStore = useNoneBotStore();

const token = ref(""),
  isDebug = ref(false),
  host = ref(""),
  port = ref("");

const date = new Date();

const login = async () => {
  if (isDebug.value) {
    const baseUrl = `//${host.value}:${port.value}/api`;
    client.setConfig({
      baseUrl: baseUrl,
    });
    localStorage.setItem("isDebug", "1");
    localStorage.setItem("debugUrl", baseUrl);
  }

  const { data, error } = await AuthService.authTokenV1AuthLoginPost({
    body: {
      token: token.value,
      mark: date.toISOString(),
    },
  });

  if (error) {
    store.add("error", `错误: ${error.detail?.toString()}`, "", 5000);
  }

  if (data) {
    localStorage.setItem("token", data.detail);
    client.interceptors.request.use((request) => {
      request.headers.set("Authorization", `Bearer ${data.detail}`);
      return request;
    });
    router.push("/");
    await nonebotStore.loadBots();
    store.add("success", "登陆成功", "", 5000);
  }
};
</script>

<template>
  <div class="shrink-0 w-full">
    <form class="flex justify-center flex-col gap-4 lg:gap-0" @submit.prevent="login">
      <div class="flex justify-center gap-0 lg:gap-4 flex-col lg:flex-row">
        <label class="form-control">
          <input
            v-model="token"
            type="password"
            placeholder="请键入登陆凭证"
            class="input input-ghost bg-base-200"
            required
          />
          <div class="label">
            <span class="label-text">开发模式</span>
            <input
              type="checkbox"
              class="checkbox checkbox-xs"
              :checked="isDebug"
              @click="isDebug = !isDebug"
            />
          </div>
        </label>

        <div class="form-control">
          <button class="btn btn-primary text-base-100">
            开始使用 <span class="material-symbols-outlined"> chevron_right </span>
          </button>
        </div>
      </div>

      <div v-if="isDebug" class="form-control flex gap-4 flex-col">
        <input
          v-model="host"
          type="text"
          placeholder="host"
          class="input input-ghost bg-base-200"
          required
        />

        <input
          v-model="port"
          type="text"
          placeholder="port"
          class="input input-ghost bg-base-200"
          required
        />
      </div>
    </form>
  </div>
</template>
