<script setup lang="ts">
import { ProcessService, type ProcessLog } from "@/client/api";
import { generateURLForWebUI } from "@/client/utils";
import { useCustomStore, useNoneBotStore, useToastStore } from "@/stores";
import { useWebSocket } from "@vueuse/core";
import { onMounted, onUnmounted, ref, watch } from "vue";

const store = useNoneBotStore();
const customStore = useCustomStore();
const toast = useToastStore();

const logData = ref<ProcessLog[]>([]),
  logShowTable = ref<HTMLElement>(),
  currentBot = ref("");

const getHistoryLogs = async () => {
  if (!store.selectedBot) return;

  const getLogCount = 20;

  const { data, error } = await ProcessService.getLogHistoryV1ProcessLogHistoryGet({
    query: {
      log_count: getLogCount,
      log_id: store.selectedBot.project_id,
    },
  });

  if (error) {
    toast.add("warning", "获取日志失败, 原因: " + error.detail, "", 5000);
  }

  if (data) {
    logData.value = data.detail;
    const dataLength = data.detail.length;
    if (dataLength > 0) {
      logData.value.push({
        message: `已获取近期 ${dataLength} 条日志`,
      });
    }
  }
};

const { status, data, close, open, send } = useWebSocket<ProcessLog>(
  generateURLForWebUI("/v1/process/log/ws", true),
  {
    immediate: false,
    onConnected(ws) {
      const token = localStorage.getItem("token") ?? "";
      ws.send(token);

      if (store.selectedBot) {
        send(JSON.stringify({ type: "log", log_key: store.selectedBot?.project_id }));
        currentBot.value = store.selectedBot?.project_id;
      }

      if (customStore.isDebug) {
        toast.add(
          "success",
          "Debug: WebSocket 连接成功",
          "views/Operation/Terminal.vue",
          5000,
        );
      }
    },
    onDisconnected() {
      if (!customStore.isDebug) return;
      toast.add(
        "error",
        "Debug: WebSocket 连接断开",
        "views/Operation/Terminal.vue",
        5000,
      );
    },
  },
);
onMounted(async () => {
  if (!store.selectedBot) return;
  open();
  await getHistoryLogs();
});

onUnmounted(() => {
  close();
});

watch(
  () => data.value,
  (rawData) => {
    if (!rawData) return;

    const data: ProcessLog = JSON.parse(rawData.toString());

    logData.value.push(data);
    if (logShowTable.value)
      logShowTable.value.scrollTop = logShowTable.value.scrollHeight;
  },
);

watch(
  () => store.selectedBot,
  (newValue) => {
    if (!newValue) return;

    if (newValue.project_id === currentBot.value) {
      if (status.value !== "OPEN") open();
      return;
    }

    currentBot.value = newValue.project_id;
    logData.value = [];
    if (newValue.is_running) {
      open();
      send(JSON.stringify({ type: "log", log_key: newValue.project_id }));
    } else {
      close();
    }
  },
);

const retry = () => {
  if (store.selectedBot?.project_id !== currentBot.value) logData.value = [];
  logData.value.push({
    message: "Retrying...",
  });
  open();
};
</script>

<template>
  <div class="w-full p-6 rounded-box bg-base-200 flex flex-col gap-2">
    <div class="flex justify-between gap-4">
      <div class="flex items-center gap-4">
        <span class="font-semibold">实例输出</span>
        <div
          v-if="status === 'OPEN'"
          class="badge badge-sm badge-success font-normal text-base-100"
        >
          已连接
        </div>
        <div v-else class="badge badge-sm badge-error font-normal text-base-100">
          未连接
        </div>
      </div>

      <div class="flex items-center gap-4">
        <button
          :class="{ 'btn btn-sm btn-ghost': true, hidden: status === 'OPEN' }"
          @click="retry()"
        >
          重连
        </button>
      </div>
    </div>

    <table
      ref="logShowTable"
      class="overflow-auto h-96 !flex table table-xs rounded-none"
    >
      <tbody>
        <tr
          v-for="item in logData"
          :key="item.message"
          :class="{
            'flex font-mono': true,
            'bg-error/50': item.level === 'ERROR',
            'bg-warning/50': item.level === 'WARNING',
          }"
        >
          <th
            v-if="item.time"
            class="sticky left-0 right-0 text-gray-500 pl-0 bg-base-200"
          >
            {{ item.time }}
          </th>
          <td v-if="item.level" class="flex">{{ item.level }}</td>
          <td :class="{ flex: true, 'pl-0 text-success': !item.time }">
            {{ item.message }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
