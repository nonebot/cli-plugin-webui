<script setup lang="ts">
import { computed, onUnmounted, ref, watch } from 'vue'
import { useAddBotStore } from '.'
import { ProjectService, type ProcessLog } from '@/client/api'
import { useWebSocket } from '@vueuse/core'
import { generateURLForWebUI } from '@/client/utils'
import { useNoneBotStore, useToastStore } from '@/stores'

const IS_FINISHED = '✨ Done!'
const IS_FAILED = '❌ Failed!'

const store = useAddBotStore()
const nonebotStore = useNoneBotStore()
const toast = useToastStore()

const logKey = ref('')
const isFailed = ref(false)
const logContainer = ref<HTMLElement>()
const logData = ref<ProcessLog[]>([])

const getLogData = computed(() => [...logData.value].reverse())

const addBot = async () => {
  if (isFailed.value) {
    isFailed.value = false
    store.warningMessage = ''

    logData.value = []
    logData.value.push({
      message: 'Retrying...'
    })
  }

  await ProjectService.addProjectV1ProjectAddPost({
    project_name: store.projectName,
    project_dir: store.projectPath,
    mirror_url: store.pythonMirror,
    adapters: store.adapters.map((obj) => obj.module_name) ?? [],
    plugins: store.plugins,
    plugin_dirs: store.pluginDirs
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
  toast.add('success', `添加实例 ${store.projectName} 成功`, '', 5000)
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
      store.addBotSuccess = true
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

onUnmounted(() => {
  close()
})
</script>

<template>
  <div class="flex flex-col gap-4">
    <div class="overflow-auto bg-base-200 rounded-lg p-4">
      <table v-if="!logKey" class="table table-sm w-full">
        <tbody>
          <tr>
            <th class="font-semibold text-base">实例名称</th>
            <td>{{ store.projectName }}</td>
          </tr>
          <tr>
            <th class="font-semibold text-base">实例路径</th>
            <td>{{ store.projectPath }}</td>
          </tr>
          <tr>
            <th class="font-semibold text-base">Python 镜像</th>
            <td>{{ store.pythonMirror }}</td>
          </tr>
          <tr>
            <th class="font-semibold text-base">实例适配器</th>
            <td class="flex items-center flex-wrap gap-2">
              <span
                v-for="adapter in store.adapters"
                :key="adapter.name"
                class="badge badge-ghost !bg-base-100"
              >
                {{ adapter.name }}
              </span>
              <span v-if="!store.adapters.length" class="text-base-content/50"> 未找到适配器 </span>
            </td>
          </tr>
          <tr>
            <th class="font-semibold text-base">实例插件</th>
            <td class="flex items-center flex-wrap gap-2">
              <span
                v-for="plugin in store.plugins"
                :key="plugin"
                class="badge badge-ghost !bg-base-100"
              >
                {{ plugin }}
              </span>
              <span v-if="!store.plugins.length" class="text-base-content/50"> 未找到插件 </span>
            </td>
          </tr>
          <tr>
            <th class="font-semibold text-base">插件加载目录</th>
            <td class="flex items-center flex-wrap gap-2">
              <span
                v-for="pluginDir in store.pluginDirs"
                :key="pluginDir"
                class="badge badge-ghost !bg-base-100"
              >
                {{ pluginDir }}
              </span>
              <span v-if="!store.pluginDirs.length" class="text-base-content/50">
                未找到插件目录
              </span>
            </td>
          </tr>
        </tbody>
      </table>

      <table v-else class="overflow-auto h-80 !flex table table-xs">
        <tbody ref="logContainer">
          <tr
            v-for="(log, index) in getLogData"
            :key="index"
            :class="{
              'flex font-mono': true,
              'bg-error/50': log.level === 'ERROR',
              'bg-warning/50': log.level === 'WARNING'
            }"
          >
            <th class="sticky left-0 right-0 text-gray-500 bg-base-200">
              {{ log.time }}
            </th>
            <td class="flex">{{ log.level }}</td>
            <td class="flex">{{ log.message }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="flex items-center justify-between">
      <button
        :class="{
          'btn btn-sm btn-primary text-base-100': true,
          'btn-disabled': store.isInstalling || store.addBotSuccess
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
              'btn-disabled': store.isInstalling || store.addBotSuccess
            }"
          >
            取消
          </button>
        </form>

        <form v-if="store.addBotSuccess" method="dialog">
          <button class="btn btn-sm btn-primary text-base-100" @click="finish()">完成</button>
        </form>
        <button
          v-else
          :class="{
            'btn btn-sm btn-primary text-base-100': true,
            'btn-disabled': store.isInstalling
          }"
          @click="addBot()"
        >
          {{ isFailed ? '重试' : '安装' }}
        </button>
      </div>
    </div>
  </div>
</template>
