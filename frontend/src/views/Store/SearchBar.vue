<script setup lang="ts">
import { ref, watch } from 'vue'
import { useSearchStore } from './client'
import { SearchRequest, SearchTag } from '@/client/api'
import { useCustomStore, useNoneBotStore } from '@/stores'

const store = useSearchStore(),
  nonebotStore = useNoneBotStore(),
  customStore = useCustomStore()

const searchInputElement = ref<HTMLInputElement>(),
  authorInput = ref(''),
  labelInput = ref('')

document.addEventListener('keydown', (e) => {
  if (e.key === '/' && !e.ctrlKey && !e.altKey && !e.metaKey) {
    e.preventDefault()
    searchInputElement.value?.focus()
  }
})

const checkIsDelete = (e: KeyboardEvent) => {
  if (e.key === 'Backspace' && !store.searchInput) {
    store.searchTags.pop()
  }
}

const checkIsAddTag = (e: KeyboardEvent) => {
  const addTag = (label: SearchTag.label, text: string) => {
    e.preventDefault()
    store.searchTags.push({ label, text })
    store.searchInput = ''
  }

  const noTextLabel = ['official', 'valid', 'downloaded']

  if (e.key === ' ') {
    let input = store.searchInput

    for (let tag in SearchTag.label) {
      tag = tag.toLowerCase()
      if (input.startsWith(`${tag}:`) && input.length > tag.length + 1) {
        if (noTextLabel.includes(tag)) {
          input = ''
        }

        addTag(tag as SearchTag.label, input.slice(tag.length + 1))
        return
      }
    }
  }
}

const checkIsSearch = (e: KeyboardEvent) => {
  if (
    e.key === 'Enter' &&
    (store.searchInput || store.searchTags.length > 0) &&
    !customStore.isInstantSearch
  ) {
    store.upDataBySearch(nonebotStore.selectedBot?.project_id!)
  }
}

watch(
  () => [store.searchInput, store.searchTags.length],
  async () => {
    if (customStore.isInstantSearch || (!store.searchInput && store.searchTags.length === 0)) {
      await store.upDataBySearch(nonebotStore.selectedBot?.project_id!)
    }
  }
)

const searchInputPlaceholder = () => {
  let text = '键入 / 以开始'
  const noInstanceSearchText = ', 回车以搜索'
  if (!customStore.isInstantSearch) {
    text += noInstanceSearchText
  }
  return text
}

type moduleItem = {
  label: SearchRequest.module_type
  tip: string
}

const moduleItems: moduleItem[] = [
  { label: SearchRequest.module_type.PLUGIN, tip: '插件' },
  { label: SearchRequest.module_type.ADAPTER, tip: '适配器' },
  { label: SearchRequest.module_type.DRIVER, tip: '驱动器' }
]

type filterItem = {
  label: SearchTag.label
  text?: string
  tip: string
}

const filterItems: filterItem[] = [
  { label: SearchTag.label.OFFICIAL, tip: '官方认证' },
  { label: SearchTag.label.VALID, tip: '测试通过' },
  { label: SearchTag.label.DOWNLOADED, tip: '已下载' },
  { label: SearchTag.label.LATEST, text: 'week', tip: '最近一周' },
  { label: SearchTag.label.LATEST, text: 'month', tip: '最近一月' }
]
</script>

<template>
  <div class="flex flex-col gap-4">
    <div class="w-full flex justify-center">
      <div class="p-2 pl-4 bg-base-200 rounded-box w-full lg:w-3/4 flex items-center gap-2">
        <div class="w-full flex flex-wrap items-center gap-1">
          <div
            v-for="tag in store.searchTags"
            :key="tag.label"
            role="button"
            class="badge badge-primary"
            @click="store.removeTag(tag)"
          >
            <span v-if="tag.text">{{ tag.label }}:{{ tag.text }}</span>
            <span v-else>{{ tag.label }}</span>
          </div>
          <input
            ref="searchInputElement"
            v-model="store.searchInput"
            type="text"
            class="grow input input-sm bg-base-200 !outline-none border-none rounded-none p-0 leading-5 h-auto"
            :placeholder="searchInputPlaceholder()"
            @keydown="checkIsDelete($event), checkIsAddTag($event), checkIsSearch($event)"
          />
        </div>
        <span
          v-if="store.searchInput || store.searchTags.length > 0"
          role="button"
          class="material-symbols-outlined opacity-50 hover:opacity-100 transition"
          @click="store.clear()"
        >
          close
        </span>
        <span v-else class="material-symbols-outlined opacity-50"> search </span>
      </div>
    </div>

    <div class="flex justify-between">
      <div role="tablist" class="tabs tabs-boxed">
        <a
          v-for="m in moduleItems"
          :key="m.tip"
          role="tab"
          :class="{ tab: true, 'tab-active': store.viewModule === m.label }"
          @click="store.selectModule(m.label, nonebotStore.selectedBot?.project_id!)"
        >
          {{ m.tip }}
        </a>
      </div>

      <div class="flex items-center gap-2">
        <div class="dropdown dropdown-end">
          <div tabindex="0" role="button" class="btn btn-sm btn-outline btn-primary">
            <div class="flex gap-1 items-center">
              <span class="material-symbols-outlined text-base"> filter_list </span>
              筛选
            </div>
          </div>
          <div tabindex="0" class="dropdown-content z-[1] bg-base-200 rounded-lg">
            <ul class="menu menu-sm w-36 gap-y-0.5">
              <li
                v-for="filter in filterItems"
                :key="filter.tip"
                role="button"
                @click="store.updateTag({ label: filter.label, text: filter.text })"
              >
                <a
                  :class="{
                    active: store.isTagExisted({ label: filter.label, text: filter.text })
                  }"
                >
                  {{ filter.tip }}
                </a>
              </li>
            </ul>
          </div>
        </div>

        <div class="dropdown dropdown-end">
          <div tabindex="0" role="button" class="btn btn-sm btn-outline btn-primary">
            <div class="flex gap-1 items-center">
              <span class="material-symbols-outlined text-base"> person </span>
              作者
            </div>
          </div>
          <div tabindex="0" class="dropdown-content z-[1] p-2 bg-base-200 rounded-lg">
            <input
              v-model="authorInput"
              placeholder="请键入"
              class="input input-sm input-bordered"
              @keydown.enter="
                store.updateTag({ label: SearchTag.label.AUTHOR, text: authorInput }),
                  (authorInput = '')
              "
            />
          </div>
        </div>

        <div class="dropdown dropdown-end">
          <div tabindex="0" role="button" class="btn btn-sm btn-outline btn-primary">
            <div class="flex gap-1 items-center">
              <span class="material-symbols-outlined text-base"> sell </span>
              标签
            </div>
          </div>
          <div tabindex="0" class="dropdown-content z-[1] p-2 bg-base-200 rounded-lg">
            <input
              v-model="labelInput"
              placeholder="请键入"
              class="input input-sm input-bordered"
              @keydown.enter="
                store.updateTag({ label: SearchTag.label.TAG, text: labelInput }), (labelInput = '')
              "
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
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
