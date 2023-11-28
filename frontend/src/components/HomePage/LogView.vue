<script setup lang="ts">
import { appStore } from "@/store/global";
import api from "@/api";
import AnsiUp from "ansi_up";
import { onBeforeUnmount, ref, watch } from "vue";
import { getURL } from "@/utils";
import { ProcessLog } from "@/api/schemas";
import { useWebSocket } from "@vueuse/core";
import type { UseWebSocketReturn } from "@vueuse/core";

interface LogItem {
  content: string;
  classList: string[];
}

const ansiUp = new AnsiUp();

const writeStdinInput = ref<HTMLInputElement>(),
  websocket = ref<UseWebSocketReturn<any>>(),
  logShowArea = ref<HTMLElement>(),
  logItems = ref<LogItem[]>([]);

const writeToArea = (content: string, classList?: string[]) => {
  logItems.value.push({
    content: content,
    classList: classList ?? [],
  });
};

const clearArea = () => {
  console.log("clear log");
  logItems.value = [];
};

const writeStdin = async (content: string) => {
  const projectID = appStore().choiceProject.project_id;
  await api.writeToProjectProcessStdin(content, projectID).catch(() => {
    writeToArea(`Input failed!`, ["text-red-500", "font-bold"]);
  });
};

const handleKeydown = async (event: KeyboardEvent) => {
  if (event.key !== "Enter") {
    return;
  }

  event.preventDefault();
  if (writeStdinInput.value) {
    const message = writeStdinInput.value.value.trim();
    writeToArea(`> ${message}`, ["text-sky-500", "font-bold"]);
    writeStdinInput.value.value = "";
    if (message) {
      await writeStdin(message);
    }
  }
};

const reconnectWebSocket = () => {
  if (websocket.value?.status.value !== "OPEN") {
    websocket.value?.open();
  }
};

const changeProject = async (projectID: string) => {
  if (!projectID) return;
  clearArea();
  const logCount = 50;
  await api.getProcessLogHistory(projectID, logCount).then((resp) => {
    const detail = resp.data.detail;
    if (detail.length) {
      for (const log of detail) {
        writeToArea(ansiUp.ansi_to_html(log.message));
      }
      writeToArea("加载历史日志完成");
    }
    return Promise.resolve();
  });
  websocket.value?.send(JSON.stringify({ type: "log", project_id: projectID }));
};

websocket.value = useWebSocket(getURL("/api/v1/process/log/ws", true), {
  onConnected(ws) {
    const token = localStorage.getItem("jwtToken") ?? "";
    ws.send(token);
  },
  onMessage(_, event) {
    const data: ProcessLog = JSON.parse(event.data.toString());
    writeToArea(ansiUp.ansi_to_html(data.message));
    if (data.message === "Process finished.") {
      appStore().projectIsStop();
    }
  },
});

onBeforeUnmount(() => {
  websocket.value?.close();
  clearArea();
});

watch(
  () => [appStore().choiceProject.project_id, appStore().choiceProject.is_running],
  async (newValue, _) => {
    const [projectID, __] = newValue;
    await changeProject(projectID.toString());
  },
);
</script>

<template>
  <div
    :class="{
      '!mt-0 !mb-0 sm:m-8 md:m-12 lg:m-16 xl:m-20 2xl:m-28 p-4 md:p-6 rounded shadow-none md:shadow-lg bg-base-200': true,
      hidden: !appStore().choiceProject.project_id,
    }"
  >
    <div class="flex justify-between items-center">
      <h3 class="text-base md:text-xl">运行日志</h3>
      <div class="flex grid grid-cols-2 gap-4">
        <div
          role="button"
          class="btn btn-xs md:btn-sm h-auto md:!h-10 rounded"
          @click="clearArea()"
        >
          清空日志
        </div>

        <div
          role="button"
          :class="{
            'btn btn-xs md:btn-sm h-auto md:!h-10 rounded': true,
            'btn-disabled': String(websocket?.status) === 'OPEN',
          }"
          @click="reconnectWebSocket()"
        >
          重新连接
        </div>
      </div>
    </div>

    <div
      class="custom-y-scrollbar overflow-y-auto h-96 p-2 md:p-4 mt-2 bg-base-300 text-xs"
    >
      <table class="table">
        <tbody ref="logShowArea">
          <tr v-for="item in logItems" :class="item.classList">
            <td class="p-0" v-html="item.content"></td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="w-full">
      <div class="pl-4 w-full flex items-center bg-base-300">
        <div class="pointer-events-none">></div>
        <input
          type="text"
          ref="writeStdinInput"
          placeholder="请键入内容，回车以发送"
          class="p-4 input input-sm w-full rounded-none !outline-none bg-base-300"
          @keydown="handleKeydown"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.table :where(thead, tbody) :where(tr:not(:last-child)),
.table :where(thead, tbody) :where(tr:first-child:last-child) {
  border-bottom-width: 0;
}
</style>
