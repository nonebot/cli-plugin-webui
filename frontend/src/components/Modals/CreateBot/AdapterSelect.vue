<script setup lang="ts">
import { ref } from 'vue'
import { ModuleType, StoreService, type Adapter } from '@/client/api'
import ItemSelect from './ItemSelect.vue'

const adapterList = ref<Adapter[]>([])

StoreService.getNonebotStoreItemsV1StoreNonebotListGet(ModuleType.ADAPTER, 0, false, true).then(
  (res) => {
    adapterList.value = res.detail
  }
)
</script>

<template>
  <ItemSelect :data="adapterList" :data-type="ModuleType.ADAPTER" />
</template>
