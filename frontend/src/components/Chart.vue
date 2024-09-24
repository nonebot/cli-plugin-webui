<script setup lang="ts" generic="T extends (number | string)[]">
import { ref, watch } from 'vue'
import VChart from 'vue-echarts'
import { LineChart } from 'echarts/charts'
import { use } from 'echarts/core'
import { TooltipComponent, GridComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import type { ComposeOption } from 'echarts/core'
import type { LineSeriesOption } from 'echarts/charts'
import type { TooltipComponentOption, GridComponentOption } from 'echarts/components'
import type { LoadingOptions } from '@/types'

use([TooltipComponent, GridComponent, LineChart, CanvasRenderer])

type EChartsOption = ComposeOption<TooltipComponentOption | GridComponentOption | LineSeriesOption>

type ChartItemData = {
  name?: string
  data: T
}

const props = defineProps<{
  itemData: ChartItemData[]
  timeData: T
  isLoading?: boolean
  loadingOptions?: LoadingOptions
}>()

const parseValue = (value: any) => {
  return isNaN(Number(value)) ? 'unknown' : Number(value).toFixed(3)
}

const getData = (): EChartsOption => {
  return {
    tooltip: {
      trigger: 'axis',
      formatter: (params: any) => {
        let paramContent: string[] = []
        params.forEach((param: any) => {
          paramContent.push(`${param.seriesName}: ${parseValue(param.value)}`)
        })
        return paramContent.join('<br>')
      }
    },
    grid: {
      top: '20%',
      left: '10%',
      right: '5%',
      bottom: '20%'
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: []
    },
    yAxis: {
      type: 'value',
      splitNumber: 2,
      boundaryGap: [0, '100%']
    },
    series: []
  }
}

const option = ref<EChartsOption>(getData())

watch(props, () => {
  option.value.series = props.itemData.map((item, _) => {
    return {
      name: item.name,
      data: item.data,
      type: 'line',
      showSymbol: false
    }
  })
  option.value.xAxis = {
    data: props.timeData
  }
})
</script>

<template>
  <v-chart
    autoresize
    :loading="props.isLoading"
    :loadingOptions="props.loadingOptions"
    :option="option"
  ></v-chart>
</template>
