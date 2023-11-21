<script setup lang="ts" generic="T extends number | string, U extends string">
import { onMounted, ref, watch } from "vue";
import * as echarts from "echarts";
import { appStore } from "@/store/global";

const props = withDefaults(
  defineProps<{
    chartDom: string;
    timeData: U[];
    itemName?: string;
    itemData: T[];
    anotherItemName?: string;
    anotherItemData?: T[];
  }>(),
  {
    itemName: () => "",
    anotherItemName: () => "",
    anotherItemData: () => [],
  },
);

const chartElement = ref<HTMLElement>();
const chartParser = ref<echarts.ECharts>();

const parseValue = (value: any) => {
  if (isNaN(Number(value))) {
    return "unknown";
  } else {
    return Number(value).toFixed(3);
  }
};

const chartOptions = {
  tooltip: {
    trigger: "axis",
    formatter: function (params: any) {
      if (!props.anotherItemName) {
        const param = params[0];
        return `
          ${param.name}: ${parseValue(param.value)}
        `;
      } else {
        const fParam = params[0];
        const sParam = params[1];
        return `
          ${fParam.name}<br>
          ${fParam.seriesName}: ${parseValue(fParam.value)}<br>
          ${sParam.seriesName}: ${parseValue(sParam.value)}
        `;
      }
    },
  },
  grid: {
    top: "20%",
    left: "12%",
    right: "12%",
    bottom: "20%",
  },
  xAxis: {
    type: "category",
    boundaryGap: false,
    data: [],
  },
  yAxis: {
    type: "value",
    splitNumber: 2,
    boundaryGap: [0, "100%"],
  },
  series: [
    {
      data: [],
      type: "line",
      showSymbol: false,
    },
    {
      data: [],
      type: "line",
      showSymbol: false,
    },
  ],
} as echarts.EChartsOption;

const createChart = () => {
  if (chartElement.value && !chartParser.value) {
    chart = echarts.init(chartElement.value);
    chart.setOption(chartOptions);
  }
};

let chart: echarts.ECharts;

let resizeChart: string | number | NodeJS.Timeout | undefined;
window.addEventListener("resize", () => {
  clearTimeout(resizeChart);
  resizeChart = setTimeout(() => {
    chart.dispose();
    createChart();
  }, 100);
});

onMounted(() => {
  createChart();
});

watch(props, () => {
  chart.setOption({
    xAxis: {
      data: props.timeData,
    },
    series: [
      {
        name: props.itemName,
        data: props.itemData,
      },
      {
        name: props.anotherItemName,
        data: props.anotherItemData,
      },
    ],
  } as echarts.EChartsOption);
});

watch(
  () => appStore().choiceProject.project_id,
  () => {
    createChart();
  },
);
</script>

<template>
  <div ref="chartElement"></div>
</template>
