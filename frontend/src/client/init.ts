import { createApp, type App as VueAPP } from 'vue'
import { createPinia } from 'pinia'
import router from '@/router'
import { OpenAPI } from './api'
import { useNoneBotStore } from '@/stores'
import App from '@/App.vue'

const installVuePlugins = (app: VueAPP) => {
  app.use(createPinia())
  app.use(router)
}

export const initWebUI = async () => {
  const app = createApp(App)
  installVuePlugins(app)
  app.mount('#app')

  OpenAPI.TOKEN = async () => {
    return localStorage.getItem('token') || ''
  }
  OpenAPI.BASE = localStorage.getItem('debugUrl') || ''

  const store = useNoneBotStore()
  await store.loadBots()
}
