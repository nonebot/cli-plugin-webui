import { ref } from 'vue'
import { defineStore } from 'pinia'
import type { NoneBotProjectMeta } from '@/client/api'

export const useNoneBotStore = defineStore('nonebotStore', () => {
  const bots = ref<NoneBotProjectMeta[]>([])

  return {
    bots
  }
})
