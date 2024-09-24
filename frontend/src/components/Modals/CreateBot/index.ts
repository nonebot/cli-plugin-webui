import type { Adapter, Driver } from '@/client/api'
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useCreateBotStore = defineStore('createBotStore', () => {
  const step = ref(0)
  const warningMessage = ref('')
  const template = ref('')
  const useSrc = ref(false)
  const projectName = ref('')
  const projectPath = ref('')
  const pythonMirror = ref('')
  const drivers = ref<Driver[]>([])
  const adapters = ref<Adapter[]>([])
  const isInstalling = ref(false)
  const createBotSuccess = ref(false)

  const reset = () => {
    step.value = 0
    warningMessage.value = ''
    template.value = ''
    useSrc.value = false
    projectName.value = ''
    projectPath.value = ''
    pythonMirror.value = ''
    drivers.value = []
    adapters.value = []
    isInstalling.value = false
    createBotSuccess.value = false
  }

  return {
    step,
    warningMessage,
    template,
    useSrc,
    projectName,
    projectPath,
    pythonMirror,
    drivers,
    adapters,
    isInstalling,
    createBotSuccess,
    reset
  }
})
