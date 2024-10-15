<script setup lang="ts">
import { generateURLForWebUI } from '@/client/utils'
import ChartItem from '@/components/ChartItem.vue'
import { useWebSocket } from '@vueuse/core'
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'
import type { StatusInfo, ChartItem as ChartItemType } from './types'
import { useChartStore, useCustomStore, useNoneBotStore, useToastStore } from '@/stores'
import type { LoadingOptions } from '@/types'

const store = useCustomStore(),
  chartStore = useChartStore(),
  nonebotStore = useNoneBotStore()
const toast = useToastStore()

chartStore.addDataType('systemData', {
  diskReadSpeed: [0],
  diskWriteSpeed: [0],
  netSentSpeed: [0],
  netRecvSpeed: [0]
})

chartStore.addDataType('processData', {
  cpuPercent: [0],
  memPercent: [0]
})

chartStore.addDataType('timeData', {
  time: ['00:00:00']
})

const machineStatIsLoading = ref(true),
  processStatIsLoading = ref(true)

const { data, close, open, send } = useWebSocket<StatusInfo>(
  generateURLForWebUI('/v1/status/ws', true),
  {
    immediate: false,
    onConnected(ws) {
      const token = localStorage.getItem('token') ?? ''
      ws.send(token)

      if (nonebotStore.selectedBot) {
        ws.send(
          JSON.stringify({
            type: 'status',
            project_id: nonebotStore.selectedBot.project_id
          })
        )
      }

      if (store.isDebug) {
        toast.add('success', 'Debug: WebSocket 连接成功', 'views/Dashboard/MachineStat.vue', 5000)
      }
    },
    onDisconnected() {
      if (!store.isDebug) return
      toast.add('error', 'Debug: WebSocket 连接断开', 'views/Dashboard/MachineStat.vue', 5000)
    }
  }
)

watch(
  () => data.value,
  (rawData) => {
    if (!rawData) {
      machineStatIsLoading.value = true
      return
    } else {
      machineStatIsLoading.value = false
    }

    const data: StatusInfo = JSON.parse(rawData.toString())

    const convertToMB = (v: number) => v / 1024 / 1024
    const convertToKB = (v: number) => v / 1024

    const date = new Date()

    chartStore.updateData(
      'timeData',
      'time',
      `${date.getHours()}:${date.getMinutes()}:${date.getSeconds()}`
    )

    const diskSpeed = data.system.disk.speed
    const netSpeed = data.system.net.speed

    chartStore.updateData('systemData', 'diskReadSpeed', convertToMB(diskSpeed[0]))
    chartStore.updateData('systemData', 'diskWriteSpeed', convertToMB(diskSpeed[1]))
    chartStore.updateData('systemData', 'netSentSpeed', convertToKB(netSpeed[0]))
    chartStore.updateData('systemData', 'netRecvSpeed', convertToKB(netSpeed[1]))

    if (data.process && data.process.performance) {
      chartStore.updateData(
        'processData',
        'cpuPercent',
        Number(data.process.performance.cpu.toFixed(3)) * 100
      )
      chartStore.updateData(
        'processData',
        'memPercent',
        Number(data.process.performance.mem.toFixed(3)) * 100
      )
      processStatIsLoading.value = false
    } else {
      processStatIsLoading.value = true
    }
  }
)

onMounted(() => {
  open()
})

onUnmounted(() => {
  close()
})

watch(
  () => nonebotStore.selectedBot,
  (newValue) => {
    if (!newValue) return
    send(JSON.stringify({ type: 'status', project_id: newValue.project_id }))

    // bug: 重置数据后, 图表会停止更新
    // chartStore.resetData('processData')
  }
)

const loadingOptions: LoadingOptions = {
  text: '等待数据传入...',
  textColor: 'grey',
  maskColor: 'rgba(255, 255, 255, 0)',
  color: 'rgb(107 114 128)'
}

const chartItems: ChartItemType[] = [
  {
    title: '机器硬盘情况',
    subtitle: computed(() => {
      const lastReadSpeed = chartStore.dataRefs.systemData?.diskReadSpeed.slice(-1)[0]
      const lastWriteSpeed = chartStore.dataRefs.systemData?.diskWriteSpeed.slice(-1)[0]
      return `读取: ${Number(lastReadSpeed).toFixed(3)} MB/s, 写入: ${Number(
        lastWriteSpeed
      ).toFixed(3)} MB/s`
    }),
    isLoading: computed(() => machineStatIsLoading.value),
    timeData: chartStore.dataRefs.timeData?.time ?? [],
    data: [
      {
        name: '读取',
        data: chartStore.dataRefs.systemData?.diskReadSpeed ?? []
      },
      {
        name: '写入',
        data: chartStore.dataRefs.systemData?.diskWriteSpeed ?? []
      }
    ]
  },
  {
    title: '机器网络情况',
    subtitle: computed(() => {
      const lastSentSpeed = chartStore.dataRefs.systemData?.netSentSpeed.slice(-1)[0]
      const lastRecvSpeed = chartStore.dataRefs.systemData?.netRecvSpeed.slice(-1)[0]
      return `发送: ${Number(lastSentSpeed).toFixed(3)} KB/s, 接收: ${Number(lastRecvSpeed).toFixed(
        3
      )} KB/s`
    }),
    isLoading: computed(() => machineStatIsLoading.value),
    timeData: chartStore.dataRefs.timeData?.time ?? [],
    data: [
      {
        name: '发送',
        data: chartStore.dataRefs.systemData?.netSentSpeed ?? []
      },
      {
        name: '接收',
        data: chartStore.dataRefs.systemData?.netRecvSpeed ?? []
      }
    ]
  },
  {
    title: '实例 CPU 使用率',
    subtitle: computed(() => {
      const lastCpuPercent = chartStore.dataRefs.processData?.cpuPercent.slice(-1)[0]
      return `当前: ${Number(lastCpuPercent).toFixed(3)}%`
    }),
    isLoading: computed(() => processStatIsLoading.value),
    timeData: chartStore.dataRefs.timeData?.time ?? [],
    data: [
      {
        name: 'CPU 使用率',
        data: chartStore.dataRefs.processData?.cpuPercent ?? []
      }
    ]
  },
  {
    title: '实例内存使用率',
    subtitle: computed(() => {
      const lastMemPercent = chartStore.dataRefs.processData?.memPercent.slice(-1)[0]
      return `当前: ${Number(lastMemPercent).toFixed(3)}%`
    }),
    isLoading: computed(() => processStatIsLoading.value),
    timeData: chartStore.dataRefs.timeData?.time ?? [],
    data: [
      {
        name: '内存使用率',
        data: chartStore.dataRefs.processData?.memPercent ?? []
      }
    ]
  }
]
</script>

<template>
  <div class="grid gap-4 grid-cols-1 md:grid-cols-2">
    <div v-for="item in chartItems" :key="item.title" class="p-6 bg-base-200 rounded-box h-56">
      <div>{{ item.title }}</div>
      <div class="relative flex grow items-center h-full">
        <div class="absolute top-0 mt-2 mb-2 text-xs">{{ item.subtitle.value }}</div>
        <ChartItem
          :item-data="item.data"
          :time-data="item.timeData"
          :is-loading="item.isLoading?.value"
          :loading-options="loadingOptions"
        />
      </div>
    </div>
  </div>
</template>
