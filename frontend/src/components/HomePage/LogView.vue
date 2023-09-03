<script setup lang="ts">
import { appStore } from "@/store/global";
import { API } from "@/api";
import AnsiUp from "ansi_up";
import { onMounted, onUnmounted, ref, watch } from "vue";
import { WebUIWebSocket } from "@/utils/ws";
import { globalLog as log } from "@/main";
import { ProcessLog } from "@/api/models";

const ansiUp = new AnsiUp();
const api = new API();

const viewProject = ref("");
const viewArea = ref<HTMLElement>();
const writeStdinInput = ref<HTMLInputElement>();
const ws = ref<WebUIWebSocket>();

const writeToArea = (content: string, classList?: string[]) => {
  if (viewArea.value) {
    viewArea.value.innerHTML += `
      <tr class="flex border-0">
        <td class="p-0 ${classList?.join(" ")}">${content}</td>
      </tr>
    `;
  }
};

const clearArea = () => {
  if (viewArea.value) {
    viewArea.value.innerHTML = "";
  }
};

const writeStdin = async (content: string) => {
  const projectID = appStore().choiceProject.project_id;
  await api.writeStdin(projectID, content).catch(() => {
    writeToArea(`Input failed!`, ["text-red-500", "font-bold"]);
    return;
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
    .catch((error) => {
      log.error(`获取历史日志失败：${error}`);
    });
};

const handleWebSocket = async () => {
  clearArea();
  await getHistoryLog(viewProject.value, 50);

  const newWebSocket = () => {
    ws.value = new WebUIWebSocket(`/api/log/logs/${viewProject.value}`);
  };

  if (!ws.value) {
    newWebSocket();
  } else {
    if (
      ws.value.isConnected() &&
      viewProject.value !== appStore().choiceProject.project_id
    ) {
      ws.value.client?.close();
    }
    newWebSocket();
  }

  const maxRetries = 3;
  let retries = 0;
  let connected = false;

  while (!connected && retries < maxRetries) {
    try {
      ws.value!.connect();
      connected = true;
    } catch (error: any) {
      console.log(`连接至日志 WebSocket 失败...(${retries + 1}/${maxRetries})`);
      retries++;
    }
  }

  if (!connected) {
    log.error("连接至日志 WebSocket 失败");
    return;
  }

  ws.value!.client!.onmessage = (event: MessageEvent) => {
    const data: ProcessLog = JSON.parse(event.data.toString());
    writeToArea(ansiUp.ansi_to_html(data.message));

    if (data.message === "Process finished.") {
      appStore().projectIsStop();
    }
  };

  ws.value!.client!.onopen = () => {
    writeToArea(" ");
    writeToArea("日志 WebSocket 已连接", ["text-green-500", "font-bold"]);
  };

  ws.value!.client!.onclose = () => {
    writeToArea(" ");
    writeToArea("日志 WebSocket 已断开", ["text-red-500", "font-bold"]);
  };
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

onMounted(async () => {
  if (appStore().choiceProject.project_id && appStore().choiceProject.is_running) {
    viewProject.value = appStore().choiceProject.project_id;
    await handleWebSocket();
  }
});

onUnmounted(() => {
  if (ws.value?.isConnected()) {
    ws.value.client?.close();
  }
});

watch(
  () => appStore().choiceProject,
  async (newValue) => {
    // 检测不同实例间切换
    if (viewProject.value !== newValue.project_id) {
      viewProject.value = newValue.project_id;
    }
    await handleWebSocket();
  },
);

watch(
  () => appStore().choiceProject.is_running,
  async () => {
    if (
      viewProject.value === appStore().choiceProject.project_id &&
      appStore().choiceProject.is_running
    ) {
      await handleWebSocket();
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
            'btn-disabled': !ws?.client?.CLOSED,
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
        <tbody ref="viewArea"></tbody>
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

<style>
.table .log-view-area :where(thead, tbody) :where(tr:not(:last-child)) {
  border-bottom-width: 0;
}
</style>
