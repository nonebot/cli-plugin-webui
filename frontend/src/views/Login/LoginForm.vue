<script setup lang="ts">
import { ref } from 'vue'
import { OpenAPI, AuthService } from '@/client/api'
import router from '@/router'
import { useNoneBotStore, useToastStore } from '@/stores'

const store = useToastStore()
const nonebotStore = useNoneBotStore()

const token = ref(''),
  isDebug = ref(false),
  host = ref(''),
  port = ref('')

const date = new Date()

const login = () => {
  if (isDebug.value) {
    OpenAPI.BASE = `//${host.value}:${port.value}/api`
    localStorage.setItem('isDebug', '1')
    localStorage.setItem('debugUrl', OpenAPI.BASE)
  }

  AuthService.authTokenV1AuthLoginPost({ token: token.value, mark: date.toISOString() })
    .then(async (res) => {
      localStorage.setItem('token', res.detail)
      OpenAPI.TOKEN = async () => res.detail
      router.push('/')
      await nonebotStore.loadBots()
      store.add('success', '登录成功', '', 3000)
    })
    .catch((err) => {
      if (err.body) {
        store.add('error', err.body.detail)
        return
      }
      store.add('error', '无法连接到服务器', '', 5000)
    })
}
</script>

<template>
  <div class="shrink-0 w-full">
    <form class="flex justify-center flex-col gap-4 lg:gap-0" @submit.prevent="login">
      <div class="flex justify-center gap-0 lg:gap-4 flex-col lg:flex-row">
        <label class="form-control">
          <input
            v-model="token"
            type="password"
            placeholder="请键入登陆凭证"
            class="input input-ghost bg-base-200"
            required
          />
          <div class="label">
            <span class="label-text">开发模式</span>
            <input
              type="checkbox"
              class="checkbox checkbox-xs"
              :checked="isDebug"
              @click="isDebug = !isDebug"
            />
          </div>
        </label>

        <div class="form-control">
          <button class="btn btn-primary text-base-100">
            开始使用 <span class="material-symbols-outlined"> chevron_right </span>
          </button>
        </div>
      </div>

      <div v-if="isDebug" class="form-control flex gap-4 flex-col">
        <input
          v-model="host"
          type="text"
          placeholder="host"
          class="input input-ghost bg-base-200"
          required
        />

        <input
          v-model="port"
          type="text"
          placeholder="port"
          class="input input-ghost bg-base-200"
          required
        />
      </div>
    </form>
  </div>
</template>
