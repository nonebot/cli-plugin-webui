<script setup lang="ts">
import { ProcessLog } from "@/api/models";
import { WebUIWebSocket } from "@/utils/ws";
import { ToastWrapper } from "@/utils/notification";
import { ref, watch } from "vue";

const log = new ToastWrapper("Log Show");

const emit = defineEmits(["isRetry", "isOK"]);

const props = defineProps({
  logKey: String,
});

const showModal = ref(false);

const openModal = () => {
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
};

defineExpose({
  openModal,
  closeModal,
});

const isFailed = ref(false);
const isDone = ref(false);
const logShowArea = ref<HTMLElement>();

const showLog = () => {
  const ws = new WebUIWebSocket(`/api/log/logs/${props.logKey}`);
  ws.connect();

  if (!ws.client) {
    log.error("WebSocket 未初始化");
    return;
  }

  ws.client.onmessage = (event) => {
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
      ws.client?.close();
      isDone.value = true;
    } else if (data.message === "❗ Failed...") {
      ws.client?.close();
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
  showLog();
});
</script>

<template>
  <dialog :class="{ 'modal pl-0 md:pl-14': true, 'modal-open': showModal }">
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
          <button class="btn rounded-lg h-10 min-h-0" @click="closeModal()">
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
            @click="emit('isOK', true), clearState(), closeModal()"
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
