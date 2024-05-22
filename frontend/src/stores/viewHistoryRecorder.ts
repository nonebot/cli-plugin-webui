import { ref } from 'vue'
import { defineStore } from 'pinia'
import type { NavItem } from '@/router/client'
import { defaultRoutes } from '@/router/client'

export const useViewHistoryRecorderStore = defineStore('viewHistoryRecorder', () => {
  const viewHistory = ref<NavItem[]>([])

  const viewHistoryFromLocalStorage = localStorage.getItem('viewHistory')
  if (viewHistoryFromLocalStorage) {
    const storedHistory = JSON.parse(viewHistoryFromLocalStorage)
    viewHistory.value = storedHistory.map((name: string) => {
      const routeItem = defaultRoutes.find((route) => route.name === name)
      return routeItem
    })
  }

  function _record() {
    localStorage.setItem('viewHistory', JSON.stringify(viewHistory.value.map((item) => item.name)))
  }

  function _remove(name: string) {
    const data = viewHistory.value.map((item) => item.name)
    data.filter((item) => item !== name)

    localStorage.setItem('viewHistory', JSON.stringify(data))
  }

  function record(route: NavItem) {
    viewHistory.value.push(route)
    _record()
  }

  function remove(route: NavItem) {
    const index = viewHistory.value.findIndex((item: any) => item.name === route.name)
    if (index !== -1) {
      viewHistory.value.splice(index, 1)
    }
    _remove(route.name)
  }

  return { viewHistory, record, remove }
})
