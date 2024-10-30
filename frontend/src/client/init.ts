import { createApp, type App as VueAPP } from 'vue'
import { createPinia } from 'pinia'
import router from '@/router'
import { client, AuthService } from './api'
import { useNoneBotStore, useToastStore } from '@/stores'
import App from '@/App.vue'
import './useMonacoWorker'

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

  if (!token) {
    router.push('/login')
    return
  }

  client.setConfig({
    baseUrl: base
  })
  client.interceptors.request.use((request) => {
    request.headers.set('Authorization', `Bearer ${token}`)
    return request
  })

  const toast = useToastStore()

  const { data, error, response } = await AuthService.verifyTokenV1AuthVerifyPost({
    body: {
      jwt_token: token
    }
  })
  if (error && response.status === 403) {
    localStorage.clear()
    router.push('/login')
    toast.add('warning', 'Token 已失效, 请重新登陆', '', 5000)
    return
  }

  if (data) {
    const expire = Number(data.detail)
    const now = Date.now() / 1000
    const diff = expire - now
    toast.add(
      'info',
      `Token 有效还剩: ${Math.floor((diff % 86400) / 3600)}h${Math.floor(
        (diff % 3600) / 60
      )}m${Math.floor(diff % 60)}s`,
      '',
      10000
    )
  }

  const store = useNoneBotStore()
  await store.loadBots()
}
