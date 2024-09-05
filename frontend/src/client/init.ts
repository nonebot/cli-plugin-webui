import { createApp, type App as VueAPP } from 'vue'
import { createPinia } from 'pinia'
import router from '@/router'
import { AuthService, OpenAPI } from './api'
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

  const token = localStorage.getItem('token') || ''
  const base = localStorage.getItem('debugUrl') || ''

  OpenAPI.TOKEN = async () => token
  OpenAPI.BASE = base

  await AuthService.verifyTokenV1AuthVerifyPost({
    jwt_token: token
  })
    .then((resp) => {
      console.log(resp.detail)
    })
    .catch(() => {
      localStorage.clear()
      router.push('/login')
    })

  const store = useNoneBotStore()
  await store.loadBots()
}
