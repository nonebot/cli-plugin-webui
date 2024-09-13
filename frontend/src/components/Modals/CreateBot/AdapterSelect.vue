<script setup lang="ts">
import { ref } from 'vue'
import { ModuleType, StoreService, type Adapter } from '@/client/api'
import ItemSelect from './ItemSelect.vue'
import { useCreateBotStore } from '.'

const store = useCreateBotStore()

const adapterList = ref<Adapter[]>([])

StoreService.getNonebotStoreItemsV1StoreNonebotListGet(ModuleType.ADAPTER, 0, false, true).then(
  (res) => {
    adapterList.value = res.detail
  }
)
</script>

<template>
  <div class="flex flex-col gap-8">
    <ItemSelect :data="adapterList" :data-type="ModuleType.ADAPTER" />

    <div class="flex justify-between items-center">
      <button class="btn btn-sm btn-primary text-base-100" @click="store.step--">上一步</button>

      <button
        :class="{
          'btn btn-sm btn-primary text-base-100': true,
          'btn-disabled': !store.adapters.length
        }"
        @click="store.step++"
      >
        下一步
      </button>
    </div>
  </div>
</template>
