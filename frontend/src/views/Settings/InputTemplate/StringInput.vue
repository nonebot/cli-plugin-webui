<script setup lang="ts">
import type { ModuleConfigChild, ModuleConfigFather } from '@/client/api'
import { updateConfig } from '../client'
import { ref } from 'vue'
import { useNoneBotStore } from '@/stores'

const store = useNoneBotStore()

const props = defineProps<{
  moduleType: ModuleConfigFather.module_type
  data: ModuleConfigChild
}>()

const inputValue = ref(props.data.configured),
  inEditing = ref(false),
  inVisible = ref(!props.data.is_secret)

const update = async () => {
  if (!inputValue.value) {
    return
  }
  const data = props.data
  await updateConfig(
    props.moduleType,
    store.enabledEnv,
    data.conf_type,
    data.name,
    inputValue.value
  )
}
</script>

<template>
  <div class="flex items-center gap-2">
    <input
      :type="data.is_secret && inVisible ? 'password' : 'text'"
      v-model="inputValue"
      v-if="data.default.length <= 15 && data.conf_type !== 'object' && !data.is_secret"
      class="input input-sm !bg-base-100"
      :disabled="!inEditing"
      @blur="update()"
    />
    <textarea
      v-else
      v-model="inputValue"
      class="textarea textarea-xs w-full max-w-xs !bg-base-100"
      :disabled="!inEditing"
      @blur="update()"
    />

    <div class="join">
      <button
        v-if="data.is_secret"
        class="btn btn-xs btn-ghost join-item tooltip font-normal"
        data-tip="查看"
        @click="inVisible = !inVisible"
      >
        <span class="material-symbols-outlined text-base"> visibility </span>
      </button>

      <button class="btn btn-xs btn-ghost join-item tooltip font-normal" data-tip="恢复默认">
        <span class="material-symbols-outlined text-base"> refresh </span>
      </button>

      <button
        class="btn btn-xs btn-ghost join-item tooltip font-normal"
        data-tip="编辑"
        @click="inEditing = !inEditing"
      >
        <span :class="{ 'material-symbols-outlined text-base': true, 'text-primary': inEditing }">
          edit
        </span>
      </button>
    </div>
  </div>
</template>
