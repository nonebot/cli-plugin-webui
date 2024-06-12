<script setup lang="ts">
import type { ProcessLog } from '@/client/api'
import { generateURLForWebUI } from '@/client/utils'
import { useCustomStorage } from '@/stores'
import { useWebSocket } from '@vueuse/core'
import { onUnmounted, ref, watch } from 'vue'

const store = useCustomStorage()

const props = defineProps<{
  logKey: string
}>()

const emit = defineEmits(['retry', 'finished'])

const logViewModal = ref<HTMLDialogElement>()

defineExpose({
  openModal: () => {
    logViewModal.value?.showModal()
  },
  closeModal: () => {
    logViewModal.value?.close()
  }
})

const logData = ref<ProcessLog[]>([]),
  logContainer = ref<HTMLElement>(),
  isFailed = ref(false),
  isInstalling = ref(false)

const { status, data, close, open } = useWebSocket<ProcessLog>(
  generateURLForWebUI('/v1/process/log/ws', true),
  {
    immediate: false,
    onConnected(ws) {
      const token = localStorage.getItem('token') ?? ''
      ws.send(token)
      ws.send(JSON.stringify({ type: 'log', log_key: props.logKey }))
    }
  }
)

onUnmounted(() => {
  close()
})

watch(
  () => status.value,
  (newValue) => {
    isInstalling.value = newValue === 'OPEN'

    if (store.isDebug) {
      logData.value.push({ message: `WebSocket connection status: ${newValue}` })
    }
  }
)

watch(
  () => data.value,
  (newValue) => {
    if (!newValue) return

    const data: ProcessLog = JSON.parse(newValue.toString())

    logData.value.push(data)

    if (data.message === '❌ Failed!') {
      isFailed.value = true
    }
    if (data.message === '✨ Done!') {
      close()
    }

    if (logContainer.value) {
      logContainer.value.scrollTop = logContainer.value.scrollHeight
    }
  }
)

watch(
  () => props.logKey,
  (newValue) => {
    if (!newValue) return
    logData.value = []
    open()
  }
)
</script>

<template>
  <dialog ref="logViewModal" class="modal">
    <div class="modal-box max-w-5xl rounded-lg flex flex-col gap-4">
      <h3 class="font-semibold text-lg">安装概览</h3>

      <div class="overflow-hidden rounded-lg bg-base-200 p-4">
        <table ref="logContainer" class="overflow-auto h-96 !flex table table-xs">
          <tbody>
            <tr
              v-for="log in logData"
              :class="{
                'flex font-mono': true,
                'bg-error/50': log.level === 'ERROR',
                'bg-warning/50': log.level === 'WARNING'
              }"
            >
              <th v-if="log.time" class="sticky left-0 right-0 text-gray-500">{{ log.time }}</th>
              <td v-if="log.level" class="flex">{{ log.level }}</td>
              <td class="flex">{{ log.message }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="flex items-center gap-2">
        <button
          :class="{ 'btn btn-sm': true, 'btn-disabled': isInstalling }"
          @click="logViewModal?.close()"
        >
          取消
        </button>

        <div class="w-full"></div>

        <button
          :class="{ 'btn btn-sm': true, 'btn-disabled': isInstalling || !isFailed }"
          @click="emit('retry', true)"
        >
          重试
        </button>
        <button
          :class="{
            'btn btn-sm btn-primary text-white': true,
            'btn-disabled': isFailed || isInstalling
          }"
          @click="emit('finished', true), logViewModal?.close()"
        >
          完成
        </button>
      </div>
    </div>
  </dialog>
</template>
