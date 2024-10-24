<script setup lang="ts">
import { type ConfigType, type ModuleConfigChild, type ModuleType } from '@/client/api'
import { ref, watch } from 'vue'
import { updateConfig } from '../client'

const props = defineProps<{ moduleType: ModuleType | ConfigType; data: ModuleConfigChild }>()

const data = props.data as Omit<ModuleConfigChild, 'configured' | 'default' | 'enum'> & {
  configured: any
  default: any
  enum: any[]
}

const selectedValue = ref(data.configured)
const inEditing = ref(false)

const update = async (v: any) => {
  await updateConfig(props.moduleType, data.conf_type, data.name, v)
}

watch(selectedValue, async () => {
  await update(selectedValue.value)
})
</script>

<template>
  <div class="flex items-center gap-2">
    <select v-model="selectedValue" class="select select-sm" :disabled="!inEditing">
      <option v-for="i in data.enum" :key="i">{{ i }}</option>
    </select>

    <div class="join">
      <button
        v-if="data.default"
        class="btn btn-xs btn-ghost join-item tooltip font-normal"
        data-tip="恢复默认"
      >
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
