<script setup lang="ts">
import {
  ProjectService,
  StoreService,
  type Adapter as BaseAdapter,
  type Driver as BaseDriver,
  type nb_cli_plugin_webui__app__models__base__Plugin
} from '@/client/api'
import { compareSemanticVersion } from '@/client/utils'
import router from '@/router'
import { useNoneBotStore, useToastStore } from '@/stores'
import { useFetch } from '@vueuse/core'
import { onMounted, ref } from 'vue'

const store = useNoneBotStore()
const toast = useToastStore()

interface Plugin extends nb_cli_plugin_webui__app__models__base__Plugin {
  latestVersion?: string
  releases?: string[]
  selectedVersion?: string
}

interface Adapter extends BaseAdapter {
  latestVersion?: string
}

interface Driver extends BaseDriver {
  latestVersion?: string
}

const pluginsRef = ref<Plugin[]>()
const adaptersRef = ref<Adapter[]>()
const driversRef = ref<Driver[]>()

const getPlugins = async () => {
  const { data } = await ProjectService.getPluginsV1ProjectPluginsGet({
    query: { project_id: store.selectedBot!.project_id }
  })

  if (data) pluginsRef.value = data.detail
}

const getAdapters = async () => {
  const { data } = await ProjectService.getAdaptersV1ProjectAdaptersGet({
    query: { project_id: store.selectedBot!.project_id }
  })

  if (data) adaptersRef.value = data.detail
}

const getDrivers = async () => {
  const { data } = await ProjectService.getDriversV1ProjectDriversGet({
    query: { project_id: store.selectedBot!.project_id }
  })

  if (data) driversRef.value = data.detail
}

const getData = async () => {
  if (!store.selectedBot) {
    toast.add('error', '请先选择实例', '', 5000)
    return
  }

  await getPlugins()
  await getAdapters()
  await getDrivers()

  toast.add('info', '数据加载完成', '', 5000)
}

const updateLatestVersion = async () => {
  if (!store.selectedBot) {
    toast.add('error', '请先选择实例', '', 5000)
    return
  }

  const fetchLatestVersion = async (moduleName: string) => {
    const url = `https://pypi.org/pypi/${moduleName}/json`
    const { data } = await useFetch(url).json<{
      info: {
        version: string
      }
      releases: Record<string, any[]>
    }>()
    return data.value
  }

  if (pluginsRef.value) {
    pluginsRef.value = await Promise.all(
      pluginsRef.value.map(async (plugin: Plugin) => {
        plugin.latestVersion = 'ignore'
        const data = await fetchLatestVersion(plugin.module_name!)
        if (data) {
          plugin.latestVersion = data.info.version
          plugin.releases = Object.keys(data.releases)
          plugin.selectedVersion = plugin.version
        }
        return plugin
      })
    )
  }

  toast.add('info', '检查更新完成', '', 5000)
}

onMounted(async () => {
  await getData()
  await updateLatestVersion()
})

const uninstall = async (module: Plugin | Adapter | Driver) => {
  if (!store.selectedBot) return

  const moduleType = 'valid' in module ? 'plugin' : 'module'

  const { data, error } = await StoreService.uninstallNonebotModuleV1StoreNonebotUninstallPost({
    query: {
      env: store.selectedBot.use_env!,
      project_id: store.selectedBot.project_id
    },

    // @ts-ignore
    body: {
      ...module,
      module_type: moduleType
    }
  })

  if (error) {
    toast.add('error', `卸载失败, 原因：${error.detail?.toString()}`, '', 5000)
  }

  if (data) {
    await getData()
    toast.add('success', '卸载成功', '', 5000)
  }
}
</script>

