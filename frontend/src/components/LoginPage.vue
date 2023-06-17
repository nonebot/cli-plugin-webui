<script setup lang="ts">
import { ref, watch } from "vue";
import { ToastWrapper } from "@/core/notification";
import { API } from "@/api";
import { globalStore } from "@/store/app";
import { router } from "@/router";

const log = new ToastWrapper("Authentication");

const token = ref("");
const checkToken = ref(false);
const isDebug = ref(false);
const host = ref("");
const port = ref("");

watch(isDebug, () => {
  localStorage.setItem("isDebug", isDebug.value ? "1" : "0");
  log.info(`已${isDebug.value ? "启用" : "禁用"}开发模式`);
});

async function doLogin() {
  if (token.value === "") {
    log.warning("缺少 Token");
    return;
  }
  if (isDebug.value) {
    if (host.value === "") {
      log.warning("缺少 Host");
      return;
    }
    if (port.value === "") {
      log.warning("缺少 Port");
      return;
    }

    localStorage.setItem("host", host.value);
    localStorage.setItem("port", port.value);
  }

  const api = new API();
  try {
    const resp = await api.doLogin(token.value);
    log.success("登录成功");
    localStorage.setItem("jwtToken", resp.jwt_token);
    globalStore().isAuthed = true;
    router.push("/");
  } catch (error) {
    log.error(`验证失败：${error}`);
  }
}
</script>

<template>
  <div class="hero min-h-screen bg-base-200">
    <div class="flex flex-col items-center w-auto max-[640px]:w-full">
      <div
        class="max-[390px]:w-full max-[640px]:w-8/12 hero-content flex-col min-[280px]:flex-col-reverse lg:flex-row-reverse gap-8"
      >
        <div
          class="card rounded flex-shrink-0 w-full lg:max-w-sm shadow-lg bg-base-100"
        >
          <div class="card-body">
            <div class="mt-4 flex flex-col items-center">
              <div class="form-control w-full">
                <label class="label">
                  <span class="text-sm">访问 Token</span>
                  <span>
                    <label class="swap">
                      <input type="checkbox" />
                      <svg
                        @click="checkToken = true"
                        class="swap-on fill-current"
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 0 24 24"
                        height="20"
                        width="20"
                      >
                        <title>查看</title>
                        <path
                          d="M12,9A3,3 0 0,1 15,12A3,3 0 0,1 12,15A3,3 0 0,1 9,12A3,3 0 0,1 12,9M12,4.5C17,4.5 21.27,7.61 23,12C21.27,16.39 17,19.5 12,19.5C7,19.5 2.73,16.39 1,12C2.73,7.61 7,4.5 12,4.5M3.18,12C4.83,15.36 8.24,17.5 12,17.5C15.76,17.5 19.17,15.36 20.82,12C19.17,8.64 15.76,6.5 12,6.5C8.24,6.5 4.83,8.64 3.18,12Z"
                        />
                      </svg>
                      <svg
                        @click="checkToken = false"
                        class="swap-off fill-current"
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 0 24 24"
                        height="20"
                        width="20"
                      >
                        <title>隐藏</title>
                        <path
                          d="M2,5.27L3.28,4L20,20.72L18.73,22L15.65,18.92C14.5,19.3 13.28,19.5 12,19.5C7,19.5 2.73,16.39 1,12C1.69,10.24 2.79,8.69 4.19,7.46L2,5.27M12,9A3,3 0 0,1 15,12C15,12.35 14.94,12.69 14.83,13L11,9.17C11.31,9.06 11.65,9 12,9M12,4.5C17,4.5 21.27,7.61 23,12C22.18,14.08 20.79,15.88 19,17.19L17.58,15.76C18.94,14.82 20.06,13.54 20.82,12C19.17,8.64 15.76,6.5 12,6.5C10.91,6.5 9.84,6.68 8.84,7L7.3,5.47C8.74,4.85 10.33,4.5 12,4.5M3.18,12C4.83,15.36 8.24,17.5 12,17.5C12.69,17.5 13.37,17.43 14,17.29L11.72,15C10.29,14.85 9.15,13.71 9,12.28L5.6,8.87C4.61,9.72 3.78,10.78 3.18,12Z"
                        />
                      </svg>
                    </label>
                  </span>
                </label>
                <input
                  v-model="token"
                  :type="checkToken ? 'text' : 'password'"
                  placeholder="token"
                  class="input input-bordered w-auto max-w-xs"
                />
              </div>

              <div class="mt-4 w-3/4 flex justify-around">
                <div class="text-sm">开发模式：</div>
                <input
                  type="checkbox"
                  class="toggle toggle-primary"
                  :checked="isDebug"
                  @click="isDebug = !isDebug"
                />
              </div>
            </div>

            <div v-if="isDebug" class="mt-4">
              <div class="form-control w-full">
                <input
                  v-model="host"
                  type="text"
                  placeholder="host"
                  class="input input-bordered w-full max-w-xs"
                />
                <input
                  v-model="port"
                  type="text"
                  placeholder="port"
                  class="input input-bordered w-full max-w-xs mt-4"
                />
              </div>
            </div>

            <div class="form-control mt-6">
              <button class="btn btn-primary text-white" @click="doLogin">
                Login
              </button>
            </div>
          </div>
        </div>

        <div class="w-full tracking-tight font-light">
          <div class="mt-2 mb-2 lg:text-8xl sm:text-6xl text-6xl">
            <span class="main-word">N</span>one<span class="main-word">B</span
            >ot
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
            class="opacity-60 hover:opacity-100 duration-200 hover:ease-in-out"
            target="_blank"
          >
            NoneBot v2
          </a>
        </div>
        <div class="ml-4 mr-4 opacity-60">|</div>
        <div class="w-full">
          <a
            href="https://github.com/nonebot/nonebot2"
            class="opacity-60 hover:opacity-100 duration-200 hover:ease-in-out"
            target="_blank"
          >
            GitHub
          </a>
        </div>
      </div>
    </div>
  </div>
</template>
