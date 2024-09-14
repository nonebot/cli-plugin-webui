import { ref } from 'vue'
import { defineStore } from 'pinia'
import { ProjectService } from '@/client/api'
import type { NoneBotProjectMeta } from '@/client/api'

export const useNoneBotStore = defineStore('nonebotStore', () => {
  const bots = ref<{ [key: string]: NoneBotProjectMeta }>({})
  const selectedBot = ref<NoneBotProjectMeta>()

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
  }

  const loadBots = async () => {
    await ProjectService.listProjectV1ProjectListGet().then((res) => {
      bots.value = res.detail
      selectedBot.value = selectedBot.value ? bots.value[selectedBot.value.project_id] : undefined
    })
  }

  return {
    bots,
    selectedBot,
    getExtendedBotsList,
    selectBot,
    loadBots
  }
})
