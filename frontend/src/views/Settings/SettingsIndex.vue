<script setup lang="ts">
import SettingCard from './SettingCard.vue'
import SearchBar from './SearchBar.vue'
import { useSettingsStore } from './client'

const settingsStore = useSettingsStore()

settingsStore.init()
</script>

<template>
  <div class="flex flex-col gap-6">
    <SearchBar />

    <div v-if="settingsStore.viewData.length" class="flex flex-col items-center gap-4">
      <div v-for="i in settingsStore.viewData" :key="i.title" class="w-full">
        <SettingCard :data="i" />
      </div>
      <span class="badge">共 {{ settingsStore.viewData.length }} 项</span>
    </div>
    <div v-else class="text-center">没有结果。</div>
  </div>
</template>
