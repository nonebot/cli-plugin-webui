import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useStatusStore } from './StatusStore'
import { v4 as uuidv4 } from 'uuid'

const ID_OF_DEBUG_STATUS = uuidv4()

export const useCustomStore = defineStore('customStore', () => {
  let data: string | null

  const statusStore = useStatusStore()

  const isDebug = ref(false)

  data = localStorage.getItem('isDebug')
  if (data) {
    isDebug.value = data === '1'
    if (isDebug.value) statusStore.update(ID_OF_DEBUG_STATUS, 'badge-warning', '开发模式')
  }

  const toggleDebug = () => {
    isDebug.value = !isDebug.value
    localStorage.setItem('isDebug', isDebug.value ? '1' : '0')

    if (isDebug.value) {
      statusStore.update(ID_OF_DEBUG_STATUS, 'badge-warning', '开发模式')
    } else {
      statusStore.deleteStatus(ID_OF_DEBUG_STATUS)
    }
  }

  const toggleTheme = (theme: 'light' | 'dark') => {
    currentTheme.value = theme
    localStorage.setItem('theme', theme)
    document.documentElement.setAttribute('data-theme', theme)
  }

  const isThemeFollowSystem = ref(true)

  data = localStorage.getItem('isThemeFollowSystem')
  if (data) {
    isThemeFollowSystem.value = data === '1'
  }

  const toggleThemeFollowSystem = () => {
    isThemeFollowSystem.value = !isThemeFollowSystem.value
    localStorage.setItem('isThemeFollowSystem', isThemeFollowSystem.value ? '1' : '0')
  }

  const currentTheme = ref<string>('light')

  data = localStorage.getItem('theme') ?? 'light'
  const sysTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'

  if (isThemeFollowSystem.value) {
    toggleTheme(sysTheme)
  } else {
    if (data) {
      toggleTheme(data as 'light' | 'dark')
    } else {
      toggleTheme(sysTheme)
    }
  }

  const isInstantSearch = ref(false)

  data = localStorage.getItem('instantSearch')
  if (data) {
    isInstantSearch.value = data === '1'
  }

  const toggleInstantSearch = () => {
    isInstantSearch.value = !isInstantSearch.value
    localStorage.setItem('instantSearch', isInstantSearch.value ? '1' : '0')
  }

  const menuMinify = ref(false)

  const toggleMenuMinify = () => {
    menuMinify.value = !menuMinify.value
  }

  const menuShow = ref(false)

  const toggleMenuShow = () => {
    menuShow.value = !menuShow.value
  }

  return {
    isDebug,
    toggleDebug,
    isThemeFollowSystem,
    toggleThemeFollowSystem,
    currentTheme,
    toggleTheme,
    isInstantSearch,
    toggleInstantSearch,
    menuMinify,
    toggleMenuMinify,
    menuShow,
    toggleMenuShow
  }
})
