<script setup lang="ts">
import { StoreService, type Driver } from "@/client/api";
import { ref } from "vue";
import ItemSelect from "./ItemSelect.vue";
import { useCreateBotStore } from ".";

const store = useCreateBotStore();

const driverList = ref<Driver[]>([]);

const { data } = await StoreService.getNonebotStoreItemsV1StoreNonebotListGet({
  query: {
    module_type: "driver",
    page: 0,
    is_search: false,
    show_all: true,
  },
});

if (data) {
  driverList.value = data.detail;
}
</script>

<template>
  <div class="flex flex-col gap-4 md:gap-8">
    <ItemSelect :data="driverList" :data-type="'driver'" />

    <div class="flex justify-between items-center">
      <button class="btn btn-sm btn-primary text-base-100" @click="store.step--">
        上一步
      </button>

      <button
        :class="{
          'btn btn-sm btn-primary text-base-100': true,
          'btn-disabled': !store.drivers.length,
        }"
        @click="store.step++"
      >
        下一步
      </button>
    </div>
  </div>
</template>
