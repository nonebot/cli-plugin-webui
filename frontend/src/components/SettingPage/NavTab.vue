<script setup lang="ts">
import { ref } from "vue";
import { API } from "@/api";
import { appStore as store } from "@/store/global";
import { limitContent } from "@/utils";
import { notice, getNonebotConfig } from "./client";
import { AxiosError } from "axios";

const api = new API();

const tabs = ref<string[]>([]);
const addEnvInput = ref("");
const envEditModal = ref<HTMLDialogElement>();

const getDotenv = async () => {
  await api
    .getEnvs(store().choiceProject.project_id)
    .then((resp) => {
      tabs.value = resp.detail;
    })
    .catch((error: AxiosError) => {
      let reason: string;
      if (error.response) {
        reason = (error.response.data as { detail: string })?.detail;
      } else {
        reason = error.message;
      }
      notice.error(`获取环境列表失败：${reason}`);
    });
};

getDotenv();

const addEnv = async () => {
  if (!addEnvInput.value.length) {
    return;
  }

  const env = `.env.${addEnvInput.value}`;
  await api
    .createEnv(env, store().choiceProject.project_id)
    .then(() => {
      tabs.value.push(env);
      addEnvInput.value = "";
    })
    .catch((error: AxiosError) => {
      let reason: string;
      if (error.response) {
        reason = (error.response.data as { detail: string })?.detail;
      } else {
        reason = error.message;
      }
      notice.error(`创建环境失败：${reason}`);
    });
};

const assignEnv = async (env: string) => {
  await api
    .useEnv(env, store().choiceProject.project_id)
    .then(() => {
      store().enabledEnv = env;
      tabs.value = [env, ...tabs.value.filter((i) => i !== env)];
      notice.success(`已切换至 ${env}`);
      return Promise.resolve();
    })
    .catch((error: AxiosError) => {
      let reason: string;
      if (error.response) {
        reason = (error.response.data as { detail: string })?.detail;
      } else {
        reason = error.message;
      }
      notice.error(`切换环境失败：${reason}`);
    });

  await getNonebotConfig();
};

const deleteEnv = async (env: string) => {
  if (env === ".env") {
    notice.warning("该环境不可删除");
    return;
  }

  await api
    .deleteEnv(env, store().choiceProject.project_id)
    .then(() => {
      store().enabledEnv = ".env";
    })
    .catch((error: AxiosError) => {
      let reason: string;
      if (error.response) {
        reason = (error.response.data as { detail: string })?.detail;
      } else {
        reason = error.message;
      }
      notice.error(`删除环境失败：${reason}`);
    });
};
</script>

<template>
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
      <div class="tab tab-sm tab-lifted" @click="envEditModal?.showModal()">...</div>
    </div>

    <div class="tabs">
      <button
        class="tab tab-sm tab-lifted tab-active"
        title="更多选项"
        @click="envEditModal?.showModal()"
      >
        +
      </button>
    </div>
  </div>

  <dialog ref="envEditModal" class="modal">
    <div class="modal-box rounded-lg overflow-hidden flex flex-col flex-nowrap">
      <h3 class="font-bold text-lg">更多选项</h3>
      <p class="text-xs">
        说明：运行环境配置。大小写不敏感。<br />
        将会从
        <strong>环境变量 > .env 环境配置文件</strong>
        的优先级读取环境信息。
      </p>
      <p class="pt-4">已知可使用的环境配置文件：</p>
      <div class="overflow-hidden flex flex-col flex-nowrap">
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
                  <span
                    v-if="store().enabledEnv !== env"
                    role="button"
                    class="material-symbols-outlined text-3xl leading-5 opacity-30 hover:opacity-100 transition-all ease-in duration-100"
                    @click="assignEnv(env)"
                  >
                    play_arrow
                  </span>

                  <label
                    class="swap pl-1 pr-1 rounded opacity-30 hover:opacity-100 transition-all ease-in duration-100"
                  >
                    <input type="checkbox" />
                    <span
                      class="swap-off material-symbols-outlined text-xl leading-5"
                      @click="deleteEnv(env)"
                    >
                      delete
                    </span>
                    <span class="swap-on material-symbols-outlined text-xl leading-5">
                      check
                    </span>
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
        <button class="btn rounded-lg h-10 min-h-0" @click="envEditModal?.close()">
          关闭
        </button>
      </div>
    </div>
    <form method="dialog" class="modal-backdrop">
      <button>close</button>
    </form>
  </dialog>
</template>
