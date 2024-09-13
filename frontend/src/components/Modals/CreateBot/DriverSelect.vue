<script setup lang="ts">
import { ModuleType, StoreService, type Driver } from '@/client/api'
import { ref } from 'vue'
import ItemSelect from './ItemSelect.vue'
import { useCreateBotStore } from '.'

const store = useCreateBotStore()

const driverList = ref<Driver[]>([])

StoreService.getNonebotStoreItemsV1StoreNonebotListGet(ModuleType.DRIVER, 0, false, true).then(
  (res) => {
    driverList.value = res.detail
  }
)
</script>

<template>
  <div class="flex flex-col gap-8">
    <ItemSelect :data="driverList" :data-type="ModuleType.DRIVER" />

    <div class="flex justify-between items-center">
      <button class="btn btn-sm btn-primary text-base-100" @click="store.step--">上一步</button>

      <button
        :class="{
          'btn btn-sm btn-primary text-base-100': true,
          'btn-disabled': !store.drivers.length
        }"
        @click="store.step++"
      >
        下一步
      </button>
    </div>
  </div>
</template>