<template>
  <div class="flex flex-col gap-4 w-full">
    <div class="w-full p-6 bg-base-200 rounded-box flex items-center">
      <div class="shrink-0 font-semibold text-lg">
        <h3>操作</h3>
      </div>

      <div class="w-full flex items-center justify-end gap-2">
        <button class="btn btn-sm shadow-none btn-primary text-base-100">检查更新</button>
        <button class="btn btn-sm shadow-none" @click="getData()">刷新</button>
      </div>
    </div>

    <div class="collapse">
      <input type="checkbox" />
      <div class="collapse-title">
        <h3>插件管理</h3>
      </div>

      <div class="collapse-content overflow-x-auto relative">
        <table class="table table-sm">
          <thead>
            <tr>
              <th>名称</th>
              <th>本地版本</th>
              <th>远程版本</th>
              <th>版本列表</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="plugin in pluginsRef"
              :key="plugin.module_name"
              class="hover:bg-base-300 transition-colors"
            >
              <th class="flex item-center gap-2 whitespace-nowrap">
                <span>{{ plugin.name }}</span>
                <span
                  v-if="compareSemanticVersion(plugin.version!, plugin.latestVersion!)"
                  class="badge badge-primary text-base-100 font-normal"
                >
                  可更新
                </span>
              </th>
              <td>{{ plugin.version }}</td>
              <td>{{ plugin.latestVersion }}</td>
              <td>
                <select
                  class="select select-sm"
                  :disabled="!plugin.releases"
                  v-model="plugin.selectedVersion"
                >
                  <option disabled>请选择</option>
                  <option v-for="version in plugin.releases" :key="version">
                    {{ version }}
                  </option>
                </select>
              </td>
              <td class="flex item-center gap-2">
                <button
                  class="btn btn-ghost btn-sm"
                  @click="router.push(`/settings?search=${plugin.module_name}`)"
                >
                  设置
                </button>
                <label class="swap btn btn-sm btn-ghost">
                  <input type="checkbox" />
                  <div class="swap-off" @click="uninstall(plugin)">卸载</div>
                  <div class="swap-on text-primary">确认</div>
                </label>
                <button
                  v-if="
                    compareSemanticVersion(plugin.version!, plugin.latestVersion!) ||
                    (plugin.version !== plugin.selectedVersion && plugin.selectedVersion)
                  "
                  class="btn btn-primary btn-sm text-base-100"
                >
                  更新
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="collapse">
      <input type="checkbox" />
      <div class="collapse-title">
        <h3>适配器管理</h3>
      </div>
      <div class="collapse-content">
        <div class="overflow-x-auto">
          <table class="table table-sm">
            <thead>
              <tr>
                <th>名称</th>
                <!-- <th>本地版本</th>
                <th>远程版本</th> -->
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="adapter in adaptersRef"
                :key="adapter.module_name"
                class="hover:bg-base-300 transition-colors"
              >
                <th>{{ adapter.name }}</th>
                <!-- <td>{{ adapter.version }}</td>
                <td>{{ adapter.latestVersion }}</td> -->
                <td class="flex item-center gap-2">
                  <button
                    class="btn btn-ghost btn-sm"
                    @click="router.push(`/settings?search=${adapter.module_name}`)"
                  >
                    设置
                  </button>
                  <button class="btn btn-ghost btn-sm">卸载</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div class="collapse">
      <input type="checkbox" />
      <div class="collapse-title">
        <h3>驱动器管理</h3>
      </div>
      <div class="collapse-content">
        <div class="overflow-x-auto">
          <table class="table table-sm">
            <thead>
              <tr>
                <th>名称</th>
                <!-- <th>本地版本</th>
                <th>远程版本</th> -->
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="driver in driversRef"
                :key="driver.module_name"
                class="hover:bg-base-300 transition-colors"
              >
                <th>{{ driver.name }}</th>
                <!-- <td>{{ driver.version }}</td>
                <td>{{ driver.latestVersion }}</td> -->
                <td class="flex item-center gap-2">
                  <button
                    class="btn btn-ghost btn-sm"
                    @click="router.push(`/settings?search=${driver.module_name}`)"
                  >
                    设置
                  </button>
                  <button class="btn btn-ghost btn-sm">卸载</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="css" scoped>
.collapse {
  @apply bg-base-200;
}

.collapse-title {
  @apply p-6;
}

.collapse-title > h3 {
  @apply font-semibold text-lg;
}

.collapse-content {
  @apply px-4;
}

.collapse[open] > :where(.collapse-content),
.collapse-open > :where(.collapse-content),
.collapse:focus:not(.collapse-close) > :where(.collapse-content),
.collapse:not(.collapse-close) > :where(input[type='checkbox']:checked ~ .collapse-content),
.collapse:not(.collapse-close) > :where(input[type='radio']:checked ~ .collapse-content) {
  @apply pb-4;
}

.collapse-title,
:where(.collapse > input[type='checkbox']),
:where(.collapse > input[type='radio']) {
  @apply min-h-0;
}
</style>
