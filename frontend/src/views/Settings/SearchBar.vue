<script setup lang="ts">
import { ConfigTypeSchema, ModuleTypeSchema } from '@/client/api'
import { useCustomStore, useNoneBotStore } from '@/stores'
import { onMounted, ref, watch } from 'vue'
import { useSettingsStore, type ModuleConfigType } from './client'
import DotenvManageModal from './DotenvManageModal.vue'
import { useRoute } from 'vue-router'
import DotenvEditorModal from './DotenvEditorModal.vue'

const customStore = useCustomStore()
const settingsStore = useSettingsStore()
const nonebotStore = useNoneBotStore()

const route = useRoute()

const searchInputElement = ref<HTMLInputElement>()
const dotenvManageModal = ref<InstanceType<typeof DotenvManageModal> | null>()
const dotenvEditorModal = ref<InstanceType<typeof DotenvEditorModal> | null>()

onMounted(() => {
  settingsStore.searchInput = Array.isArray(route.query.search)
    ? route.query.search[0] ?? ''
    : route.query.search ?? ''
})

document.addEventListener('keydown', (e) => {
  if (e.key === '/' && !e.ctrlKey && !e.altKey && !e.metaKey) {
    e.preventDefault()
    searchInputElement.value?.focus()
  }
})

const checkIsSearch = (e: KeyboardEvent) => {
  if (e.key === 'Enter' && settingsStore.searchInput && !customStore.isInstantSearch) {
    settingsStore.updateViewData(settingsStore.searchInput)
  }
}

const searchInputPlaceholder = () => {
  let text = '键入 / 以开始'
  const noInstanceSearchText = ', 回车以搜索'
  if (!customStore.isInstantSearch) {
    text += noInstanceSearchText
  }
  return text
}

watch(
  () => settingsStore.searchInput,
  () => {
    if (customStore.isInstantSearch || !settingsStore.searchInput) {
      settingsStore.updateViewData(settingsStore.searchInput)
    }
  }
)

type moduleItem = {
  label: ModuleConfigType
  text: string
}

const configTypeItems = Object.values(ConfigTypeSchema.enum).map((type) => ({
  label: type,
  text: type.charAt(0).toUpperCase() + type.slice(1)
}))

const moduleItemFromEnum = Object.values(ModuleTypeSchema.enum).map((type) => ({
  label: type,
  text: type.charAt(0).toUpperCase() + type.slice(1)
}))

const moduleItems: moduleItem[] = [
  { label: 'all', text: 'All' },
  ...configTypeItems,
  ...moduleItemFromEnum
]
</script>

<template>
  <DotenvManageModal ref="dotenvManageModal" />
  <DotenvEditorModal ref="dotenvEditorModal" :theme="customStore.currentTheme" />

  <div class="flex flex-col gap-4">
    <div class="w-full flex justify-center">
      <div class="p-2 pl-4 bg-base-200 rounded-box w-full lg:w-3/4 flex items-center gap-2">
        <input
          ref="searchInputElement"
          v-model="settingsStore.searchInput"
          type="text"
          class="grow input input-sm bg-base-200 !outline-none border-none rounded-none p-0 leading-5 h-auto"
          :placeholder="searchInputPlaceholder()"
          @keydown="checkIsSearch($event)"
        />

        <span class="material-symbols-outlined opacity-50"> search </span>
      </div>
    </div>

    <div
      class="flex items-center justify-center md:justify-between flex-col md:flex-row gap-4 md:gap-0"
    >
      <div role="tablist" class="tabs tabs-boxed !flex md:grid flex-wrap">
        <a
          v-for="i in moduleItems"
          :key="i.text"
          role="tab"
          :class="{ tab: true, 'tab-active': i.label == settingsStore.viewModule }"
          @click="settingsStore.setViewModule(i.label)"
        >
          {{ i.text }}
        </a>
      </div>

      <div class="flex items-center gap-2">
        <button class="btn btn-sm btn-outline btn-primary" @click="dotenvManageModal?.openModal()">
          <div class="flex gap-1 items-center">
            <span class="material-symbols-outlined text-base"> menu </span>
            当前环境：{{ nonebotStore.selectedBot?.use_env || '未知' }}
          </div>
        </button>

        <button class="btn btn-sm" @click="dotenvEditorModal?.openModal()">编辑文件</button>
      </div>
    </div>
  </div>
</template>

<style lang="css" scoped>
.tab-active,
.badge-primary,
.active {
  color: white !important;
}

.active {
  --tw-bg-opacity: 0.2 !important;
  background-color: var(--fallback-n, oklch(var(--p) / var(--tw-bg-opacity))) !important;
  color: var(--fallback-nc, oklch(var(--p) / var(--tw-text-opacity))) !important;
}
</style>
