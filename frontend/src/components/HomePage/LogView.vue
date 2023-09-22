<script setup lang="ts">
import { appStore } from "@/store/global";
import { api } from "./client";
import AnsiUp from "ansi_up";
import { onBeforeUnmount, onMounted, ref, watch } from "vue";
import { WebsocketWrapper } from "@/utils/ws";
import { notice } from "@/utils/notification";
import { ProcessLog } from "@/api/models";
import { AxiosError } from "axios";

const ansiUp = new AnsiUp();

const viewProject = ref("");
const writeStdinInput = ref<HTMLInputElement>();
const websocket = ref<WebsocketWrapper>();

interface LogItem {
  content: string;
  classList: string[];
}

const logShowArea = ref<HTMLElement>();
const logItems = ref<LogItem[]>([]);

const writeToArea = (content: string, classList?: string[]) => {
  logItems.value.push({
    content: content,
    classList: classList ?? [],
  });
};

const clearArea = () => {
  logItems.value = [];
};

const writeStdin = async (content: string) => {
  const projectID = appStore().choiceProject.project_id;
  await api.writeStdin(projectID, content).catch(() => {
    writeToArea(`Input failed!`, ["text-red-500", "font-bold"]);
  });
};

const getHistoryLog = async (logID: string, logCount: number) => {
  await api
    .getProcessLogHistory(logID, logCount)
    .then((resp) => {
      const detail = resp.detail;
      if (detail.length) {
        for (const log of detail) {
          writeToArea(ansiUp.ansi_to_html(log.message));
        }
        writeToArea("加载历史日志完成");
      }
    })
    .catch((error: AxiosError) => {
      let reason: string;
      if (error.response) {
        reason = (error.response.data as { detail: string })?.detail;
      } else {
        reason = error.message;
      }
      notice.error(`获取历史日志失败：${reason}`);
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

const handleWebSocket = () => {
  if (websocket.value?.state.connected) {
    websocket.value.close();
  }

  websocket.value = new WebsocketWrapper(`/api/log/logs/${viewProject.value}`);

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

  websocket.value.client.onmessage = (event: MessageEvent) => {
    const data: ProcessLog = JSON.parse(event.data.toString());
    writeToArea(ansiUp.ansi_to_html(data.message));
    if (logShowArea.value) {
      const logRows = logShowArea.value.getElementsByTagName("tr");
      const lastLogRow = logRows[logRows.length - 1];
      lastLogRow.scrollIntoView({ behavior: "smooth", block: "end" });
    }

    if (data.message === "Process finished.") {
      appStore().projectIsStop();
    }
  };

  websocket.value.client.onopen = () => {
    writeToArea(" ");
    writeToArea("日志 WebSocket 已连接", ["text-green-500", "font-bold"]);
  };

  websocket.value.client.onclose = () => {
    writeToArea(" ");
    writeToArea("日志 WebSocket 已断开", ["text-red-500", "font-bold"]);
  };
};

onMounted(() => {
  if (appStore().choiceProject.is_running) {
    viewProject.value = appStore().choiceProject.project_id;
  }
});

onBeforeUnmount(() => {
  websocket.value?.close();
  clearArea();
});

watch(
  () => appStore().choiceProject,
  async (newValue) => {
    viewProject.value = newValue.project_id;
    if (websocket.value?.state.connected) {
      websocket.value.close();
    }
    clearArea();
    await getHistoryLog(viewProject.value, 50);
    handleWebSocket();
  },
);

watch(
  () => appStore().choiceProject.is_running,
  async (newValue) => {
    if (newValue) {
      clearArea();
      await getHistoryLog(viewProject.value, 50);
      handleWebSocket();
    }
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
      <div class="grid grid-cols-2 sm:gap-2 md:gap-4">
        <div
          role="button"
          class="mr-2 btn btn-xs md:btn-sm h-auto md:!h-10 rounded"
          @click="clearArea()"
        >
          清空日志
        </div>

        <div
          role="button"
          :class="{
            'btn btn-xs md:btn-sm h-auto md:!h-10 rounded': true,
            'btn-disabled': websocket?.state.connected,
          }"
          @click="handleWebSocket()"
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
