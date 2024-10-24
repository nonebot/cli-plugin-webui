<script setup lang="ts">
import type { ConfigType, ModuleConfigChild, ModuleType } from '@/client/api'
import { ref } from 'vue'
import { updateConfig } from '../client'
import { useNoneBotStore } from '@/stores'

const store = useNoneBotStore()

const props = defineProps<{
  moduleType: ModuleType | ConfigType
  data: ModuleConfigChild
}>()
const data = props.data as Omit<ModuleConfigChild, 'configured' | 'enum'> & {
  configured: string[]
  enum: any[]
}

const isAddItem = ref(false),
  inputValue = ref<string>()

const findItem = (fItem: string) => {
  return data.configured.findIndex((item: string) => item === fItem)
}

const addItem = async () => {
  if (!inputValue.value) {
    return
  }

  if (!store.selectedBot) {
    return
  }

  data.configured.push(inputValue.value)

  const result = await updateConfig(props.moduleType, data.conf_type, data.name, data.configured)

  if (result?.error) {
    const index = findItem(inputValue.value!)
    if (index === -1) return
    data.configured.splice(index, 1)
  }

  if (result?.data) {
    inputValue.value = ''
    isAddItem.value = false
  }
}

const removeItem = async (rItem: string) => {
  if (!store.selectedBot) {
    return
  }

  const index = findItem(rItem)
  if (index === -1) return
  data.configured.splice(index, 1)

  await updateConfig(props.moduleType, data.conf_type, data.name, data.configured).catch(() => {
    data.configured.push(rItem)
  })
}

const cancel = () => {
  isAddItem.value = false
  inputValue.value = ''
}
</script>

<template>
  <div class="flex flex-col gap-2">
    <div class="w-full">
      <table class="table table-xs">
        <thead>
          <tr class="border-b border-b-base-content/10">
            <th>值</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="i in data.configured" :key="i" class="transition-colors hover:bg-base-300">
            <td>{{ i }}</td>
            <td>
              <button class="btn btn-xs btn-square btn-ghost" @click="removeItem(i)">
                <span class="material-symbols-outlined text-base"> close </span>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div>
      <button v-if="!isAddItem" class="btn btn-xs btn-ghost" @click="isAddItem = true">
        + 添加
      </button>
      <div v-else class="flex items-center gap-2">
        <input
          v-if="!data.items?.enum"
          v-model="inputValue"
          class="input input-xs"
          placeholder="请键入"
        />
        <select v-else v-model="inputValue" class="select select-sm">
          <option disabled selected>请选择</option>
          <option v-for="i in data.items.enum" :key="String(i)">{{ i }}</option>
        </select>

        <button class="btn btn-xs btn-ghost" @click="addItem()">确认</button>
        <button class="btn btn-xs btn-ghost" @click="cancel()">取消</button>
      </div>
    </div>
  </div>
</template>
