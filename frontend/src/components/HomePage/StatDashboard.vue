<script setup lang="ts">
import StatDashboardChart from "@/components/HomePage/StatDashboardChart.vue";
import { useStatusStore } from "@/store/status";
import { appStore } from "@/store/global";
import { onMounted, watch, computed, ComputedRef } from "vue";
import { statusWebSocket } from "@/components/HomePage/client";

interface StatChartData {
  title: string;
  subtitle: ComputedRef<string>;
  chartDomName: string;
  timeData: any[];
  yDataName: string;
  yData: any[];
  yAnotherDataName?: string;
  yAnotherData?: any[];
}

const statStore = useStatusStore();

const chartData: StatChartData[] = [
  {
    title: "实例 CPU 利用率 (%)",
    subtitle: computed(() => {
      const lastData =
        statStore.process.cpuPercentList[
          statStore.process.cpuPercentList.length - 1
        ].toFixed(2);
      return `当前: ${lastData} %`;
    }),
    chartDomName: "cpu-chart",
    timeData: statStore.timeList,
    yDataName: "CPU 利用率",
    yData: statStore.process.cpuPercentList,
  },
  {
    title: "实例内存使用率 (%)",
    subtitle: computed(() => {
      const lastData =
        statStore.process.memPercentList[
          statStore.process.memPercentList.length - 1
        ].toFixed(2);
      return `当前: ${lastData} %`;
    }),
    chartDomName: "mem-chart",
    timeData: statStore.timeList,
    yDataName: "内存利用率(压力)",
    yData: statStore.process.memPercentList,
  },
  {
    title: "平台网络吞吐 (Kbps)",
    subtitle: computed(() => {
      const lastSentDataSpeed =
        statStore.system.netSentSpeedList[
          statStore.system.netSentSpeedList.length - 1
        ].toFixed(3);
      const lastRecvDataSpeed =
        statStore.system.netRecvSpeedList[
          statStore.system.netRecvSpeedList.length - 1
        ].toFixed(3);
      return `发送: ${lastSentDataSpeed} 接收: ${lastRecvDataSpeed}`;
    }),
    chartDomName: "net-chart",
    timeData: statStore.timeList,
    yDataName: "发送",
    yData: statStore.system.netSentSpeedList,
    yAnotherDataName: "接收",
    yAnotherData: statStore.system.netRecvSpeedList,
  },
  {
    title: "平台硬盘 IO (MB)",
    subtitle: computed(() => {
      const lastReadSpeed =
        statStore.system.diskReadSpeedList[
          statStore.system.diskReadSpeedList.length - 1
        ].toFixed(3);
      const lastWriteSpeed =
        statStore.system.diskWriteSpeedList[
          statStore.system.diskWriteSpeedList.length - 1
        ].toFixed(3);
      return `读取: ${lastReadSpeed} 写入: ${lastWriteSpeed}`;
    }),
    chartDomName: "disk-chart",
    timeData: statStore.timeList,
    yDataName: "读取",
    yData: statStore.system.diskReadSpeedList,
    yAnotherDataName: "写入",
    yAnotherData: statStore.system.diskWriteSpeedList,
  },
];

const changeProject = (projectID: string) => {
  statusWebSocket?.send(
    JSON.stringify({
      type: "status",
      project_id: projectID,
    }),
  );
};

onMounted(() => {
  if (appStore().choiceProject.project_id && appStore().choiceProject.is_running) {
    changeProject(appStore().choiceProject.project_id);
  }
});

watch(
  () => appStore().choiceProject,
  (newValue) => {
    if (newValue.is_running) {
      statStore.clearProcessList();
      changeProject(newValue.project_id);
    }
  },
);

watch(
  () => appStore().choiceProject.is_running,
  (newValue) => {
    if (newValue) {
      changeProject(appStore().choiceProject.project_id);
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
        <div v-for="data in chartData" class="w-1/2 h-44">
          <div class="relative h-full flex flex-col">
            <h3 class="text-xs font-bold">{{ data.title }}</h3>
            <div class="grow relative flex items-center">
              <div class="absolute top-0 mt-2 mb-2 text-xs">
                {{ data.subtitle.value }}
              </div>
              <StatDashboardChart
                class="h-full w-full"
                :chart-dom="data.chartDomName"
                :time-data="data.timeData"
                :item-name="data.yDataName"
                :item-data="data.yData"
                :another-item-name="data?.yAnotherDataName"
                :another-item-data="data?.yAnotherData"
              />
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>
