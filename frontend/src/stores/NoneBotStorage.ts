import { ref } from 'vue'
import { defineStore } from 'pinia'
import { ProjectService } from '@/client/api'
import type { NoneBotProjectMeta, Driver, Adapter } from '@/client/api'

interface MetaWrapper extends NoneBotProjectMeta {
  projectID: string
}

export const useNoneBotStore = defineStore('nonebotStore', () => {
  const bots = ref<{ [key: string]: NoneBotProjectMeta }>({})
  const selectedBot = ref<MetaWrapper>()

  const selectedBotFromLocalStorage = localStorage.getItem('selectedBot')
  if (selectedBotFromLocalStorage) {
    selectedBot.value = JSON.parse(selectedBotFromLocalStorage)
  }

  const getExtendedBotsList = (): MetaWrapper[] => {
    return Object.keys(bots.value).map((projectID) => ({
      projectID,
      ...bots.value[projectID]
    }))
  }

  const selectBot = (bot: MetaWrapper) => {
    selectedBot.value = bot
    localStorage.setItem('selectedBot', JSON.stringify(bot))
  }

  const loadBots = async () => {
    await ProjectService.listProjectV1ProjectListGet().then((res) => {
      bots.value = res.detail
    })
  }

  const template = ref(''),
    useSrc = ref(false),
    name = ref(''),
    projectPath = ref(''),
    pythonMirror = ref(''),
    drivers = ref<Driver[]>([]),
    adapters = ref<Adapter[]>([]),
    isInstalling = ref(false),
    addNoneBotSuccess = ref(false)

  const reset = () => {
    template.value = ''
    name.value = ''
    projectPath.value = ''
    pythonMirror.value = ''
    drivers.value = []
    adapters.value = []
    isInstalling.value = false
    addNoneBotSuccess.value = false
  }

  return {
    bots,
    selectedBot,
    template,
    useSrc,
    name,
    projectPath,
    pythonMirror,
    drivers,
    adapters,
    isInstalling,
    addNoneBotSuccess,
    getExtendedBotsList,
    selectBot,
    loadBots,
    reset
  }
})
