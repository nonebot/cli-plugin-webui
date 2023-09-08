<script setup lang="ts">
import OfficialCheckIcon from "../Icons/OfficialCheckIcon.vue";
import CheckCircleIcon from "../Icons/CheckCircleIcon.vue";
import CancelCircleIcon from "../Icons/CancelCircleIcon.vue";

import { Adapter, Driver, Plugin } from "@/api/models";
import { computed, ref } from "vue";
import { routerTo } from "@/router/client";
import { API } from "@/api";
import { appStore } from "@/store/global";
import { nonebotExtensionStore } from "@/store/extensionStore";

const showModal = ref(false);

const openModal = () => {
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
};

defineExpose({
  openModal,
  closeModal,
});

const api = new API();

const props = defineProps<{ itemData: Plugin | Adapter | Driver }>();
const itemData = computed(() => {
  return props.itemData;
});

const uninstallModule = async () => {
  try {
    await api.uninstallModule(
      appStore().choiceProject.project_id,
      appStore().enabledEnv,
      props.itemData,
    );
    closeModal();
  } catch (error: any) {
    console.log(error);
  }

  try {
    await nonebotExtensionStore().updateData(appStore().choiceProject.project_id);
  } catch (error: any) {}
};
</script>

<template>
  <dialog :class="{ 'modal pl-0 md:pl-14': true, 'modal-open': showModal }">
    <form method="dialog" class="modal-box w-11/12 max-w-5xl sm:max-w-4xl rounded-lg">
      <div class="flex items-center">
        <h2 class="font-bold text-xl mr-2">{{ itemData.name }}</h2>
        <OfficialCheckIcon
          v-if="itemData.is_official"
          class="mr-1 h-6 w-6 text-green-600"
        />

        <div v-if="(itemData as Plugin).valid">
          <CheckCircleIcon
            v-if="(itemData as Plugin).valid"
            class="h-6 w-6 text-green-600"
          />
          <CancelCircleIcon v-else class="h-6 w-6 text-red-600" />
        </div>
      </div>

      <div class="mt-2 flex">
        <div>{{ itemData.author }}</div>
        <div class="ml-2 mr-2">|</div>
        <a
          class="link link-hover hover:link-primary"
          :href="itemData.homepage"
          target="_blank"
        >
          主页
        </a>
      </div>

      <div class="mt-2">{{ itemData.desc }}</div>

      <div class="mt-2 flex gap-2">
        <button class="btn btn-sm rounded" @click="routerTo('/setting')">设置</button>
        <button class="btn btn-sm rounded" @click="uninstallModule()">卸载</button>
        <a
          class="btn btn-sm rounded"
          :href="`https://registry.nonebot.dev/plugin/${itemData.project_link}:${itemData.module_name}`"
          target="_blank"
        >
          于 Registry 中查看
        </a>
      </div>
    </form>
    <form method="dialog" class="modal-backdrop">
      <button @click="closeModal()">close</button>
    </form>
  </dialog>
</template>
