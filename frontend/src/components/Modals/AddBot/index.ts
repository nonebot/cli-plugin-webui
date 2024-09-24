import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAddBotStore = defineStore('addBotStore', () => {
  const step = ref(0)
  const warningMessage = ref('')
  const projectName = ref('')
  const projectPath = ref('')
  const pythonMirror = ref('')
  const adapters = ref<Record<string, string>[]>([])
  const plugins = ref<string[]>([])
  const pluginDirs = ref<string[]>([])
  const isInstalling = ref(false)
  const addBotSuccess = ref(false)
  const searchBotSuccess = ref(false)

  const reset = () => {
    step.value = 0
    warningMessage.value = ''
    projectName.value = ''
    projectPath.value = ''
    pythonMirror.value = ''
    adapters.value = []
    plugins.value = []
    pluginDirs.value = []
    isInstalling.value = false
    addBotSuccess.value = false
    searchBotSuccess.value = false
  }

  return {
    step,
    warningMessage,
    projectName,
    projectPath,
    pythonMirror,
    adapters,
    plugins,
    pluginDirs,
    isInstalling,
    addBotSuccess,
    searchBotSuccess,
    reset
  }
})
