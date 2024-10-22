<script setup lang="ts" generic="T extends Driver | Adapter">
import { type Driver, type Adapter, type ModuleType } from '@/client/api'
import { ref, watch, type Ref } from 'vue'
import { limitContentShow } from '@/client/utils'
import { useCreateBotStore } from '.'

const props = defineProps<{ data: T[]; dataType: ModuleType }>()

const store = useCreateBotStore()

const currentPage = ref(0),
  maxPage = ref(0),
  rawData = ref<T[]>([]) as Ref<T[]>,
  showData = ref<T[]>([]) as Ref<T[]>

watch(
  () => props.data,
  (value) => {
    rawData.value = value
    maxPage.value = Math.ceil(rawData.value.length / 12) - 1
    updateData(currentPage.value)
  }
)

const updateData = (page: number) => {
  showData.value = rawData.value.slice(page * 12, (page + 1) * 12)
}

const itemIsExisted = (data: T): number => {
  if (props.dataType === 'driver') {
    return store.drivers.findIndex((item) => item.name === data.name)
  } else {
    return store.adapters.findIndex((item) => item.name === data.name)
  }
}

const updateItem = (data: T) => {
  const index = itemIsExisted(data)
  if (index === -1) {
    if (props.dataType === 'driver') {
      store.drivers.push(data as Driver)
    } else {
      store.adapters.push(data as Adapter)
    }
  } else {
    if (props.dataType === 'driver') {
      store.drivers.splice(index, 1)
    } else {
      store.adapters.splice(index, 1)
    }
  }
}
</script>

<template>
  <div class="flex flex-col gap-4">
    <div class="bg-base-200 rounded-lg p-4 flex gap-4">
      <div class="flex flex-col gap-4">
        <div class="h-full"></div>
        <button
          :class="{ 'btn btn-sm btn-square btn-ghost': true, 'btn-disabled': currentPage <= 0 }"
          @click="currentPage--, updateData(currentPage)"
        >
          <span class="material-symbols-outlined"> expand_less </span>
        </button>
        <div class="text-center">{{ currentPage + 1 }}</div>
        <button
          :class="{
            'btn btn-sm btn-square btn-ghost': true,
            'btn-disabled': currentPage >= maxPage
          }"
          @click="currentPage++, updateData(currentPage)"
        >
          <span class="material-symbols-outlined"> expand_more </span>
        </button>
        <div class="h-full"></div>
      </div>

      <div
        v-if="props.data.length"
        class="overflow-auto max-h-96 w-full grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4"
      >
        <div
          v-for="item in showData"
          :key="item.name"
          class="bg-base-100 rounded-lg p-4 flex justify-between"
        >
          <div>
            <div class="text-semibold flex items-center gap-1">
              <a
                target="_blank"
                :href="`
                ${item.homepage!.startsWith('/docs') ? 'https://nonebot.dev' : ''}
                ${item.homepage}
                `"
              >
                {{ limitContentShow(item.name!, 10) }}
              </a>
              <div v-if="item.is_official" class="tooltip flex items-center" data-tip="官方认证">
                <span class="material-symbols-outlined text-green-600"> check_circle </span>
              </div>
            </div>
            <div class="text-sm">{{ limitContentShow(item.desc!, 20) }}</div>
          </div>
          <div class="flex items-center justify-center">
            <input
              type="checkbox"
              class="checkbox"
              :checked="itemIsExisted(item) !== -1"
              @click="updateItem(item)"
            />
          </div>
        </div>
      </div>
      <div v-else class="w-full flex items-center justify-center">暂无内容</div>
    </div>

    <div
      v-if="(store as any)[`${props.dataType.toLowerCase()}s`].length"
      class="bg-base-200 rounded-lg p-4 flex gap-4"
    >
      <div class="shrink-0">当前选择:</div>
      <div class="flex items-center flex-wrap gap-2">
        <div
          v-for="item in (store as any)[`${props.dataType.toLowerCase()}s`]"
          :key="item.name"
          role="button"
          class="badge badge-lg !bg-base-100"
          @click="updateItem(item)"
        >
          {{ item.name }}
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.material-symbols-outlined {
  font-variation-settings:
    'FILL' 1,
    'wght' 400,
    'GRAD' 0,
    'opsz' 24;
}
</style>
