<script setup lang="ts">
import { ProcessLog } from "@/api/models";
import { WebsocketWrapper } from "@/utils/ws";
import { ToastWrapper } from "@/utils/notification";
import { ref, watch } from "vue";

const notice = new ToastWrapper("Log Show");
const websocket = ref<WebsocketWrapper>();
const logShowModal = ref<HTMLDialogElement>();

defineExpose({
  openModal: () => {
    logShowModal.value?.showModal();
  },
  closeModal: () => {
    logShowModal.value?.close();
  },
});

const emit = defineEmits(["isRetry", "isOK"]);

const props = defineProps({
  logKey: String,
});

const isFailed = ref(false);
const isDone = ref(false);
const logShowArea = ref<HTMLElement>();

const handleWebSocket = () => {
  if (websocket.value?.state.connected) {
    websocket.value.close();
  }

  websocket.value = new WebsocketWrapper(`/api/log/logs/${props.logKey}`);

  const maxRetries = 3;
  let retries = 0;
  let connected = false;

  while (!connected && retries < maxRetries) {
    try {
      websocket.value.connect();
      connected = true;
    } catch (error: any) {
      notice.error(`连接至日志 WebSocket 失败...(${retries + 1}/${maxRetries})`);
      retries++;
    }
  }

  if (!connected) {
    notice.error("连接至日志 WebSocket 失败");
    return;
  }

  websocket.value.client!.onmessage = (event: MessageEvent) => {
    const data: ProcessLog = JSON.parse(event.data.toString());
    if (logShowArea.value) {
      logShowArea.value.innerHTML += `
      <tr class="flex">
        <td>${data.time}</td>
        <td>${data.level} ${data.message}</td>
      </tr>
      `;
      const logRows = logShowArea.value.getElementsByTagName("tr");
      const lastLogRow = logRows[logRows.length - 1];
      lastLogRow.scrollIntoView({ behavior: "smooth", block: "end" });
    }

    if (data.message === "✨ Done!") {
      websocket.value?.close();
      isDone.value = true;
    } else if (data.message === "❗ Failed...") {
      websocket.value?.close();
      isFailed.value = true;
    }
  };
};

const retry = () => {
  if (logShowArea.value) {
    logShowArea.value.innerHTML = `
      <tr class="flex">
        <td>Retrying...</td>
        <td></td>
      </tr>
    `;
  }
  isDone.value = false;
  isFailed.value = false;
};

const clearState = () => {
  if (logShowArea.value) {
    logShowArea.value.innerHTML = "";
  }

  isDone.value = false;
  isFailed.value = false;
};

watch(props, () => {
  clearState();
  handleWebSocket();
});
</script>

<template>
  <dialog ref="logShowModal" class="modal">
    <form method="dialog" class="modal-box rounded-lg log-view-card">
      <div class="h-full flex flex-col">
        <h3 class="font-bold text-lg">正在安装依赖</h3>

        <div
          class="h-full mt-4 p-2 md:p-4 overflow-y-auto bg-base-200"
          style="font-family: monospace"
        >
          <table class="table table-xs">
            <tbody ref="logShowArea"></tbody>
          </table>
        </div>

        <div class="modal-action">
          <button class="btn rounded-lg h-10 min-h-0" @click="logShowModal?.close()">
            取消
          </button>

          <button
            :class="{
              'btn rounded-lg h-10 min-h-0': true,
              'btn-disabled': !isFailed,
            }"
            @click="emit('isRetry', true), retry()"
          >
            重试
          </button>

          <button
            :class="{
              'btn rounded-lg h-10 min-h-0': true,
              'btn-primary text-white': isDone,
              'btn-disabled': !isDone,
            }"
            @click="emit('isOK', true), clearState(), logShowModal?.close()"
          >
            完成
          </button>
        </div>
      </div>
    </form>
  </dialog>
</template>

<style>
.log-view-card {
  height: 75%;
  max-width: 100% !important;
  width: 76%;
}

@media screen and (max-width: 640px) {
  .log-view-card {
    width: 90%;
  }
}
</style>
