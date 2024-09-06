import { defineStore } from 'pinia'
import { ref } from 'vue'

const MAX_VISIBLE_TOASTS = 5

export type ToastType = 'success' | 'error' | 'info' | 'warning'

export interface ToastItem {
  id: string
  type: ToastType
  message: string
  time: number
  from?: string
  timer?: ReturnType<typeof setTimeout>
}

export const useToastStore = defineStore('toastStore', () => {
  const toasts = ref<ToastItem[]>([])
  const visibleToasts = ref<ToastItem[]>([])

  const add = (type: ToastType, message: string, from?: string, exp?: number) => {
    if (visibleToasts.value.length >= MAX_VISIBLE_TOASTS) {
      const toast = visibleToasts.value.shift()
      if (toast) {
        remove(toast.id)
      }
    }

    const toast: ToastItem = {
      id: crypto.randomUUID(),
      type,
      message,
      time: Date.now()
    }

    if (exp) {
      toast.timer = setTimeout(() => {
        remove(toast.id)
      }, exp)
    }

    visibleToasts.value.push(toast)
    toasts.value.push(toast)
  }

  const remove = (id: string, isVisible: boolean = true) => {
    if (isVisible) {
      const index = visibleToasts.value.findIndex((toast) => toast.id === id)
      if (index !== -1) {
        clearTimeout(visibleToasts.value[index].timer!)
        visibleToasts.value.splice(index, 1)
      }
    } else {
      const index = toasts.value.findIndex((toast) => toast.id === id)
      if (index !== -1) {
        toasts.value.splice(index, 1)
      }
    }
  }

  return {
    toasts,
    visibleToasts,
    add,
    remove
  }
})
