<script setup lang="ts">
import PlayArrowIcon from "@/components/Icons/PlayArrowIcon.vue";
import StopIcon from "@/components/Icons/StopIcon.vue";
import RefreshIcon from "@/components/Icons/RefreshIcon.vue";
import DeleteIcon from "@/components/Icons/DeleteIcon.vue";
import CheckIcon from "@/components/Icons/CheckIcon.vue";

import { API } from "@/api";
import { appStore as store } from "@/store/global";
import { globalLog as log } from "@/main";

const api = new API();

const runProject = async () => {
  await api
    .runProject(store().choiceProject.project_id)
    .then(() => {
      store().projectIsRunning();
    })
    .catch((error) => {
      log.error(`运行实例失败：${error}`);
      return;
    });
};

const stopProject = async () => {
  await api
    .stopProject(store().choiceProject.project_id)
    .then(() => {
      store().projectIsStop();
    })
    .catch((error) => {
      log.error(`停止实例失败：${error}`);
      return;
    });
};

const restartProject = async () => {
  const sleep = (ms: number) => {
    return new Promise((resolve) => {
      setTimeout(resolve, ms);
    });
  };

  log.info("重启中...");
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
    log.info("实例已重启");
  } else {
    log.warning("重启失败，无法确定实例是否已停止");
  }
};

const deleteProject = async () => {
  const project = store().choiceProject;
  try {
    await api.deleteProject(project.project_id);
  } catch (error) {
    log.error(`删除操作失败：${error}`);
    return;
  }
  store().choiceProject = Object();
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
                'btn-disabled': store().choiceProject.is_running,
              }"
              title="启动"
              @click="runProject()"
            >
              <PlayArrowIcon class="h-6 w-6" />
            </button>

            <button
              :class="{
                'btn btn-sm rounded hover:bg-[hsl(var(--bc)/0.1)] transition-all ease-in': true,
                'btn-disabled': !store().choiceProject.is_running,
              }"
              title="停止"
              @click="stopProject()"
            >
              <StopIcon class="h-6 w-6" />
            </button>

            <button
              :class="{
                'btn btn-sm rounded hover:bg-[hsl(var(--bc)/0.1)] transition-all ease-in': true,
                'btn-disabled': !store().choiceProject.is_running,
              }"
              title="重启"
              @click="restartProject()"
            >
              <RefreshIcon class="h-6 w-6" />
            </button>

            <label
              :class="{
                'swap btn btn-sm rounded hover:bg-[hsl(var(--bc)/0.1)] transition-all ease-in': true,
                'btn-disabled': store().choiceProject.is_running,
              }"
            >
              <input type="checkbox" />
              <CheckIcon
                title="销毁实例"
                class="swap-on h-6 w-6 text-primary"
                @click="deleteProject()"
              />
              <DeleteIcon title="确认" class="swap-off h-6 w-6" />
            </label>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>
