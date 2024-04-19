<script setup lang="ts">
import { ProjectService, type ProcessLog } from '@/client/api'
import { useNoneBotStore } from '@/stores'
import { useWebSocket, type UseWebSocketReturn } from '@vueuse/core'
import { computed, onUnmounted, ref, watch, watchEffect } from 'vue'
import { generateURLForWebUI } from '@/client/utils'

const IS_FINISHED = '✨ Done!',
  IS_FAILED = '❌ Failed!'

const store = useNoneBotStore()

const logKey = ref(''),
  isFinished = ref(false),
  isFailed = ref(false),
  logShowArea = ref<HTMLElement>(),
  logData = ref<ProcessLog[]>([])

const doCreate = () => {
  ProjectService.createProjectV1ProjectCreatePost({
    is_bootstrap: store.template === 'bootstrap',
    use_src: store.useSrc,
    project_name: store.name,
    project_dir: store.projectPath,
    mirror_url: store.pythonMirror,
    drivers: store.drivers,
    adapters: store.adapters
  }).then((res) => {
    logKey.value = res.detail
    open()
  })
}

const { status, data, close, open } = useWebSocket<ProcessLog>(
  generateURLForWebUI('/v1/process/log/ws', true),
  {
    immediate: false,
    onConnected(ws) {
      const token = localStorage.getItem('token') ?? ''
      ws.send(token)
      ws.send(JSON.stringify({ type: 'log', log_key: logKey.value }))
    }
  }
)

watch(
  () => data.value,
  (rawData) => {
    if (!rawData) return

    const data: ProcessLog = JSON.parse(rawData.toString())

    logData.value.push(data)

    if (data.message === IS_FINISHED) {
      close()
      isFinished.value = true
      store.addNoneBotSuccess = true
    } else if (data.message === IS_FAILED) {
      close()
      isFailed.value = true
    }
  }
)

watch(
  () => status.value,
  (status) => {
    if (status === 'OPEN') {
      store.isInstalling = true
    } else if (status === 'CLOSED') {
      store.isInstalling = false
    }
  }
)

const getLogData = computed(() => [...logData.value].reverse())

const retry = () => {
  logData.value = []
  logData.value.push({
    message: 'Retrying...'
  })

  isFinished.value = false
  isFailed.value = false
  doCreate()
}

onUnmounted(() => {
  close()
  logData.value = []
})
</script>

<template>
  <div class="overflow-hidden bg-base-200 rounded-lg p-4">
    <div class="flex flex-col gap-4">
      <div v-if="!logKey">
        <table class="table w-auto">
          <tbody>
            <tr>
              <td class="font-semibold">实例名称</td>
              <td>{{ store.name }}</td>
            </tr>
            <tr>
              <td class="font-semibold">实例类型</td>
              <td>{{ store.template === 'bootstrap' ? '初学者 / 普通用户' : '开发者' }}</td>
            </tr>
            <tr v-if="store.template === 'simple'">
              <td class="font-semibold">实例插件加载位置</td>
              <td>{{ store.useSrc ? '/src' : `/${store.name}` }}</td>
            </tr>
            <tr>
              <td class="font-semibold">实例路径</td>
              <td>(Base Dir)/{{ store.projectPath }}</td>
            </tr>
            <tr>
              <td class="font-semibold">Python 镜像</td>
              <td>{{ store.pythonMirror }}</td>
            </tr>
            <tr>
              <td class="font-semibold">驱动器</td>
              <td>
                <div class="flex items-center gap-2">
                  <div v-for="driver in store.drivers" class="badge">{{ driver.name }}</div>
                </div>
              </td>
            </tr>
            <tr>
              <td class="font-semibold">适配器</td>
              <td>
                <div class="flex items-center gap-2">
                  <div v-for="adapter in store.adapters" class="badge">{{ adapter.name }}</div>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <table v-else class="overflow-auto h-80 !flex table table-xs">
        <tbody ref="logShowArea">
          <tr
            v-for="item in getLogData"
            :class="{
              'flex font-mono': true,
              'bg-error/50': item.level === 'ERROR',
              'bg-warning/50': item.level === 'WARNING'
            }"
          >
            <th class="sticky left-0 right-0 bg-base-200 text-gray-500">{{ item.time }}</th>
            <td class="flex">{{ item.level }}</td>
            <td class="flex">{{ item.message }}</td>
          </tr>
        </tbody>
      </table>

      <div v-if="!logKey" class="bg-base-content/10 h-px"></div>

      <div class="flex justify-end gap-4">
        <button v-if="isFailed" class="btn btn-sm btn-outline" @click="retry">重试</button>

        <button v-if="!logKey" class="btn btn-sm btn-primary text-white" @click="doCreate">
          确认并安装依赖
        </button>
      </div>
    </div>
  </div>
</template>
