<script setup lang="ts">
import { ProjectService, type ModuleConfigFather } from '@/client/api'
import SettingCard from './SettingCard.vue'
import { useNoneBotStore } from '@/stores'
import { ref } from 'vue'

const store = useNoneBotStore()

const configData = ref<ModuleConfigFather[]>([])

const getProjectMetaConfig = async () => {
  await ProjectService.getProjectMetaConfigV1ProjectConfigMetaDetailGet(
    store.selectedBot?.project_id!
  ).then((res) => {
    configData.value = configData.value.concat(res.detail)
  })
}

const getNonebotConfig = async () => {
  await ProjectService.getProjectNonebotConfigV1ProjectConfigNonebotDetailGet(
    store.selectedBot?.project_id!
  ).then((res) => {
    configData.value = configData.value.concat(res.detail)
  })
}

const getProjectPluginConfig = async () => {
  await ProjectService.getProjectNonebotPluginConfigV1ProjectConfigNonebotPluginDetailGet(
    store.selectedBot?.project_id!
  ).then((res) => {
    configData.value = configData.value.concat(res.detail)
  })
}

const getConfig = async () => {
  await getProjectMetaConfig()
  await getNonebotConfig()
  await getProjectPluginConfig()
}

getConfig()
</script>

<template>
  <div class="flex flex-col gap-4">
    <div v-for="i in configData" class="w-full">
      <SettingCard :data="i" />
    </div>
  </div>
</template>
