<script setup lang="ts">
import { ref } from 'vue'
import { StoreService, type Adapter } from '@/client/api'
import ItemSelect from './ItemSelect.vue'
import { useCreateBotStore } from '.'

const store = useCreateBotStore()

const adapterList = ref<Adapter[]>([])

const { data } = await StoreService.getNonebotStoreItemsV1StoreNonebotListGet({
  query: {
    module_type: 'adapter',
    page: 0,
    is_search: false,
    show_all: true
  }
})

if (data) {
  adapterList.value = data.detail
}
</script>

<template>
  <div class="flex flex-col gap-4 md:gap-8">
    <ItemSelect :data="adapterList" :data-type="'adapter'" />

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
