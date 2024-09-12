<script setup lang="ts">
import { ModuleType, StoreService, type Driver } from '@/client/api'
import { ref } from 'vue'
import ItemSelect from './ItemSelect.vue'

const driverList = ref<Driver[]>([])

StoreService.getNonebotStoreItemsV1StoreNonebotListGet(ModuleType.DRIVER, 0, false, true).then(
  (res) => {
    driverList.value = res.detail
  }
)
</script>

<template>
  <ItemSelect :data="driverList" :data-type="ModuleType.DRIVER" />
</template>
