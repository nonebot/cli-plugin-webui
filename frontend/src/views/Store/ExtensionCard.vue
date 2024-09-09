<script
  setup
  lang="ts"
  generic="
    T extends
      | nb_cli_plugin_webui__app__schemas__Plugin
      | nb_cli_plugin_webui__app__schemas__ModuleInfo
  "
>
import {
  SearchTag,
  StoreService,
  type nb_cli_plugin_webui__app__schemas__ModuleInfo,
  type nb_cli_plugin_webui__app__schemas__Plugin
} from '@/client/api'
import type { PypiInfo } from '@/views/Store/types'
import { useFetch } from '@vueuse/core'
import { computed, ref } from 'vue'
import { useSearchStore } from './client'
import { useNoneBotStore } from '@/stores'
import LogView from '@/components/Modals/Global/LogView.vue'
import { useToastStore } from '@/stores/ToastStorage'

const store = useSearchStore(),
  nonebotStore = useNoneBotStore()

const toast = useToastStore()

const props = defineProps<{
  data: T
}>()

const extensionCardModal = ref<HTMLDialogElement>(),
  pypiData = ref<PypiInfo>(),
  logViewModal = ref<InstanceType<typeof LogView> | null>(),
  installLogKey = ref(''),
  extensionUninstallConfirmModal = ref<HTMLDialogElement>()

const open = async () => {
  extensionCardModal.value?.showModal()

  const pypiURL = `https://pypi.org/pypi/${props.data.project_link}/json`
  const { data } = await useFetch(pypiURL).json<PypiInfo>()
  if (data.value) pypiData.value = data.value
}

const isTestPassed = (data: T): boolean => {
  if ('valid' in data && 'skip_test' in data) {
    return data.valid && !data.skip_test
  }
  return false
}

const installModule = async (module: T) => {
  if (!nonebotStore.selectedBot || !module) return

  const moduleType = 'valid' in module ? 'plugin' : 'module'

  await StoreService.installNonebotModuleV1StoreNonebotInstallPost(
    nonebotStore.enabledEnv,
    nonebotStore.selectedBot?.project_id,

    // TODO: 因后端实现需借助 module_type 以区分传入的类型, 而其所需类型为私有类型, 无法直接引用。待修复
    // @ts-ignore
    { ...module, module_type: moduleType }
  )
    .then((res) => {
      installLogKey.value = res.detail
      logViewModal.value?.openModal()
    })
    .catch((err) => {
      let detail = ''
      if (err.body) {
        detail = err.body.detail
      } else {
        detail = err
      }
      toast.add('error', `提交安装失败, 原因：${detail}`, '', 5000)
    })
}

const uninstallModule = async (module: T) => {
  if (!nonebotStore.selectedBot || !module) return
  if (!module.is_download) return

  const moduleType = 'valid' in module ? 'plugin' : 'module'

  await StoreService.uninstallNonebotModuleV1StoreNonebotUninstallPost(
    nonebotStore.enabledEnv,
    nonebotStore.selectedBot.project_id,

    // @ts-ignore
    { ...module, module_type: moduleType }
  )
    .then(() => {
      extensionUninstallConfirmModal.value?.close()
      store.updateData(nonebotStore.selectedBot!.project_id, false)
      toast.add('success', '卸载成功', '', 5000)
    })
    .catch((err) => {
      let detail = ''
      if (err.body) {
        detail = err.body.detail
      } else {
        detail = err
      }
      toast.add('error', `卸载失败, 原因：${detail}`, '', 5000)
    })
}

const isRetry = () => {
  installModule(props.data)
}

const isFinished = async () => {
  await store.updateData(nonebotStore.selectedBot!.project_id, false)
}

const getUpdateTime = computed(() => {
  if (!('time' in props.data)) return 'ignore'

  const time = new Date(props.data.time)
  const now = new Date()
  const diff = now.getTime() - time.getTime()
  const diffHours = diff / (1000 * 60 * 60)
  const diffDays = diff / (1000 * 60 * 60 * 24)
  const diffMonths = diff / (1000 * 60 * 60 * 24 * 30)
  const diffYears = diff / (1000 * 60 * 60 * 24 * 365)

  if (diffYears >= 1) {
    return `${Math.floor(diffYears)}年前`
  } else if (diffMonths >= 1) {
    return `${Math.floor(diffMonths)}个月前`
  } else if (diffDays >= 1) {
    return `${Math.floor(diffDays)}天前`
  } else if (diffHours >= 1) {
    return `${Math.floor(diffHours)}小时前`
  } else {
    return '刚刚'
  }
})
</script>

