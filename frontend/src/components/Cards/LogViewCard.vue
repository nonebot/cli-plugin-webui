<script setup lang="ts">
import { WebUIWebSocket } from "@/core/ws";
import { ToastWrapper } from "@/core/notification";
import { ref, watch } from "vue";

const log = new ToastWrapper("Log View");

const emit = defineEmits(["isRetry", "isOK"]);

const props = defineProps({
  logKey: String,
});
const isFailed = ref(false);
const isDone = ref(false);

interface ProcessLog {
  time: String;
  level: String;
  message: String;
}

const showLog = () => {
  const showArea = document.getElementById("log-show-area")!;
  const ws = new WebUIWebSocket(`/api/log/logs/${props.logKey}`).init();
  ws.connect();

  if (!ws.client) {
    log.error("WebSocket 未初始化");
    return;
  }

  ws.client.onmessage = (event) => {
    const data: ProcessLog = JSON.parse(event.data.toString());
    showArea.innerHTML += `
    <tr class="flex">
      <td>${data.time}</td>
      <td>${data.level} ${data.message}</td>
    </tr>
    `;

    if (data.message === "✨ Done!") {
      ws.client?.close();
      isDone.value = true;
    } else if (data.message === "❗ Failed...") {
      ws.client?.close();
      isFailed.value = true;
    }

    const logRows = showArea.getElementsByTagName("tr");
    const lastLogRow = logRows[logRows.length - 1];
    lastLogRow.scrollIntoView({ behavior: "smooth", block: "end" });
  };
};

const retry = () => {
  const showArea = document.getElementById("log-show-area")!;
  showArea.innerHTML = `
  <tr class="flex">
    <td>Retrying...</td>
    <td></td>
  </tr>
  `;
  isDone.value = false;
  isFailed.value = false;
};

const clearState = () => {
  const showArea = document.getElementById("log-show-area")!;
  showArea.innerHTML = "";

  isDone.value = false;
  isFailed.value = false;
};

watch(props, () => {
  showLog();
});
</script>

<template>
  <div class="modal" id="log-view">
    <div class="modal-box rounded-lg log-view-card">
      <div class="h-full flex flex-col">
        <h3 class="font-bold text-lg">正在安装依赖</h3>

        <div
          class="h-full mt-4 p-4 overflow-y-auto bg-base-200"
          style="font-family: monospace"
        >
          <table class="table table-xs">
            <tbody id="log-show-area"></tbody>
          </table>
        </div>

        <div class="modal-action">
          <a href="#" class="btn rounded-lg h-10 min-h-0">取消</a>
          <a
            :class="{
              'btn rounded-lg h-10 min-h-0': true,
              'btn-disabled': !isFailed,
            }"
            @click="emit('isRetry', true), retry()"
            >重试</a
          >

          <!-- TODO: 自动选中 -->
          <a
            href="#"
            :class="{
              'btn rounded-lg h-10 min-h-0': true,
              'btn-primary text-white': isDone,
              'btn-disabled': !isDone,
            }"
            @click="emit('isOK', true), clearState()"
            >完成</a
          >
        </div>
      </div>
    </div>
  </div>
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
