<script setup lang="ts">
import { ref } from 'vue'
import { useNoneBotStore } from '@/stores'
import { limitContentShow } from '@/client/utils'

import FolderSelect from '@/components/Modals/Global/FolderSelect.vue'

const store = useNoneBotStore()

const folderSelectModal = ref<InstanceType<typeof FolderSelect> | null>()

const acceptModalData = (data: string) => {
  store.projectPath = data
}
</script>

<template>
  <FolderSelect ref="folderSelectModal" @select-folder="acceptModalData" />

  <div class="flex flex-col items-center justify-center">
    <div class="form-control w-full max-w-xs">
      <div class="label">
        <span class="label-text">实例名称</span>
      </div>
      <input
        type="text"
        placeholder="请输入"
        class="input input-bordered w-full max-w-xs"
        v-model="store.name"
      />
    </div>

    <div class="form-control w-full max-w-xs">
      <div class="label">
        <span class="label-text">实例绝对路径</span>
      </div>
      <button class="btn btn-outline btn-primary" @click="folderSelectModal?.openModal">
        选择文件夹
      </button>
      <div class="label">
        <span v-if="store.projectPath" class="label-text bg-base-300 p-1 rounded w-full">
          当前选择: (Base Dir)/{{ limitContentShow(store.projectPath, 30) }}
        </span>
      </div>
    </div>
  </div>
</template>
