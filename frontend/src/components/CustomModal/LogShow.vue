<script setup lang="ts" generic="T extends any">
import { ProcessLog } from "@/api/schemas";
import { getURL } from "@/utils";
import { onUnmounted, ref, watch } from "vue";
import { useWebSocket } from "@vueuse/core";
import type { UseWebSocketReturn } from "@vueuse/core";

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

const isFailed = ref(false),
  isDone = ref(false),
  logShowArea = ref<HTMLElement>(),
  websocket = ref<UseWebSocketReturn<T>>();

interface LogItem {
  message: string;
  time?: string;
  level?: string;
}

const logItems = ref<LogItem[]>([]);

const writeToArea = (message: string, time?: string, level?: string) => {
  logItems.value.push({
    message: message,
    time: time,
    level: level,
  });
};

const clearArea = () => {
  logItems.value = [];
};

const handleWebSocket = () => {
  if (!props.logKey) return;

  websocket.value = useWebSocket(getURL(`/api/v1/process/log/ws`, true), {
    onConnected(ws) {
      const token = localStorage.getItem("jwtToken") ?? "";
      ws.send(token);
      ws.send(JSON.stringify({ type: "log", log_key: props.logKey }));
    },
    onMessage(ws, event) {
      const data: ProcessLog = JSON.parse(event.data.toString());
      if (logShowArea.value) {
        writeToArea(data.message, data.time, data.level);
        const logRows = logShowArea.value.getElementsByTagName("tr");
        const lastLogRow = logRows[logRows.length - 1];
        lastLogRow.scrollIntoView({ behavior: "smooth", block: "end" });
      }

      if (data.message === "✨ Done!") {
        ws.close();
        isDone.value = true;
      } else if (data.message === "❌ Failed!") {
        ws.close();
        isFailed.value = true;
      }
    },
  });
};

const retry = () => {
  writeToArea("Retrying...");
  isDone.value = false;
  isFailed.value = false;
};

const clearState = () => {
  clearArea();

  isDone.value = false;
  isFailed.value = false;
};

onUnmounted(() => {
  websocket.value?.close();
  clearArea();
});

watch(props, () => {
  clearState();
  handleWebSocket();
});
</script>

<template>
  <dialog ref="logShowModal" class="modal">
    <div class="modal-box rounded-lg log-view-card">
      <div class="h-full flex flex-col">
        <h3 class="font-bold text-lg">正在安装依赖</h3>

        <div
          class="h-full mt-4 p-2 md:p-4 overflow-y-auto bg-base-200"
          style="font-family: monospace"
        >
          <table class="table table-xs">
            <tbody ref="logShowArea">
              <tr v-for="item in logItems" class="flex">
                <td>{{ item.time }}</td>
                <td>{{ item.level }} {{ item.message }}</td>
              </tr>
            </tbody>
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
    </div>
  </dialog>
</template>

<style scoped>
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
