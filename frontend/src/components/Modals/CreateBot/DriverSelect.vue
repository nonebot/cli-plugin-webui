<script setup lang="ts">
import { StoreService, type Driver } from '@/client/api'
import { ref } from 'vue'
import ItemSelect from './ItemSelect.vue'

const driverList = ref<Driver[]>([])

StoreService.getNonebotStoreItemsV1StoreNonebotListGet('driver', 0, false, true).then((res) => {
  driverList.value = res.detail
})
</script>

<template>
  <ItemSelect :data="driverList" :data-type="'Driver'" />
</template>
