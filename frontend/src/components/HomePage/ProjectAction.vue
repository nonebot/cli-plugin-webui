<script setup lang="ts">
import { appStore as store } from "@/store/global";
import { notice } from "@/utils/notification";
import { ref } from "vue";
import { api, getProjectList } from "./client";
import { AxiosError } from "axios";

const oprateLock = ref(false);

const oLock = () => {
  oprateLock.value = true;
};

const oUnlock = () => {
  oprateLock.value = false;
};

const runProject = async () => {
  oLock();
  await api
    .runProject(store().choiceProject.project_id)
    .then(async () => {
      store().projectIsRunning();
      await getProjectList();
      oUnlock();
    })
    .catch((error: AxiosError) => {
      let reason: string;
      if (error.response) {
        reason = (error.response.data as { detail: string })?.detail;
      } else {
        reason = error.message;
      }
      notice.error(`运行实例失败：${reason}`);
      oUnlock();
    });
};

const stopProject = async () => {
  oLock();
  await api
    .stopProject(store().choiceProject.project_id)
    .then(async () => {
      store().projectIsStop();
      await getProjectList();
      oUnlock();
    })
    .catch((error: AxiosError) => {
      let reason: string;
      if (error.response) {
        reason = (error.response.data as { detail: string })?.detail;
      } else {
        reason = error.message;
      }
      notice.error(`停止实例失败：${reason}`);
      oUnlock();
    });
};

const restartProject = async () => {
  const sleep = (ms: number) => {
    return new Promise((resolve) => {
      setTimeout(resolve, ms);
    });
  };

  notice.info("重启中...");
  oLock();
  await stopProject();

  const pollingInterval = 2000;
  const maxAttempts = 30;

  let attempts = 0;
  while (attempts < maxAttempts) {
    if (!store().choiceProject.is_running) {
      break;
    }

    await sleep(pollingInterval);
  }

  if (!store().choiceProject.is_running) {
    await runProject();
    notice.info("实例已重启");
  } else {
    notice.warning("重启失败，无法确定实例是否已停止");
  }
  oUnlock();
};

const deleteProject = async () => {
  oLock();
  const project = store().choiceProject;
  await api
    .deleteProject(project.project_id)
    .then(async () => {
      await getProjectList();
      store().choiceProject = Object();
      oUnlock();
    })
    .catch((error: AxiosError) => {
      let reason: string;
      if (error.response) {
        reason = (error.response.data as { detail: string })?.detail;
      } else {
        reason = error.message;
      }
      notice.error(`删除操作失败：${reason}`);
      oUnlock();
    });
};
</script>

<template>
  <div class="!mt-0 !mb-0 sm:m-8 md:m-12 lg:m-16 xl:m-20 2xl:m-28">
    <Transition>
      <div
        v-if="store().choiceProject.project_id"
        class="w-full p-4 md:p-6 rounded shadow-none md:shadow-lg bg-base-200"
      >
        <div class="flex justify-between items-center">
          <div class="xs:text-base md:text-xl">实例控制</div>
          <div class="grid grid-cols-4 gap-4">
            <button
              :class="{
                'btn btn-sm rounded hover:bg-[hsl(var(--bc)/0.1)] transition-all ease-in': true,
                'btn-disabled': store().choiceProject.is_running || oprateLock,
              }"
              title="启动"
              @click="runProject()"
            >
              <span class="material-symbols-outlined"> play_arrow </span>
            </button>

            <button
              :class="{
                'btn btn-sm rounded hover:bg-[hsl(var(--bc)/0.1)] transition-all ease-in': true,
                'btn-disabled': !store().choiceProject.is_running || oprateLock,
              }"
              title="停止"
              @click="stopProject()"
            >
              <span class="material-symbols-outlined"> stop </span>
            </button>

            <button
              :class="{
                'btn btn-sm rounded hover:bg-[hsl(var(--bc)/0.1)] transition-all ease-in': true,
                'btn-disabled': !store().choiceProject.is_running || oprateLock,
              }"
              title="重启"
              @click="restartProject()"
            >
              <span class="material-symbols-outlined"> restart_alt </span>
            </button>

            <label
              :class="{
                'swap btn btn-sm rounded hover:bg-[hsl(var(--bc)/0.1)] transition-all ease-in': true,
                'btn-disabled': store().choiceProject.is_running || oprateLock,
              }"
            >
              <input type="checkbox" />
              <span
                title="销毁实例"
                class="swap-off material-symbols-outlined"
                @click="deleteProject()"
              >
                delete
              </span>
              <span class="swap-on material-symbols-outlined"> check </span>
            </label>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>