<template>
  <LogView
    ref="logViewModal"
    :log-key="installLogKey"
    v-on:retry="isRetry"
    v-on:finished="isFinished"
  />

  <dialog ref="extensionUninstallConfirmModal" class="modal">
    <div class="modal-box rounded-lg flex flex-col gap-4">
      <h3 class="font-semibold text-lg">确认吗</h3>

      <div class="w-full grid grid-cols-2 gap-4">
        <button class="btn btn-sm" @click="uninstallModule(props.data)">确定</button>
        <button class="btn btn-sm" @click="extensionUninstallConfirmModal?.close()">取消</button>
      </div>
    </div>
  </dialog>

  <dialog ref="extensionCardModal" class="modal">
    <div class="modal-box rounded-lg flex flex-col gap-4">
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-4">
          <div class="h-12 w-12 rounded-full overflow-hidden">
            <img :src="`https://github.com/${props.data.author}.png?size=100`" />
          </div>

          <div class="flex flex-col justify-between">
            <div class="font-semibold opacity-80">{{ props.data.name }}</div>
            <a
              :href="`https://github.com/${props.data.author}`"
              class="link link-hover hover:link-primary text-sm"
            >
              @{{ props.data.author }}
            </a>
          </div>
        </div>

        <div class="flex items-center gap-2">
          <a
            v-if="isTestPassed(props.data)"
            :href="`https://registry.nonebot.dev/plugin/${props.data.project_link}:${props.data.module_name}`"
            target="_blank"
            class="btn btn-sm btn-success text-white"
          >
            测试通过
          </a>
          <a
            v-else
            :href="`https://registry.nonebot.dev/plugin/${props.data.project_link}:${props.data.module_name}`"
            target="_blank"
            class="btn btn-sm btn-error text-white"
          >
            测试未通过
          </a>

          <button
            v-if="props.data.is_download"
            class="btn btn-sm"
            @click="extensionUninstallConfirmModal?.showModal()"
          >
            卸载
          </button>
          <button v-else class="btn btn-sm" @click="installModule(props.data)">安装</button>
        </div>
      </div>

      <div class="bg-base-content/10 h-px"></div>

      <div class="flex justify-between gap-2">
        <div class="flex flex-col justify-between">
          <div class="opacity-70 text-sm">{{ props.data.desc }}</div>

          <div class="flex flex-wrap items-center gap-2">
            <div
              v-for="tag in props.data.tags"
              :key="tag.label"
              class="tooltip badge rounded-md text-white font-mono"
              :style="`color: ${tag.color}`"
              :data-tip="tag.label"
            >
              {{ tag.label }}
            </div>
          </div>
        </div>

        <div v-if="pypiData" class="flex gap-2">
          <div class="bg-base-content/10 w-px"></div>

          <div class="flex flex-col">
            <div class="flex items-center gap-1 text-sm">
              <svg
                class="h-4 w-4"
                role="img"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 448 512"
              >
                <path
                  fill="currentColor"
                  d="M439.8 200.5c-7.7-30.9-22.3-54.2-53.4-54.2h-40.1v47.4c0 36.8-31.2 67.8-66.8 67.8H172.7c-29.2 0-53.4 25-53.4 54.3v101.8c0 29 25.2 46 53.4 54.3 33.8 9.9 66.3 11.7 106.8 0 26.9-7.8 53.4-23.5 53.4-54.3v-40.7H226.2v-13.6h160.2c31.1 0 42.6-21.7 53.4-54.2 11.2-33.5 10.7-65.7 0-108.6zM286.2 404c11.1 0 20.1 9.1 20.1 20.3 0 11.3-9 20.4-20.1 20.4-11 0-20.1-9.2-20.1-20.4.1-11.3 9.1-20.3 20.1-20.3zM167.8 248.1h106.8c29.7 0 53.4-24.5 53.4-54.3V91.9c0-29-24.4-50.7-53.4-55.6-35.8-5.9-74.7-5.6-106.8.1-45.2 8-53.4 24.7-53.4 55.6v40.7h106.9v13.6h-147c-31.1 0-58.3 18.7-66.8 54.2-9.8 40.7-10.2 66.1 0 108.6 7.6 31.6 25.7 54.2 56.8 54.2H101v-48.8c0-35.3 30.5-66.4 66.8-66.4zm-6.7-142.6c-11.1 0-20.1-9.1-20.1-20.3.1-11.3 9-20.4 20.1-20.4 11 0 20.1 9.2 20.1 20.4s-9 20.3-20.1 20.3z"
                ></path>
              </svg>
              {{ pypiData?.info.requires_python }}
            </div>

            <div class="flex items-center gap-1 text-sm">
              <span class="material-symbols-outlined text-base"> file_save </span>
              {{ (pypiData?.releases[Object.keys(pypiData.releases).pop()!][1].size ?? 0) / 1000 }}
              K
            </div>

            <div class="flex items-center gap-1 text-sm">
              <span class="material-symbols-outlined text-base"> license </span>
              {{ pypiData?.info.license }}
            </div>

            <div class="flex items-center gap-1 text-sm">
              <span class="material-symbols-outlined text-base"> sell </span>
              {{ pypiData?.info.version }}
            </div>

            <div class="flex items-center gap-1 text-sm">
              <span class="material-symbols-outlined text-base"> fingerprint </span>
              <a
                :href="pypiData?.info.home_page"
                target="_blank"
                class="link link-hover hover:link-primary"
                >{{ props.data.module_name }}</a
              >
            </div>

            <div class="flex items-center gap-1 text-sm">
              <span class="material-symbols-outlined text-base"> deployed_code </span>
              <a
                :href="pypiData?.info.package_url"
                target="_blank"
                class="link link-hover hover:link-primary"
                >{{ pypiData?.info.name }}</a
              >
            </div>
          </div>
        </div>
      </div>
    </div>

    <form method="dialog" class="modal-backdrop">
      <button>close</button>
    </form>
  </dialog>

  <div
    class="h-full min-h-48 p-4 rounded-lg bg-base-200 hover:shadow-lg transition-all flex flex-col justify-between gap-2"
  >
    <div class="flex flex-col gap-0.5">
      <div class="flex gap-2">
        <div class="shrink-0 font-medium text-lg opacity-80">{{ props.data.name }}</div>

        <div class="w-full flex items-center gap-1">
          <div
            role="button"
            v-if="props.data.is_official"
            class="tooltip flex font-normal"
            data-tip="官方验证"
            @click="store.updateTag({ label: SearchTag.label.OFFICIAL })"
          >
            <span class="material-symbols-outlined text-green-600"> verified </span>
          </div>

          <div v-if="'valid' in props.data">
            <div
              role="button"
              v-if="isTestPassed(props.data)"
              class="tooltip flex font-normal"
              data-tip="测试通过"
              @click="store.updateTag({ label: SearchTag.label.VALID })"
            >
              <span class="material-symbols-outlined text-green-600"> check_circle </span>
            </div>
            <div v-else>
              <div class="tooltip flex font-normal" data-tip="测试未通过">
                <span class="material-symbols-outlined text-red-600"> cancel </span>
              </div>
            </div>
          </div>

          <div class="w-full"></div>

          <span
            role="button"
            class="material-symbols-outlined opacity-50 hover:opacity-100 transition-all"
            @click="open()"
          >
            fullscreen
          </span>
        </div>
      </div>

      <div
        role="button"
        class="text-sm opacity-70 hover:opacity-100 transition-all"
        @click="store.updateTag({ label: SearchTag.label.AUTHOR, text: props.data.author })"
      >
        @{{ props.data.author }}
      </div>

      <div class="text-sm opacity-70 flex">{{ props.data.desc }}</div>
    </div>

    <div class="flex flex-wrap items-center gap-2">
      <div
        v-for="tag in props.data.tags"
        :key="tag.label"
        role="button"
        class="tooltip badge rounded-md text-white font-mono"
        :style="`color: ${tag.color}`"
        :data-tip="tag.label"
        @click="store.updateTag({ label: SearchTag.label.TAG, text: tag.label })"
      >
        {{ tag.label }}
      </div>
    </div>

    <div class="flex flex-col gap-2">
      <div class="bg-base-content/10 h-[2px]"></div>

      <div class="flex items-center gap-2">
        <div
          v-if="(props.data as nb_cli_plugin_webui__app__schemas__Plugin).version"
          class="flex items-center gap-1 text-sm"
        >
          <span class="material-symbols-outlined text-base"> sell </span>
          v{{ (props.data as nb_cli_plugin_webui__app__schemas__Plugin).version }}
        </div>

        <div
          v-if="(props.data as nb_cli_plugin_webui__app__schemas__Plugin).time"
          class="flex items-center gap-1 text-sm"
        >
          <span class="material-symbols-outlined text-base"> update </span>
          <span class="shrink-0">{{ getUpdateTime }}</span>
        </div>

        <div class="w-full"></div>

        <!-- TODO: 设置跳转页面支持 -->
        <button v-if="props.data.is_download" class="btn btn-sm btn-outline">设置</button>
        <button v-else class="btn btn-sm btn-ghost" @click="installModule(props.data)">安装</button>
      </div>
    </div>
  </div>
</template>
