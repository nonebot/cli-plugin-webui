import {
  type ConfigType,
  type ModuleType,
  type ModuleConfigFather,
  ProjectService,
  ConfigTypeSchema,
  ModuleTypeSchema
} from '@/client/api'
import { useNoneBotStore, useToastStore } from '@/stores'
import { defineStore } from 'pinia'
import { ref } from 'vue'

const store = useNoneBotStore()
const toast = useToastStore()

export type ModuleConfigType = ModuleType | ConfigType | 'all'

export const updateConfig = async (
  moduleType: ModuleType | ConfigType,
  confType: string,
  k: string,
  v: any
) => {
  if (!store.selectedBot) {
    toast.add('warning', '未选择实例', '', 5000)
    return
  }

  const { data, error } = await ProjectService.updateProjectConfigV1ProjectConfigUpdatePost({
    query: {
      module_type: moduleType,
      project_id: store.selectedBot.project_id
    },
    body: {
      env: store.selectedBot.use_env!,
      conf_type: confType,
      k: k,
      v: v
    }
  })

  if (error) {
    toast.add('error', `更新失败, 原因：${error.detail?.toString()}`, '', 5000)
  }

  if (data) {
    toast.add('success', '更新成功', '', 5000)
  }

  return { data, error }
}

export const useSettingsStore = defineStore('settingsStore', () => {
  const viewModule = ref<ModuleConfigType>('all'),
    settingsData = ref<ModuleConfigFather[]>([]),
    viewData = ref<ModuleConfigFather[]>([]),
    isRequesting = ref(false)

  const getTomlConf = async (projectID: string) => {
    isRequesting.value = true
    const { data, error } = await ProjectService.getProjectMetaConfigV1ProjectConfigMetaDetailGet({
      query: {
        project_id: projectID
      }
    })

    if (error) {
      toast.add('error', `获取实例 toml 配置失败, 原因：${error.detail?.toString()}`, '', 5000)
    }

    if (data) {
      settingsData.value = settingsData.value.concat(data.detail)
    }

    isRequesting.value = false
  }

  const getNoneBotConf = async (projectID: string) => {
    isRequesting.value = true
    const { data, error } =
      await ProjectService.getProjectNonebotConfigV1ProjectConfigNonebotDetailGet({
        query: {
          project_id: projectID
        }
      })

    if (error) {
      toast.add('error', `获取实例 NoneBot 配置失败, 原因：${error.detail?.toString()}`, '', 5000)
    }

    if (data) {
      settingsData.value = settingsData.value.concat(data.detail)
    }

    isRequesting.value = false
  }

  const getNoneBotPluginConf = async (projectID: string) => {
    isRequesting.value = true
    const { data, error } =
      await ProjectService.getProjectNonebotPluginConfigV1ProjectConfigNonebotPluginDetailGet({
        query: {
          project_id: projectID
        }
      })

    if (error) {
      toast.add('error', `获取实例配置失败, 原因：${error.detail?.toString()}`, '', 5000)
    }

    if (data) {
      settingsData.value = settingsData.value.concat(data.detail)
    }

    isRequesting.value = false
  }

  const updateViewData = (searchText?: string) => {
    viewData.value = settingsData.value.filter((item) => {
      if (!searchText) return true
      return (
        item.title.includes(searchText) ||
        item.name.includes(searchText) ||
        item.description.includes(searchText)
      )
    })

    const filter = [...ConfigTypeSchema.enum, ...ModuleTypeSchema.enum]
    if (viewModule.value !== 'all' && Object.values(filter).includes(viewModule.value)) {
      viewData.value = viewData.value.filter((item) => item.module_type === viewModule.value)
    }
  }

  const init = async () => {
    if (!store.selectedBot) {
      toast.add('warning', '未选择实例', '', 5000)
      return
    }

    settingsData.value = []

    const projectID = store.selectedBot.project_id

    await getTomlConf(projectID)
    await getNoneBotConf(projectID)
    await getNoneBotPluginConf(projectID)

    updateViewData()
  }

  const setViewModule = (module: ModuleConfigType) => {
    viewModule.value = module
    updateViewData()
  }

  return {
    viewModule,
    settingsData,
    viewData,
    isRequesting,
    init,
    updateViewData,
    setViewModule
  }
})
