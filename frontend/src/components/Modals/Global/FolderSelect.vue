<script setup lang="ts">
import { FileService, type FileInfo } from '@/client/api'
import { covertTimestampToDateString, limitContentShow } from '@/client/utils'
import { ref } from 'vue'

const emit = defineEmits<{
  selectFolder: [value: string]
}>()

const folderSelectModal = ref<HTMLDialogElement>()

defineExpose({
  openModal: () => {
    folderSelectModal.value?.showModal()

    getFileList('')
  },
  closeModal: () => {
    folderSelectModal.value?.close()
  }
})

const newFolderModal = ref<HTMLDialogElement>()

const fileList = ref<FileInfo[]>([]),
  newFolderName = ref(''),
  currentPath = ref(''),
  selectedFolder = ref('')

const getFileList = (path: string) => {
  FileService.getFileListV1FileListGet(path).then((res) => {
    fileList.value = res.detail
  })
}

const createFolder = (folderName: string, path: string) => {
  FileService.createFileV1FileCreatePost({ name: folderName, path: path, is_dir: true }).then(
    (res) => {
      fileList.value = res.detail
      newFolderName.value = ''
      newFolderModal.value?.close()
    }
  )
}

const deleteFolder = (path: string) => {
  FileService.deleteFileV1FileDeleteDelete(path).then((res) => {
    fileList.value = res.detail
  })
}

const updateFileList = (path: string, isFolder: boolean) => {
  if (!isFolder) return

  currentPath.value = path
  getFileList(path)
}

const selectFolder = (path: string, isFolder: boolean) => {
  if (!isFolder) return
  selectedFolder.value = path
}
</script>

<template>
  <dialog ref="folderSelectModal" class="modal">
    <div class="modal-box w-11/12 max-w-5xl rounded-xl flex flex-col gap-4">
      <h3 class="font-semibold text-lg">文件夹选择</h3>

      <div class="overflow-hidden max-h-96 h-full bg-base-200 rounded-lg p-4">
        <div class="text-sm breadcrumbs pb-2">
          <ul>
            <li @click="updateFileList('', true)">
              <a>(Base Dir) /</a>
            </li>
            <li v-for="(item, index) in currentPath.split('/')">
              <a
                @click="
                  updateFileList(
                    currentPath
                      .split('/')
                      .slice(0, index + 1)
                      .join('/'),
                    true
                  )
                "
              >
                {{ item }}
              </a>
            </li>
          </ul>
        </div>

        <div class="overflow-auto max-h-80">
          <table class="table table-pin-rows w-full">
            <thead class="z-10">
              <tr class="border-b-0">
                <th class="rounded-s-lg">名称</th>
                <th>修改时间</th>
                <th>类型</th>
                <th class="rounded-e-lg">操作</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-if="fileList.length"
                v-for="file in fileList"
                role="button"
                class="transition hover:bg-base-300"
                @click="selectFolder(file.path, file.is_dir)"
              >
                <td class="flex items-center gap-1 shrink-0 whitespace-nowrap">
                  <span class="material-symbols-outlined">
                    {{ file.is_dir ? 'folder' : 'draft' }}
                  </span>
                  <a class="hover:link" @click="updateFileList(file.path, file.is_dir)">
                    {{ limitContentShow(file.name, 10) }}
                  </a>
                </td>
                <td class="whitespace-nowrap">
                  {{ covertTimestampToDateString(file.modified_time) }}
                </td>
                <td class="whitespace-nowrap">{{ file.is_dir ? '文件夹' : '文件' }}</td>
                <td class="flex items-center whitespace-nowrap">
                  <label class="swap">
                    <input type="checkbox" />

                    <span class="swap-on fill-current material-symbols-outlined"> check </span>

                    <span
                      class="swap-off fill-current material-symbols-outlined"
                      @click="deleteFolder(selectedFolder)"
                    >
                      delete
                    </span>
                  </label>
                </td>
              </tr>
              <tr v-else>
                <td colspan="4" class="text-center">暂无数据</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="bg-base-200 rounded-lg p-4 text-sm">
        当前选择:
        <span v-if="selectedFolder" class="bg-base-300 p-1 rounded">
          (Base Dir)/{{ selectedFolder }}
        </span>
      </div>

      <div class="flex justify-between">
        <div class="flex gap-4">
          <button class="btn btn-sm" @click="updateFileList(currentPath, true)">刷新</button>
          <button class="btn btn-sm" @click="newFolderModal?.showModal">新建文件夹</button>
          <button class="btn btn-sm" @click="selectFolder(currentPath, true)">选中当前目录</button>
        </div>

        <div class="flex gap-4">
          <button class="btn btn-sm" @click="folderSelectModal?.close">取消</button>
          <button
            :class="{ 'btn btn-sm btn-primary text-white': true, 'btn-disabled': !selectedFolder }"
            @click="folderSelectModal?.close(), emit('selectFolder', selectedFolder)"
          >
            确认
          </button>
        </div>
      </div>
    </div>
  </dialog>

  <dialog ref="newFolderModal" class="modal">
    <div class="modal-box rounded-xl flex flex-col gap-4">
      <h3 class="font-semibold text-lg">新建文件夹</h3>
      <div class="flex justify-center">
        <input
          type="text"
          placeholder="请输入"
          class="input input-bordered w-full max-w-xs"
          v-model="newFolderName"
        />
      </div>
      <div class="flex justify-end gap-4">
        <button class="btn btn-sm" @click="newFolderModal?.close(), (newFolderName = '')">
          取消
        </button>
        <button
          :class="{ 'btn btn-sm btn-primary text-white': true, 'btn-disabled': !newFolderName }"
          @click="createFolder(newFolderName, currentPath)"
        >
          确认
        </button>
      </div>
    </div>
  </dialog>
</template>

<style scoped>
.material-symbols-outlined {
  font-variation-settings:
    'FILL' 0,
    'wght' 300,
    'GRAD' 0,
    'opsz' 24;
}
</style>
