<script setup lang="ts" generic="T extends Plugin | Adapter | Driver">
import OfficialCheckIcon from "@/components/Icons/OfficialCheckIcon.vue";
import CheckCircleIcon from "@/components/Icons/CheckCircleIcon.vue";
import CancelCircleIcon from "@/components/Icons/CancelCircleIcon.vue";
import PackageIcon from "@/components/Icons/PackageIcon.vue";
import AccountIcon from "@/components/Icons/AccountIcon.vue";
import LogShow from "@/components/CustomModal/LogShow.vue";
import ExtensionDetailModal from "@/components/NonebotStore/ExtensionDetailModal.vue";

import { Adapter, Driver, Plugin } from "@/api/models";
import { computed, ref } from "vue";
import { nonebotExtensionStore } from "@/store/extensionStore";
import { API } from "@/api";
import { appStore } from "@/store/global";
import { ToastWrapper } from "@/utils/notification";
import { limitContent } from "@/utils";
import { AxiosError } from "axios";

const props = defineProps<{ itemData: T }>();

const api = new API();
const notice = new ToastWrapper("Nonebot Store");

const logKey = ref("");
const showInstallTipsModal = ref(false);
const logShowModal = ref<InstanceType<typeof LogShow> | null>();
const extensionDetailModal = ref<InstanceType<typeof ExtensionDetailModal> | null>();

const itemData = computed(() => {
  return props.itemData;
});

const doInstall = async (pass?: boolean) => {
  showInstallTipsModal.value = false;

  // 仅针对插件的 valid 属性
  if (pass || pass === undefined) {
    logShowModal.value?.openModal();
    const projectID = appStore().choiceProject.project_id;
    const module = nonebotExtensionStore().choiceItem;
    await api
      .installModule(projectID, appStore().enabledEnv, module)
      .then((resp) => {
        logKey.value = resp.log_key;
      })
      .catch((error: AxiosError) => {
        let reason: string;
        if (error.response) {
          reason = (error.response.data as { detail: string })?.detail;
        } else {
          reason = error.message;
        }
        notice.error(`安装拓展失败：${reason}`);
      });
  } else {
    showInstallTipsModal.value = true;
  }
};

const isRetry = async (data: boolean) => {
  if (data) {
    await doInstall(true);
  }
};
</script>

<template>
  <div class="extension-card card card-compact w-full bg-base-200 rounded-lg">
    <div class="card-body bg-base-200 rounded-lg transition-all hover:shadow-lg">
      <dialog
        :class="{
          'modal pl-0 md:pl-14': true,
          'modal-open': showInstallTipsModal,
        }"
      >
        <form method="dialog" class="modal-box rounded-lg">
          <h3 class="font-bold text-lg">注意</h3>
          <p class="py-4">
            {{ nonebotExtensionStore().choiceItem.name }}
            ({{ nonebotExtensionStore().choiceItem.project_link }})<br />
            测试未通过，安装并运行后可能出现意料之外的问题。
          </p>
          <div class="modal-action">
            <button
              class="btn rounded-lg h-10 min-h-0"
              @click="showInstallTipsModal = false"
            >
              取消
            </button>

            <button class="btn rounded-lg h-10 min-h-0" @click="doInstall(true)">
              无视风险，继续安装！
            </button>
          </div>
        </form>
      </dialog>

      <LogShow
        ref="logShowModal"
        @is-retry="isRetry"
        @is-o-k="nonebotExtensionStore().updateData(appStore().choiceProject.project_id)"
        :log-key="logKey"
      />

      <ExtensionDetailModal ref="extensionDetailModal" :item-data="itemData" />

      <h2 class="card-title !font-normal !text-base !mb-0">
        <a :href="itemData.homepage" target="_blank">{{
          limitContent(itemData.name, 27)
        }}</a>
        <div class="flex items-center">
          <div
            v-if="itemData.is_official"
            class="mr-1 tooltip font-normal"
            data-tip="官方认证"
          >
            <OfficialCheckIcon class="h-6 w-6 text-green-600" />
          </div>

          <div v-if="'valid' in itemData" class="flex items-center">
            <div
              v-if="(itemData as Plugin).valid"
              class="tooltip font-normal"
              data-tip="测试通过"
            >
              <CheckCircleIcon class="h-6 w-6 text-green-600" />
            </div>
            <div v-else class="tooltip font-normal" data-tip="测试未通过">
              <CancelCircleIcon class="h-6 w-6 text-red-600" />
            </div>
          </div>
        </div>
      </h2>
      <div>
        <div
          v-if="itemData.tags"
          v-for="tag in itemData.tags"
          class="badge badge-outline tooltip"
          :style="`color: ${tag.color}`"
          :data-tip="tag.label"
        >
          {{ tag.label }}
        </div>
      </div>
      <p class="mb-2 text-gray-600">{{ itemData.desc }}</p>
      <div class="flex justify-between">
        <div>
          <div
            class="tooltip flex items-center text-xs text-gray-500"
            :data-tip="itemData.project_link"
          >
            <PackageIcon class="h-4 w-4 mr-2" />
            {{ limitContent(itemData.project_link, 25) }}
          </div>
          <div class="mt-2 flex items-center text-xs text-gray-500">
            <AccountIcon class="h-4 w-4 mr-2" />
            {{ itemData.author }}
          </div>
        </div>

        <div class="flex flex-col-reverse">
          <button
            v-if="itemData.is_download"
            class="btn btn-sm btn-primary btn-outline whitespace-nowrap"
            @click="extensionDetailModal?.openModal()"
          >
            详细
          </button>

          <button
            v-else
            class="install-btn btn btn-sm btn-primary text-white whitespace-nowrap"
            @click="
              nonebotExtensionStore().choiceItem = itemData;
              doInstall((itemData as Plugin).valid);
            "
          >
            安装
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
.extension-card .install-btn {
  opacity: 0;
}

.extension-card:hover .install-btn {
  opacity: 100;
}
</style>
