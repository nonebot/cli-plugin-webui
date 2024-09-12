import { createApp, type App as VueAPP } from 'vue'
import { createPinia } from 'pinia'
import router from '@/router'
import { AuthService, OpenAPI } from './api'
import { useNoneBotStore, useToastStore } from '@/stores'
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

  const toast = useToastStore()

  if (!token) {
    router.push('/login')
    return
  }

  await AuthService.verifyTokenV1AuthVerifyPost({
    jwt_token: token
  })
    .then((resp) => {
      const expire = Number(resp.detail)
      const data = Date.now() / 1000
      const diff = expire - data
      toast.add(
        'info',
        `Token 有效还剩: ${Math.floor((diff % 86400) / 3600)}h${Math.floor(
          (diff % 3600) / 60
        )}m${Math.floor(diff % 60)}s`,
        '',
        10000
      )
    })
    .catch(() => {
      localStorage.clear()
      router.push('/login')
      toast.add('warning', 'Token 已失效, 请重新登录', '', 5000)
      return
    })

  const store = useNoneBotStore()
  await store.loadBots()
}
