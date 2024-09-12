import { ConfigType, ModuleType, ProjectService, type ModuleConfigFather } from '@/client/api'
import { useNoneBotStore, useToastStore } from '@/stores'
import { defineStore } from 'pinia'
import { ref } from 'vue'

const store = useNoneBotStore()
const toast = useToastStore()

export type ModuleConfigType = ModuleType | ConfigType | 'all'

export const updateConfig = async (
  moduleType: ModuleType | ConfigType,
  env: string,
  confType: string,
  k: string,
  v: any
) => {
  if (!store.selectedBot) {
    toast.add('warning', '未选择实例', '', 5000)
    return
  }

  await ProjectService.updateProjectConfigV1ProjectConfigUpdatePost(
    moduleType,
    store.selectedBot.project_id,
    {
      env: env,
      conf_type: confType,
      k: k,
      v: v
    }
  )
    .then(() => {
      toast.add('success', '更新成功', '', 5000)
    })
    .catch((err) => {
      let detail = ''
      if (err.body) {
        detail = err.body.detail
      } else {
        detail = err
      }
      toast.add('error', `更新失败, 原因：${detail}`, '', 5000)
    })
}

export const useSettingsStore = defineStore('settingsStore', () => {
  const viewModule = ref<ModuleConfigType>('all'),
    settingsData = ref<ModuleConfigFather[]>([]),
    viewData = ref<ModuleConfigFather[]>([]),
    isRequesting = ref(false)

  const getTomlConf = async (projectID: string) => {
    isRequesting.value = true
    await ProjectService.getProjectMetaConfigV1ProjectConfigMetaDetailGet(projectID)
      .then((res) => {
        settingsData.value = settingsData.value.concat(res.detail)
      })
      .catch((err) => {
        let detail = ''
        if (err.body) {
          detail = err.body.detail
        } else {
          detail = err
        }
        toast.add('error', `获取实例 toml 配置失败, 原因：${detail}`, '', 5000)
      })
      .finally(() => {
        isRequesting.value = false
      })
  }

  const getNoneBotConf = async (projectID: string) => {
    isRequesting.value = true
    await ProjectService.getProjectNonebotConfigV1ProjectConfigNonebotDetailGet(projectID)
      .then((res) => {
        settingsData.value = settingsData.value.concat(res.detail)
      })
      .catch((err) => {
        let detail = ''
        if (err.body) {
          detail = err.body.detail
        } else {
          detail = err
        }
        toast.add('error', `获取实例 NoneBot 配置失败, 原因：${detail}`, '', 5000)
      })
      .finally(() => {
        isRequesting.value = false
      })
  }

  const getNoneBotPluginConf = async (projectID: string) => {
    isRequesting.value = true
    await ProjectService.getProjectNonebotPluginConfigV1ProjectConfigNonebotPluginDetailGet(
      projectID
    )
      .then((res) => {
        settingsData.value = settingsData.value.concat(res.detail)
      })
      .catch((err) => {
        let detail = ''
        if (err.body) {
          detail = err.body.detail
        } else {
          detail = err
        }
        toast.add('error', `获取实例配置失败, 原因：${detail}`, '', 5000)
      })
      .finally(() => {
        isRequesting.value = false
      })
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

    const filter = { ...ConfigType, ...ModuleType }
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
