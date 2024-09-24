<script setup lang="ts">
import { ProjectService, type ProcessLog } from '@/client/api'
import { useWebSocket } from '@vueuse/core'
import { computed, onUnmounted, ref, watch } from 'vue'
import { generateURLForWebUI } from '@/client/utils'
import { useCreateBotStore } from '.'
import { useNoneBotStore, useToastStore } from '@/stores'

const IS_FINISHED = '✨ Done!',
  IS_FAILED = '❌ Failed!'

const store = useCreateBotStore()
const toast = useToastStore()
const nonebotStore = useNoneBotStore()

const logKey = ref('')
const isFailed = ref(false)
const logContainer = ref<HTMLElement>()
const logData = ref<ProcessLog[]>([])

const createBot = async () => {
  if (isFailed.value) {
    isFailed.value = false
    store.warningMessage = ''

    logData.value = []
    logData.value.push({
      message: 'Retrying...'
    })
  }

  await ProjectService.createProjectV1ProjectCreatePost({
    is_bootstrap: store.template === 'bootstrap',
    use_src: store.useSrc,
    project_name: store.projectName,
    project_dir: store.projectPath,
    mirror_url: store.pythonMirror,
    drivers: store.drivers,
    adapters: store.adapters
  })
    .then((res) => {
      logKey.value = res.detail
      open()
    })
    .catch((err) => {
      store.warningMessage = err.body ? err.body.detail : err
      isFailed.value = true
    })
}

const finish = async () => {
  await nonebotStore.loadBots()
  toast.add('success', `创建实例 ${store.projectName} 成功`, '', 5000)
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
      store.createBotSuccess = true
    } else if (data.message === IS_FAILED) {
      close()
      isFailed.value = true
    }
  }
)

watch(
  () => status.value,
  (status) => {
    store.isInstalling = status === 'OPEN'
  }
)

const getLogData = computed(() => [...logData.value].reverse())

onUnmounted(() => {
  close()
})
</script>

<template>
  <div class="overflow-hidden flex flex-col gap-4">
    <div class="overflow-auto bg-base-200 rounded-lg p-4">
      <table v-if="!logKey" class="table table-sm w-full">
        <tbody>
          <tr>
            <th class="font-semibold text-base">实例名称</th>
            <td>{{ store.projectName }}</td>
          </tr>
          <tr>
            <th class="font-semibold text-base">实例类型</th>
            <td>{{ store.template === 'bootstrap' ? '初学者 / 普通用户' : '开发者' }}</td>
          </tr>
          <tr v-if="store.template === 'simple'">
            <th class="font-semibold text-base">实例插件加载位置</th>
            <td>{{ store.useSrc ? '/src' : `/${store.projectName}` }}</td>
          </tr>
          <tr>
            <th class="font-semibold text-base">实例路径</th>
            <td>(Base Dir)/{{ store.projectPath }}</td>
          </tr>
          <tr>
            <th class="font-semibold text-base">Python 镜像</th>
            <td>{{ store.pythonMirror }}</td>
          </tr>
          <tr>
            <th class="font-semibold text-base">驱动器</th>
            <td class="flex flex-wrap items-center gap-2">
              <span v-for="driver in store.drivers" class="badge" :key="driver.name">
                {{ driver.name }}
              </span>
            </td>
          </tr>
          <tr>
            <td class="font-semibold text-base">适配器</td>
            <td class="flex flex-wrap items-center gap-2">
              <span v-for="adapter in store.adapters" class="badge" :key="adapter.name">
                {{ adapter.name }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>

      <table v-else class="overflow-auto h-80 !flex table table-xs">
        <tbody ref="logContainer">
          <tr
            v-for="(item, index) in getLogData"
            :key="index"
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
    </div>

    <div class="flex items-center justify-between">
      <button
        :class="{
          'btn btn-sm btn-primary text-base-100': true,
          'btn-disabled': store.isInstalling || store.createBotSuccess
        }"
        @click="store.step--"
      >
        上一步
      </button>

      <div class="flex items-center gap-2">
        <form method="dialog">
          <button
            :class="{
              'btn btn-sm': true,
              'btn-disabled': store.isInstalling || store.createBotSuccess
            }"
          >
            取消
          </button>
        </form>

        <form v-if="store.createBotSuccess" method="dialog">
          <button class="btn btn-sm btn-primary text-base-100" @click="finish()">完成</button>
        </form>
        <button
          v-else
          :class="{
            'btn btn-sm btn-primary text-base-100': true,
            'btn-disabled': store.isInstalling
          }"
          @click="createBot()"
        >
          {{ isFailed ? '重试' : '安装' }}
        </button>
      </div>
    </div>
  </div>
</template>
