<script setup lang="ts">
import { ProcessService, ProjectService } from "@/client/api";
import { sleep } from "@/client/utils";
import { useNoneBotStore, useToastStore } from "@/stores";
import { ref } from "vue";

const store = useNoneBotStore();
const toast = useToastStore();

const deleteConfirmModal = ref<HTMLDialogElement>();

const oLock = ref(false);

const runBot = async () => {
  if (!store.selectedBot) return;

  oLock.value = true;
  const { data, error } = await ProcessService.runProcessV1ProcessRunPost({
    query: {
      project_id: store.selectedBot?.project_id,
    },
  });

  if (error) {
    toast.add("error", `启动失败, 原因：${error.detail?.toString()}`, "", 5000);
  }

  if (data) {
    await store.loadBots();
    toast.add("success", `${store.selectedBot?.project_name} 已启动`, "", 5000);
  }

  oLock.value = false;
};

const stopBot = async () => {
  if (!store.selectedBot) return;

  oLock.value = true;
  const { data, error } = await ProcessService.stopProcessV1ProcessStopPost({
    query: {
      project_id: store.selectedBot?.project_id,
    },
  });

  if (error) {
    toast.add("error", `停止失败, 原因：${error.detail?.toString()}`, "", 5000);
  }

  if (data) {
    await store.loadBots();
    toast.add("success", `${store.selectedBot?.project_name} 已停止`, "", 5000);
  }

  oLock.value = false;
};

const restartBot = async () => {
  if (!store.selectedBot) return;

  oLock.value = true;

  await stopBot();

  const pollingInterval = 2000;
  const maxAttempts = 30;

  let attempts = 0;
  while (attempts < maxAttempts) {
    if (!store.selectedBot.is_running) {
      break;
    }

    await sleep(pollingInterval);
  }

  if (attempts >= maxAttempts) {
    toast.add("error", "重启失败", "", 5000);
  } else {
    await runBot();
  }
  oLock.value = false;
};

const deleteBot = async (isFully: boolean = false) => {
  if (!store.selectedBot) return;

  oLock.value = true;

  const { data, error } = await ProjectService.deleteProjectV1ProjectDeleteDelete({
    query: {
      project_id: store.selectedBot.project_id,
      delete_fully: isFully,
    },
  });

  if (error) {
    toast.add("error", `删除失败, 原因：${error.detail?.toString()}`, "", 5000);
  }

  if (data) {
    await store.loadBots();
    store.selectBot(Object.values(store.bots)[0]);
  }

  oLock.value = false;
};
</script>

<template>
  <dialog ref="deleteConfirmModal" class="modal">
    <div class="modal-box rounded-lg flex flex-col gap-4">
      <h3 class="font-semibold text-lg">确定删除实例吗</h3>
      <div class="grid grid-cols-3 gap-4">
        <button class="btn btn-sm hover:btn-primary shadow-none" @click="deleteBot(true)">
          确定
        </button>
        <button class="btn btn-sm hover:btn-warning shadow-none" @click="deleteBot()">
          仅删除信息
        </button>
        <button class="btn btn-sm shadow-none" @click="deleteConfirmModal?.close()">
          取消
        </button>
      </div>
    </div>
  </dialog>

  <div
    class="w-full p-6 bg-base-200 rounded-box flex flex-col md:flex-row items-center justify-between gap-2 md:gap-0"
  >
    <div class="flex items-center gap-4">
      <div class="text-lg font-semibold">{{ store.selectedBot?.project_name }}</div>
      <div class="flex items-center gap-2">
        <div class="badge badge-sm text-gray-500">
          {{ store.selectedBot?.project_id }}
        </div>

        <div
          v-if="store.selectedBot?.is_running"
          class="badge badge-sm badge-success text-base-100"
        >
          运行中
        </div>
        <div v-else class="badge badge-sm badge-error text-base-100">未运行</div>
      </div>
    </div>

    <div class="flex gap-2">
      <button
        :class="{
          'btn btn-sm btn-primary font-normal text-base-100': true,
          'btn-disabled': store.selectedBot?.is_running || oLock,
        }"
        @click="runBot()"
      >
        启动
      </button>
      <button
        :class="{
          'btn btn-sm shadow-none font-normal': true,
          'btn-disabled': !store.selectedBot?.is_running || oLock,
        }"
        @click="stopBot()"
      >
        停止
      </button>
      <button
        :class="{
          'btn btn-sm shadow-none font-normal border-red': true,
          'btn-disabled': !store.selectedBot?.is_running || oLock,
        }"
        @click="restartBot()"
      >
        重启
      </button>
      <button
        :class="{
          'btn btn-sm btn-outline btn-primary shadow-none font-normal': true,
          'btn-disabled':
            store.selectedBot?.is_running ||
            Object.values(store.bots).length <= 1 ||
            oLock,
        }"
        @click="deleteConfirmModal?.showModal()"
      >
        删除
      </button>
    </div>
  </div>
</template>
