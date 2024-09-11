import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useCustomStore = defineStore('customStore', () => {
  let data: string | null

  const isDebug = ref(false)

  data = localStorage.getItem('isDebug')
  if (data) {
    isDebug.value = data === '1'
  }

  const toggleDebug = () => {
    isDebug.value = !isDebug.value
    localStorage.setItem('isDebug', isDebug.value ? '1' : '0')
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

  const currentTheme = ref('light')

  data = localStorage.getItem('theme')
  if (data) {
    currentTheme.value = data
    if (!isThemeFollowSystem.value) {
      document.documentElement.setAttribute('data-theme', currentTheme.value)
    }
  }

  const toggleTheme = (theme: 'light' | 'dark') => {
    currentTheme.value = theme
    localStorage.setItem('theme', theme)
    document.documentElement.setAttribute('data-theme', theme)
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

  return {
    isDebug,
    toggleDebug,
    isThemeFollowSystem,
    toggleThemeFollowSystem,
    currentTheme,
    toggleTheme,
    isInstantSearch,
    toggleInstantSearch
  }
})