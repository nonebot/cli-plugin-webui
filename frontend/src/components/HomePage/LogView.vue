<script setup lang="ts">
import { appStore } from "@/store/global";
import api from "@/api";
import AnsiUp from "ansi_up";
import { onBeforeUnmount, ref, watch } from "vue";
import { getURL } from "@/utils";
import { notice } from "@/utils/notification";
import { ProcessLog } from "@/api/schemas";
import type { AxiosError } from "axios";

const ansiUp = new AnsiUp();

const viewProject = ref("");
const writeStdinInput = ref<HTMLInputElement>();
const websocket = ref<WebSocket>();

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
  await api.writeToProjectProcessStdin(content, projectID).catch(() => {
    writeToArea(`Input failed!`, ["text-red-500", "font-bold"]);
  });
};

const getHistoryLog = async (logID: string, logCount: number) => {
  await api
    .getProcessLogHistory(logID, logCount)
    .then((resp) => {
      const detail = resp.data.detail;
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
  if (!viewProject.value) return;

  websocket.value?.close();

  websocket.value = new WebSocket(
    getURL(`/api/v1/process/log/${viewProject.value}/ws`, true),
  );

  websocket.value.onopen = () => {
    const token = localStorage.getItem("jwtToken") ?? "";
    websocket.value?.send(token);
    if (websocket.value?.readyState === WebSocket.OPEN) {
      writeToArea("日志 WebSocket 已连接", ["text-green-500", "font-bold"]);
    }
  };

  websocket.value.onmessage = (event: MessageEvent) => {
    const data: ProcessLog = JSON.parse(event.data.toString());
    writeToArea(ansiUp.ansi_to_html(data.message));

    if (data.message === "Process finished.") {
      appStore().projectIsStop();
    }
  };

  websocket.value.onclose = () => {
    writeToArea("日志 WebSocket 已断开", ["text-red-500", "font-bold"]);
    websocket.value = undefined;
  };
};

onBeforeUnmount(() => {
  websocket.value?.close();
  clearArea();
});

// 切换查看实例的情况
watch(
  () => appStore().choiceProject,
  async (newValue) => {
    // 相同实例无需额外处理
    if (newValue.project_id === viewProject.value) {
      // 未连接就重新连接
      handleWebSocket();
      return;
    }

    viewProject.value = newValue.project_id;
    clearArea();
    if (viewProject.value) await getHistoryLog(viewProject.value, 50);
    handleWebSocket();
  },
);

// 查看当前实例运行状态的情况
watch(
  () => appStore().choiceProject.is_running,
  (newValue) => {
    if (newValue) {
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
      <div
        role="button"
        class="btn btn-xs md:btn-sm h-auto md:!h-10 rounded"
        @click="clearArea()"
      >
        清空日志
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
