import { ref } from 'vue'
import { defineStore } from 'pinia'
import type { NoneBotProjectMeta, Driver, Adapter } from '@/client/api'

export const useNoneBotStore = defineStore('nonebotStore', () => {
  const bots = ref<NoneBotProjectMeta[]>([])

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
    template,
    useSrc,
    name,
    projectPath,
    pythonMirror,
    drivers,
    adapters,
    isInstalling,
    addNoneBotSuccess,
    reset
  }
})
