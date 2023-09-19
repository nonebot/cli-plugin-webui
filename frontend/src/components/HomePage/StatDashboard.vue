<script setup lang="ts">
import StatDashboardChart from "@/components/HomePage/StatDashboardChart.vue";
import { WebsocketWrapper } from "@/utils/ws";
import { systemStatStore, projectStatStore } from "@/store/status";
import { appStore } from "@/store/global";
import { ProcessInfo } from "@/api/models";
import { notice } from "@/utils/notification";
import { onBeforeUnmount, onMounted, ref, watch } from "vue";

const viewProject = ref("");
const websocket = ref<WebsocketWrapper>();

const handleProjectMonitorWebSocket = () => {
  if (websocket.value?.state.connected) {
    websocket.value.close();
  }

  websocket.value = new WebsocketWrapper(`/api/project/status/${viewProject.value}`);

  const maxRetries = 3;
  let retries = 0;
  let connected = false;

  while (!connected && retries < maxRetries) {
    try {
      websocket.value.connect();
      connected = true;
    } catch (error: any) {
      notice.error(`连接至实例性能检测 WebSocket 失败...(${retries + 1}/${maxRetries})`);
      retries++;
    }
  }

  if (!connected) {
    notice.error("连接至性能检测 WebSocket 失败");
    return;
  }

  projectStatStore().clearList();

  websocket.value.client.onmessage = (event: MessageEvent) => {
    const wsData: ProcessInfo = JSON.parse(event.data);

    if (!wsData.performance) {
      return;
    }

    const date = new Date();
    if (projectStatStore().timeList.length >= 100) {
      projectStatStore().timeList.shift();
    }
    projectStatStore().timeList.push(
      `${date.getHours()}:${date.getMinutes()}:${date.getSeconds()}`,
    );

    if (projectStatStore().cpuList.length >= 100) {
      projectStatStore().cpuList.shift();
    }
    projectStatStore().cpuList.push(Number(wsData.performance!.cpu.toFixed(3)) * 100);

    if (projectStatStore().memList.length >= 100) {
      projectStatStore().memList.shift();
    }
    projectStatStore().memList.push(Number(wsData.performance!.mem.toFixed(3)) * 100);
  };
};

const clearList = () => {
  projectStatStore().cpuList = Array(100).fill(0);
  projectStatStore().memList = Array(100).fill(0);
  projectStatStore().timeList = Array(100).fill(0);
};

onMounted(() => {
  if (appStore().choiceProject.project_id && appStore().choiceProject.is_running) {
    viewProject.value = appStore().choiceProject.project_id;
    handleProjectMonitorWebSocket();
  }
});

onBeforeUnmount(() => {
  websocket.value?.close();
});

watch(
  () => appStore().choiceProject,
  (newValue) => {
    viewProject.value = newValue.project_id;
    if (newValue.is_running) {
      clearList();
      handleProjectMonitorWebSocket();
    } else {
      websocket.value?.close();
    }
  },
);

watch(
  () => appStore().choiceProject.is_running,
  (newValue) => {
    if (newValue) {
      clearList();
      handleProjectMonitorWebSocket();
    }
  },
);
</script>

<template>
  <div
    :class="{
      'overflow-hidden relative w-full p-4 md:p-6 rounded shadow-none md:shadow-lg bg-base-200': true,
      hidden: !appStore().choiceProject.project_id,
    }"
  >
    <h3 class="xs:text-base md:text-xl">性能监控</h3>

    <Transition>
      <div v-if="appStore().choiceProject.project_id" class="mt-2 m-auto flex flex-wrap">
        <div class="w-1/2 h-44">
          <div class="relative h-full flex flex-col">
            <h3 class="text-xs font-bold">实例 CPU 利用率 (%)</h3>
            <div class="grow relative flex items-center">
              <div class="absolute top-0 mt-2 mb-2 text-xs">
                当前：{{
                  projectStatStore().cpuList[
                    projectStatStore().cpuList.length - 1
                  ].toFixed(2)
                }}
                %
              </div>
              <StatDashboardChart
                class="h-full w-full"
                chart-dom="cpuChart"
                item-name="CPU 利用率"
                :item-data="projectStatStore().cpuList"
                :time-data="projectStatStore().timeList"
              />
            </div>
          </div>
        </div>

        <div class="w-1/2 h-44">
          <div class="relative h-full flex flex-col">
            <h3 class="text-xs font-bold">实例内存使用率 (%)</h3>
            <div class="grow relative flex items-center">
              <div class="absolute top-0 mt-2 mb-2 text-xs">
                当前：{{
                  projectStatStore().memList[
                    projectStatStore().memList.length - 1
                  ].toFixed(2)
                }}
                %
              </div>
              <StatDashboardChart
                class="h-full w-full"
                chart-dom="memChart"
                item-name="内存利用率"
                :item-data="projectStatStore().memList"
                :time-data="projectStatStore().timeList"
              />
            </div>
          </div>
        </div>

        <div class="w-1/2 h-44">
          <div class="relative h-full flex flex-col">
            <h3 class="text-xs font-bold">平台网络吞吐 (Kbps)</h3>
            <div class="grow relative flex items-center">
              <div class="absolute top-0 mt-2 mb-2 text-xs">
                发送：{{
                  systemStatStore().netSentSpeedList[
                    systemStatStore().netSentSpeedList.length - 1
                  ].toFixed(3)
                }}
                接收：{{
                  systemStatStore().netRecvSpeedList[
                    systemStatStore().netRecvSpeedList.length - 1
                  ].toFixed(3)
                }}
              </div>
              <StatDashboardChart
                class="h-full w-full"
                chart-dom="netChart"
                item-name="发送"
                :item-data="systemStatStore().netSentSpeedList"
                another-item-name="接收"
                :another-item-data="systemStatStore().netRecvSpeedList"
                :time-data="systemStatStore().timeList"
              />
            </div>
          </div>
        </div>

        <div class="w-1/2 h-44">
          <div class="relative h-full flex flex-col">
            <h3 class="text-xs font-bold">平台硬盘 IO (MB)</h3>
            <div class="grow relative flex items-center">
              <div class="absolute top-0 mt-2 mb-2 text-xs">
                读取：{{
                  systemStatStore().diskReadSpeedList[
                    systemStatStore().diskReadSpeedList.length - 1
                  ].toFixed(3)
                }}
                写入：{{
                  systemStatStore().diskWriteSpeedList[
                    systemStatStore().diskWriteSpeedList.length - 1
                  ].toFixed(3)
                }}
              </div>
              <StatDashboardChart
                class="h-full w-full"
                chart-dom="diskChart"
                item-name="读取"
                :item-data="systemStatStore().diskReadSpeedList"
                another-item-name="写入"
                :another-item-data="systemStatStore().diskWriteSpeedList"
                :time-data="systemStatStore().timeList"
              />
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>
