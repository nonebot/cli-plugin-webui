<script setup lang="ts">
import SearchBar from './SearchBar.vue'
import ExtensionContainer from './ExtensionContainer.vue'
import Pagination from './Pagination.vue'
import { useSearchStore } from './client'
import { onMounted } from 'vue'
import { useNoneBotStore } from '@/stores'

const store = useSearchStore(),
  nonebotStore = useNoneBotStore()

onMounted(async () => {
  if (!nonebotStore.selectedBot) return
  await store.updateData(nonebotStore.selectedBot.project_id, false)
})
</script>

<template>
  <div class="flex flex-col gap-6">
    <SearchBar />

    <Pagination />

    <ExtensionContainer />

    <Pagination />
  </div>
</template>
