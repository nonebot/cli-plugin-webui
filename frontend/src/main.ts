import '@/assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from '@/router'
import { OpenAPI } from '@/client/api'

import App from './App.vue'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')

OpenAPI.TOKEN = async () => {
  return localStorage.getItem('token') || ''
}
