<script setup lang="ts">
import { Adapter, Driver, Plugin } from "@/api/schemas";
import { computed, ref } from "vue";
import { routerTo } from "@/router/client";
import api from "@/api";
import { appStore } from "@/store/global";
import { notice } from "@/utils/notification";
import { nonebotExtensionStore } from "@/store/extensionStore";
import type { AxiosError } from "axios";

const extensionDetailModal = ref<HTMLDialogElement>();

defineExpose({
  openModal() {
    extensionDetailModal.value?.showModal();
  },
  closeModal() {
    extensionDetailModal.value?.close();
  },
});

const props = defineProps<{ itemData: Plugin | Adapter | Driver }>();
const itemData = computed(() => {
  return props.itemData;
});

const uninstallModule = async () => {
  await api
    .uninstallModule(
      appStore().enabledEnv,
      props.itemData,
      appStore().choiceProject.project_id,
    )
    .then(() => {
      extensionDetailModal.value?.close();
      return Promise.resolve();
    })
    .catch((error: AxiosError) => {
      let reason: string;
      if (error.response) {
        reason = (error.response.data as { detail: string })?.detail;
      } else {
        reason = error.message;
      }
      notice.error(`卸载模块时失败：${reason}`);
    });

  await nonebotExtensionStore().updateData(appStore().choiceProject.project_id);
};
</script>

<template>
  <dialog ref="extensionDetailModal" class="modal">
    <div class="modal-box w-11/12 max-w-5xl sm:max-w-4xl rounded-lg">
      <div class="flex items-center">
        <h2 class="font-bold text-xl mr-2">{{ itemData.name }}</h2>
        <span
          v-if="itemData.is_official"
          class="material-symbols-outlined text-green-600"
        >
          verified
        </span>

        <div v-if="(itemData as Plugin).valid" class="flex items-center">
          <span
            v-if="(itemData as Plugin).valid"
            class="material-symbols-outlined text-green-600"
          >
            check_circle
          </span>
          <span v-else class="material-symbols-outlined text-red-600"> cancel </span>
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
    </div>
    <form method="dialog" class="modal-backdrop">
      <button>close</button>
    </form>
  </dialog>
</template>

<style scoped>
.material-symbols-outlined {
  font-variation-settings:
    "FILL" 1,
    "wght" 300,
    "GRAD" 0,
    "opsz" 40;
}
</style>
