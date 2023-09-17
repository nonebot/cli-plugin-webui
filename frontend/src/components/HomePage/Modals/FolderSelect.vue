<script setup lang="ts">
import { ref, watch } from "vue";
import { notice } from "@/utils/notification";
import { FileInfo } from "@/api/models";
import { limitContent } from "@/utils";
import { api } from "../client";
import { AxiosError } from "axios";

const showModal = ref(false);
const showCreateFolderModal = ref(false);

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

const nowPath = ref("");
const nowPathStack = ref<string[]>([]);
const files = ref<FileInfo[]>([]);
const selectedFolder = ref("Unknown");
const newFolderName = ref("");

const emit = defineEmits(["onSelectedFolder"]);

const getFiles = async (path: string) => {
  await api
    .getFileList(path)
    .then((resp) => {
      files.value = resp.files;
      nowPathStack.value = nowPath.value.split("/");
    })
    .catch((error: AxiosError) => {
      let reason: string;
      if (error.response) {
        reason = (error.response.data as { detail: string })?.detail;
      } else {
        reason = error.message;
      }
      notice.error(`获取文件列表失败：${reason}`);
    });
};

const createFile = async (fileName: string, path: string) => {
  await api
    .createFile(fileName, true, path)
    .then((resp) => {
      files.value = resp.files;
      nowPathStack.value = nowPath.value.split("/");
      newFolderName.value = "";
      showCreateFolderModal.value = false;
      openModal();
    })
    .catch((error: AxiosError) => {
      let reason: string;
      if (error.response) {
        reason = (error.response.data as { detail: string })?.detail;
      } else {
        reason = error.message;
      }
      notice.error(`创建文件夹失败：${reason}`);
    });
};

const deleteFile = async (fileName: string, isFolder: boolean, path: string) => {
  await api
    .deleteFile(fileName, isFolder, path)
    .then((resp) => {
      files.value = resp.files;
      nowPathStack.value = nowPath.value.split("/");
    })
    .catch((error: AxiosError) => {
      let reason: string;
      if (error.response) {
        reason = (error.response.data as { detail: string })?.detail;
      } else {
        reason = error.message;
      }
      notice.error(`删除文件失败：${reason}`);
    });
};

const nextDir = (path: string, is_dir: number) => {
  if (!is_dir) {
    return;
  }
  nowPath.value = path;
  getFiles(path);
};

const choiceDir = (path: string, is_dir: number) => {
  if (!is_dir) {
    notice.warning("请选择文件夹");
    return;
  }
  selectedFolder.value = path + "/(实例名称)";
};

const convertTime = (time: string) => {
  const fixed_time = Number(time);
  const date = new Date(fixed_time * 1000);
  const year = date.getFullYear();
  const mouth = date.getMonth();
  const day = date.getDay();
  const hours = date.getHours();
  const minutes = date.getMinutes();
  return `${year}/${mouth}/${day} ${hours}:${minutes}`;
};

watch(showModal, () => {
  if (showModal.value) {
    getFiles(nowPath.value);
  }
});
</script>

