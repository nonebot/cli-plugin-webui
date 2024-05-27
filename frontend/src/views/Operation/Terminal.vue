<script setup lang="ts">
import type { ProcessLog } from '@/client/api'
import { generateURLForWebUI } from '@/client/utils'
import { useNoneBotStore } from '@/stores'
import { useWebSocket } from '@vueuse/core'
import { onMounted, onUnmounted, ref, watch } from 'vue'

const store = useNoneBotStore()

const logData = ref<ProcessLog[]>([]),
  logShowTable = ref<HTMLElement>(),
  currentBot = ref('')

const { status, data, close, open, send } = useWebSocket<ProcessLog>(
  generateURLForWebUI('/v1/process/log/ws', true),
  {
    immediate: false,
    onConnected(ws) {
      const token = localStorage.getItem('token') ?? ''
      ws.send(token)

      if (store.selectedBot) {
        send(JSON.stringify({ type: 'log', log_key: store.selectedBot?.project_id }))
        currentBot.value = store.selectedBot?.project_id
      }
    }
  }
)
onMounted(() => {
  if (!store.selectedBot) return
  open()
})

onUnmounted(() => {
  close()
})

watch(
  () => data.value,
  (rawData) => {
    if (!rawData) return

    const data: ProcessLog = JSON.parse(rawData.toString())

    logData.value.push(data)
    if (logShowTable.value) logShowTable.value.scrollTop = logShowTable.value.scrollHeight
  }
)

watch(
  () => store.selectedBot,
  (newValue) => {
    if (!newValue) return

    if (newValue.project_id === currentBot.value) {
      if (status.value !== 'OPEN') open()
      return
    }

    currentBot.value = newValue.project_id
    logData.value = []
    if (newValue.is_running) {
      open()
      send(JSON.stringify({ type: 'log', log_key: newValue.project_id }))
    } else {
      close()
    }
  }
)

const retry = () => {
  if (store.selectedBot?.project_id !== currentBot.value) logData.value = []
  logData.value.push({
    message: 'Retrying...'
  })
  open()
}
</script>

<template>
  <div class="w-full p-6 rounded-box bg-base-200 flex flex-col gap-4">
    <div class="font-semibold flex justify-between gap-4">
      <div class="flex items-center gap-4">
        实例输出
        <div v-if="status === 'OPEN'" class="badge badge-sm badge-success font-normal text-white">
          已连接
        </div>
        <div v-else class="badge badge-sm badge-error font-normal text-white">未连接</div>
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

    <table ref="logShowTable" class="overflow-auto h-96 !flex table table-xs rounded-none">
      <tbody>
        <tr
          v-for="item in logData"
          :class="{
            'flex font-mono': true,
            'bg-error/50': item.level === 'ERROR',
            'bg-warning/50': item.level === 'WARNING'
          }"
        >
          <th class="sticky left-0 right-0 text-gray-500 pl-0">
            {{ item.time }}
          </th>
          <td class="flex">{{ item.level }}</td>
          <td class="flex">{{ item.message }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
