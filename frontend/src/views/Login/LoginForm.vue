<script setup lang="ts">
import { ref } from 'vue'
import { OpenAPI, AuthService } from '@/client/api'
import router from '@/router'

const token = ref(''),
  isDebug = ref(false),
  host = ref(''),
  port = ref('')

const date = new Date()

const login = () => {
  if (isDebug.value) {
    OpenAPI.BASE = `//${host.value}:${port.value}/api`
    localStorage.setItem('isDebug', '1')
  }

  AuthService.authTokenV1AuthLoginPost({ token: token.value, mark: date.toISOString() })
    .then((res) => {
      localStorage.setItem('token', res.detail)
      router.push('/')
    })
    .catch((err) => {
      console.error(err)
    })
}
</script>

<template>
  <div class="shrink-0 w-full flex flex-col gap-4">
    <form class="flex justify-center gap-4 flex-col lg:flex-row" @submit.prevent="login">
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
        <button class="btn btn-primary text-white">
          开始使用 <span class="material-symbols-outlined"> chevron_right </span>
        </button>
      </div>
    </form>

    <form v-if="isDebug" class="flex gap-4 flex-col">
      <div class="form-control">
        <input
          v-model="host"
          type="text"
          placeholder="host"
          class="input input-ghost bg-base-200"
          required
        />
      </div>

      <div class="form-control">
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
