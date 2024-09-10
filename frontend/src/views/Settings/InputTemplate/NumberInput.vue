<script setup lang="ts">
import type { ConfigType, ModuleConfigChild, ModuleType } from '@/client/api'
import { ref, watch } from 'vue'
import { updateConfig } from '../client'
import { useNoneBotStore } from '@/stores'

const store = useNoneBotStore()

const props = defineProps<{
  moduleType: ModuleType | ConfigType
  data: ModuleConfigChild
}>()

const inputValue = ref(props.data.configured),
  inEditing = ref(false),
  isNumber = ref(true)

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

watch(inputValue, (value) => {
  isNumber.value = !isNaN(Number(value.trim())) && value.trim().length !== 0
})
</script>

<template>
  <div class="flex items-center gap-2">
    <label class="form-control">
      <input
        ref="element"
        v-model="inputValue"
        :class="{ 'input input-sm !bg-base-100': true, 'input-error': !isNumber }"
        :disabled="!inEditing"
        @blur="update()"
      />
      <div v-if="!isNumber" class="label">
        <span class="label-text-alt text-error">请键入数字</span>
      </div>
    </label>

    <div class="join">
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
