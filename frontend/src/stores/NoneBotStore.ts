import { ref, watch } from 'vue'
import { defineStore } from 'pinia'
import { ProjectService } from '@/client/api'
import type { NoneBotProjectMeta } from '@/client/api'
import { useToastStore } from './ToastStore'
import { useStatusStore } from './StatusStore'
import { v4 as uuidv4 } from 'uuid'

const ID_OF_ENV_STATUS = uuidv4()
const ID_OF_BOT_STATUS = uuidv4()

export const useNoneBotStore = defineStore('nonebotStore', () => {
  const bots = ref<{ [key: string]: NoneBotProjectMeta }>({})
  const selectedBot = ref<NoneBotProjectMeta>()

  const toast = useToastStore()
  const statusStore = useStatusStore()

  const selectedBotFromLocalStorage = localStorage.getItem('selectedBot')
  if (selectedBotFromLocalStorage) {
    selectedBot.value = JSON.parse(selectedBotFromLocalStorage)
  }

  const getExtendedBotsList = (): NoneBotProjectMeta[] => {
    return Object.keys(bots.value).map((projectID) => ({
      projectID,
      ...bots.value[projectID]
    }))
  }

  const selectBot = (bot: NoneBotProjectMeta) => {
    selectedBot.value = bot
    localStorage.setItem('selectedBot', JSON.stringify(bot))
    toast.add('success', `已选择实例: ${bot.project_name}`, '', 5000)
  }

  const loadBots = async () => {
    const { data } = await ProjectService.listProjectV1ProjectListGet()
    if (data) {
      bots.value = data.detail
      selectedBot.value = selectedBot.value ? bots.value[selectedBot.value.project_id] : undefined
    }
  }

  const updateEnv = async (env: string) => {
    if (!selectedBot.value) {
      return
    }

    const { data, error } = await ProjectService.useProjectEnvV1ProjectConfigEnvUsePost({
      query: {
        env: env,
        project_id: selectedBot.value.project_id
      }
    })

    if (error) {
      toast.add('error', `更新环节失败, 原因: ${error.detail?.toString()}`, '', 5000)
    }

    if (data && selectedBot.value) {
      selectedBot.value.use_env = env
    }
  }

  const data = localStorage.getItem('selectedBot')
  if (data) {
    selectedBot.value = JSON.parse(data) as NoneBotProjectMeta
  }

  watch(
    () => selectedBot.value,
    (bot) => {
      if (bot) {
        statusStore.update(ID_OF_BOT_STATUS, 'badge-ghost', `当前实例: ${bot.project_name}`)
        statusStore.update(ID_OF_ENV_STATUS, 'badge-ghost', `当前环境: ${bot.use_env}`)
      }
    }
  )

  watch(
    () => selectedBot.value?.use_env,
    (env) => {
      statusStore.update(ID_OF_ENV_STATUS, 'badge-ghost', `当前环境: ${env}`)
    }
  )

  return {
    bots,
    selectedBot,
    getExtendedBotsList,
    selectBot,
    loadBots,
    updateEnv
  }
})
