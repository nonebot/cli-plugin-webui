<script setup lang="ts">
import { ProjectService, type ModuleConfigFather } from '@/client/api'
import SettingCard from './SettingCard.vue'
import { useNoneBotStore, useToastStore } from '@/stores'
import { ref } from 'vue'

const store = useNoneBotStore()
const toast = useToastStore()

const configData = ref<ModuleConfigFather[]>([])

const getProjectMetaConfig = async () => {
  await ProjectService.getProjectMetaConfigV1ProjectConfigMetaDetailGet(
    store.selectedBot?.project_id!
  )
    .then((res) => {
      configData.value = configData.value.concat(res.detail)
    })
    .catch((err) => {
      let detail = ''
      if (err.body) {
        detail = err.body.detail
      } else {
        detail = err
      }
      toast.add('error', `获取实例配置失败, 原因：${detail}`, '', 5000)
    })
}

const getNonebotConfig = async () => {
  await ProjectService.getProjectNonebotConfigV1ProjectConfigNonebotDetailGet(
    store.selectedBot?.project_id!
  )
    .then((res) => {
      configData.value = configData.value.concat(res.detail)
    })
    .catch((err) => {
      let detail = ''
      if (err.body) {
        detail = err.body.detail
      } else {
        detail = err
      }
      toast.add('error', `获取实例 NoneBot 配置失败, 原因：${detail}`, '', 5000)
    })
}

const getProjectPluginConfig = async () => {
  await ProjectService.getProjectNonebotPluginConfigV1ProjectConfigNonebotPluginDetailGet(
    store.selectedBot?.project_id!
  )
    .then((res) => {
      configData.value = configData.value.concat(res.detail)
    })
    .catch((err) => {
      let detail = ''
      if (err.body) {
        detail = err.body.detail
      } else {
        detail = err
      }
      toast.add('error', `获取实例插件设置失败, 原因：${detail}`, '', 5000)
    })
}

const getConfig = async () => {
  if (!store.selectedBot) {
    toast.add('warning', '未选择实例', '', 5000)
    return
  }

  await getProjectMetaConfig()
  await getNonebotConfig()
  await getProjectPluginConfig()
}

getConfig()
</script>

<template>
  <div class="flex flex-col gap-4">
    <div v-for="i in configData" :key="i.title" class="w-full">
      <SettingCard :data="i" />
    </div>
  </div>
</template>
