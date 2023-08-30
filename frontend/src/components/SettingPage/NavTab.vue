<script setup lang="ts">
import PlayArrowIcon from "@/components/Icons/PlayArrowIcon.vue";

import { ref } from "vue";
import { API } from "@/api";
import { appStore as store } from "@/store/global";
import { limitContent } from "@/utils";
import { getNonebotConfig } from "./client";

const api = new API();

const tabs = ref<string[]>([]);
const addEnvInput = ref("");
const showModal = ref(false);

const getDotenv = async () => {
  try {
    const resp = await api.getDotenvList(store().choiceProject.project_id);
    tabs.value = resp.detail;
  } catch (error: any) {}
};

getDotenv();

const addEnv = async () => {
  if (!addEnvInput.value.length) {
    return;
  }

  const env = `.env.${addEnvInput.value}`;

  try {
    await api.createDotenvFile(store().choiceProject.project_id, env);
    tabs.value.push(env);
  } catch (error: any) {}
};

const assignEnv = async (env: string) => {
  try {
    await api.activeDotenvFile(store().choiceProject.project_id, env);
    store().enabledEnv = env;
    tabs.value = [env, ...tabs.value.filter((i) => i !== env)];
    await getNonebotConfig();
  } catch (error: any) {}
};
</script>

<template>
  <dialog :class="{ 'modal pl-0 md:pl-14': true, 'modal-open': showModal }">
    <form
      method="dialog"
      class="modal-box rounded-lg overflow-hidden flex flex-col flex-nowarp"
    >
      <h3 class="font-bold text-lg">更多选项</h3>
      <p class="text-xs">
        说明：运行环境配置。大小写不敏感。<br />
        将会从
        <strong>环境变量 > .env 环境配置文件</strong>
        的优先级读取环境信息。
      </p>
      <p class="pt-4">已知可使用的环境配置文件：</p>
      <div class="overflow-hidden flex flex-col flex-nowarp">
        <div class="custom-y-scrollbar overflow-y-auto grow">
          <table class="table table-xs">
            <thead>
              <tr>
                <th>值</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="env in tabs" class="hover:bg-base-300">
                <td>{{ env }}</td>
                <td class="flex">
                  <PlayArrowIcon
                    v-if="store().enabledEnv !== env"
                    role="button"
                    class="h-6 w-6 mr-2 opacity-30 hover:opacity-100 transition-all ease-in duration-100"
                    @click="assignEnv(env)"
                  />

                  <label
                    class="swap pl-1 pr-1 rounded opacity-30 hover:opacity-100 transition-all ease-in duration-100"
                  >
                    <input type="checkbox" />
                    <svg
                      class="swap-on fill-current h-5 w-5"
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 24 24"
                    >
                      <title>删除</title>
                      <path
                        d="M21,7L9,19L3.5,13.5L4.91,12.09L9,16.17L19.59,5.59L21,7Z"
                      />
                    </svg>
                    <svg
                      class="swap-off fill-current h-5 w-5"
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 24 24"
                    >
                      <title>确认</title>
                      <path
                        d="M6,19A2,2 0 0,0 8,21H16A2,2 0 0,0 18,19V7H6V19M8,9H16V19H8V9M15.5,4L14.5,3H9.5L8.5,4H5V6H19V4H15.5Z"
                      />
                    </svg>
                  </label>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="flex mt-2 text-sm">
          <span>.env.</span>
          <input
            v-model="addEnvInput"
            class="input input-xs input-bordered rounded ml-1 mr-1"
            maxlength="10"
          />
          <div class="btn btn-xs rounded" @click="addEnv()">添加</div>
        </div>
      </div>
      <div class="modal-action">
        <button class="btn rounded-lg h-10 min-h-0" @click="showModal = false">
          关闭
        </button>
      </div>
    </form>
    <form method="dialog" class="modal-backdrop">
      <button @click="showModal = false">close</button>
    </form>
  </dialog>

  <div v-if="tabs.length" class="pl-2 pr-2 flex justify-between">
    <div class="tabs">
      <a
        v-for="tab in tabs.slice(0, 2)"
        title="点击切换环境"
        :class="{
          'tab tab-sm tab-lifted': true,
          'tab-active': store().enabledEnv === tab,
        }"
        @click="assignEnv(tab)"
        >{{ limitContent(tab, 10) }}</a
      >
      <div class="tab tab-sm tab-lifted" @click="showModal = true">...</div>
    </div>

    <div class="tabs">
      <a
        class="tab tab-sm tab-lifted tab-active"
        title="更多选项"
        @click="showModal = true"
      >
        +
      </a>
    </div>
  </div>
</template>