<template>
  <dialog :class="{ 'modal pl-0 md:pl-14': true, 'modal-open': showModal }">
    <form method="dialog" class="modal-box rounded-lg">
      <h3 class="font-bold text-lg">NoneBot 实例安装位置</h3>
      <div class="text-sm breadcrumbs">
        <ul>
          <li><a @click="nextDir('', 1)">(Base Dir)</a></li>
          <li v-for="(dir, index) in nowPathStack">
            <a @click="nextDir(nowPathStack.slice(0, index + 1).join('\\'), 1)">
              <svg
                v-if="dir"
                class="w-4 h-4 mr-2 stroke-current"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke-width="1.5"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M2.25 12.75V12A2.25 2.25 0 014.5 9.75h15A2.25 2.25 0 0121.75 12v.75m-8.69-6.44l-2.12-2.12a1.5 1.5 0 00-1.061-.44H4.5A2.25 2.25 0 002.25 6v12a2.25 2.25 0 002.25 2.25h15A2.25 2.25 0 0021.75 18V9a2.25 2.25 0 00-2.25-2.25h-5.379a1.5 1.5 0 01-1.06-.44z"
                />
              </svg>
              {{ dir }}
            </a>
          </li>
        </ul>
      </div>
      <div class="overflow-x-auto">
        <table class="table table-compact w-full">
          <thead>
            <tr>
              <th>名称</th>
              <th>修改时间</th>
              <th>类型</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-if="files.length"
              v-for="i in files"
              :key="i.name"
              class="hover"
              @click="choiceDir(i.path, i.is_dir)"
            >
              <td class="flex items-center">
                <svg
                  v-if="i.is_dir === 1"
                  class="w-4 h-4 mr-2 stroke-current"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke-width="1.5"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M2.25 12.75V12A2.25 2.25 0 014.5 9.75h15A2.25 2.25 0 0121.75 12v.75m-8.69-6.44l-2.12-2.12a1.5 1.5 0 00-1.061-.44H4.5A2.25 2.25 0 002.25 6v12a2.25 2.25 0 002.25 2.25h15A2.25 2.25 0 0021.75 18V9a2.25 2.25 0 00-2.25-2.25h-5.379a1.5 1.5 0 01-1.06-.44z"
                  />
                </svg>
                <svg
                  v-else
                  class="w-4 h-4 mr-2 stroke-current"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke-width="1.5"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z"
                  />
                </svg>
                <a class="file-name" @click="nextDir(i.path, i.is_dir)">
                  {{ limitContent(i.name, 10) }}
                </a>
              </td>
              <td>{{ convertTime(i.modified_time) }}</td>
              <td>
                <p v-if="i.is_dir === 1">文件夹</p>
                <p v-else>文件</p>
              </td>
              <td class="p-0">
                <div class="flex">
                  <label class="swap">
                    <input type="checkbox" />
                    <svg
                      class="swap-on fill-current"
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 24 24"
                      width="20"
                      height="20"
                    >
                      <title>删除文件</title>
                      <path d="M21,7L9,19L3.5,13.5L4.91,12.09L9,16.17L19.59,5.59L21,7Z" />
                    </svg>
                    <svg
                      class="swap-off fill-current"
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 24 24"
                      width="20"
                      height="20"
                      @click="deleteFile(i.name, i.is_dir ? true : false, i.path)"
                    >
                      <title>确认</title>
                      <path
                        d="M6,19A2,2 0 0,0 8,21H16A2,2 0 0,0 18,19V7H6V19M8,9H16V19H8V9M15.5,4L14.5,3H9.5L8.5,4H5V6H19V4H15.5Z"
                      />
                    </svg>
                  </label>
                </div>
              </td>
            </tr>
            <tr v-else>
              <td>该目录下无文件</td>
            </tr>
          </tbody>
        </table>
      </div>

      <p class="pt-4">当前选择：</p>
      <p class="overflow-x-auto text-sm">(Base Dir)/{{ selectedFolder }}</p>

      <div class="modal-action">
        <button class="btn rounded-lg h-10 min-h-0" @click="showCreateFolderModal = true">
          新建文件夹
        </button>

        <button class="btn rounded-lg h-10 min-h-0" @click="getFiles(nowPath)">
          刷新
        </button>

        <div class="w-full"></div>

        <button
          class="btn btn-primary rounded-lg h-10 min-h-0 text-white"
          @click="emit('onSelectedFolder', selectedFolder), closeModal()"
        >
          选择
        </button>
      </div>
    </form>
  </dialog>

  <dialog
    :class="{
      'modal pl-0 md:pl-14': true,
      'modal-open': showCreateFolderModal,
    }"
  >
    <form method="dialog" class="modal-box rounded-lg">
      <h3 class="font-bold text-lg">新建文件夹</h3>
      <input
        v-model="newFolderName"
        type="text"
        placeholder="文件夹名称"
        class="mt-4 input input-bordered w-full text-sm"
      />
      <div class="modal-action">
        <button
          class="btn rounded-lg h-10 min-h-0"
          @click="showCreateFolderModal = false"
        >
          取消
        </button>

        <button
          class="btn btn-primary rounded-lg h-10 min-h-0 text-white"
          @click="createFile(newFolderName, nowPath)"
        >
          新建文件夹
        </button>
      </div>
    </form>
  </dialog>
</template>

<style>
.file-name:hover {
  cursor: pointer;
  text-decoration: underline;
}
</style>
