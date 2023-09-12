<script setup lang="ts">
import InvisibleIcon from "@/components/Icons/InvisibleIcon.vue";
import VisibleIcon from "@/components/Icons/VisibleIcon.vue";

import { ref, watch } from "vue";
import { ToastWrapper } from "@/utils/notification";
import { API } from "@/api";
import { appStore } from "@/store/global";
import { router } from "@/router";
import { AxiosError } from "axios";

const api = new API();
const notice = new ToastWrapper("Login");

const token = ref("");
const checkToken = ref(false);
const isDebug = ref(false);
const host = ref("");
const port = ref("");

watch(isDebug, () => {
  localStorage.setItem("isDebug", isDebug.value ? "1" : "0");
  notice.info(`已${isDebug.value ? "启用" : "禁用"}开发模式`);
});

async function doLogin() {
  if (!token.value) {
    notice.warning("缺少 Token");
    return;
  }
  if (isDebug.value) {
    if (!host.value) {
      notice.warning("缺少 Host");
      return;
    }
    if (!port.value) {
      notice.warning("缺少 Port");
      return;
    }

    localStorage.setItem("host", host.value);
    localStorage.setItem("port", port.value);
  }

  await api
    .doLogin(token.value)
    .then((resp) => {
      notice.success("登录成功");
      localStorage.setItem("jwtToken", resp.jwt_token);
      appStore().isAuth = true;
      router.push("/");
    })
    .catch((error: AxiosError) => {
      if (error.response) {
        notice.error(`验证失败：${(error.response.data as { detail: string })?.detail}`);
      } else {
        notice.error(`验证失败：${error.message}`);
      }
    });
}
</script>

<template>
  <div class="hero min-h-screen bg-base-200">
    <div class="flex flex-col items-center w-full sm:w-8/12 lg:w-auto">
      <div
        class="w-full hero-content flex-col flex-col-reverse lg:flex-row-reverse gap-8"
      >
        <div
          class="card rounded flex-shrink-0 w-full lg:max-w-sm shadow-none md:shadow-lg bg-base-100"
        >
          <div class="card-body">
            <div class="form-control w-full">
              <label class="label">
                <span class="text-sm">访问 Token</span>
                <span>
                  <label class="swap">
                    <input type="checkbox" />
                    <VisibleIcon
                      title="查看"
                      class="swap-on h-5 w-5"
                      @click="checkToken = true"
                    />
                    <InvisibleIcon
                      title="隐藏"
                      class="swap-off h-5 w-5"
                      @click="checkToken = false"
                    />
                  </label>
                </span>
              </label>
              <input
                v-model="token"
                :type="checkToken ? 'text' : 'password'"
                placeholder="token"
                class="input input-bordered w-full"
              />

              <div class="mt-4 flex justify-center">
                <div class="w-3/4 flex justify-around">
                  <div class="text-sm">开发模式：</div>
                  <input
                    type="checkbox"
                    class="toggle toggle-primary"
                    :checked="isDebug"
                    @click="isDebug = !isDebug"
                  />
                </div>
              </div>

              <Transition>
                <div v-if="isDebug" class="mt-4 w-full grid grid-rows-2 gap-4">
                  <input
                    v-model="host"
                    type="text"
                    placeholder="host"
                    class="input input-bordered w-full"
                  />
                  <input
                    v-model="port"
                    type="text"
                    placeholder="port"
                    class="input input-bordered w-full"
                  />
                </div>
              </Transition>

              <button class="mt-4 btn btn-primary text-white" @click="doLogin">
                Login
              </button>
            </div>
          </div>
        </div>

        <div class="w-full tracking-tight font-light">
          <div class="mt-2 mb-2 text-6xl lg:text-8xl sm:text-6xl">
            <span class="main-word">N</span>one<span class="main-word">B</span>ot
          </div>
          <p class="text-lg">跨平台 PYTHON 异步机器人框架</p>
        </div>
      </div>

      <div
        class="h-28 pt-20 flex justify-center w-full text-sm text-base-content transition"
      >
        <div class="w-full text-right">
          <a
            href="https://nonebot.dev"
            class="opacity-60 hover:opacity-100 duration-150 hover:ease-in-out"
            target="_blank"
          >
            NoneBot
          </a>
        </div>
        <div class="ml-4 mr-4 opacity-60">|</div>
        <div class="w-full">
          <a
            href="https://github.com/nonebot/nonebot2"
            class="opacity-60 hover:opacity-100 duration-150 hover:ease-in-out"
            target="_blank"
          >
            GitHub
          </a>
        </div>
      </div>
    </div>
  </div>
</template>
