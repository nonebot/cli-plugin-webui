<script setup lang="ts">
import LogShow from "@/components/CustomModal/LogShow.vue";
import WarningCircleIcon from "@/components/Icons/WarningCircleIcon.vue";
import ErrorCircleIcon from "@/components/Icons/ErrorCircleIcon.vue";
import CloseIcon from "@/components/Icons/CloseIcon.vue";

import { ref } from "vue";
import { AxiosError } from "axios";
import { notice } from "@/utils/notification";
import { CheckProjectTomlDetail } from "@/api/models";
import { api, mirrorList } from "../client";

const addProjectByPathModal = ref<HTMLDialogElement>();

defineExpose({
  openModal: () => {
    addProjectByPathModal.value?.showModal();
  },
  closeModal: () => {
    addProjectByPathModal.value?.close();
  },
});

const addProjectByPathNextModal = ref<HTMLDialogElement>();

const openNextModal = () => {
  addProjectByPathNextModal.value?.showModal();
};

const closeNextModal = () => {
  addProjectByPathNextModal.value?.close();
};

const logShowModal = ref<InstanceType<typeof LogShow> | null>();

const projectName = ref("");
const projectDir = ref("");
const projectMirror = ref("");

const checkIsPass = ref(false);
const checkNoticeLevel = ref("");
const checkMsg = ref("");
const checkDetail = ref<CheckProjectTomlDetail | null>();

const logKey = ref("");

const doCheck = async () => {
  if (!projectDir.value) {
    notice.warning("请键入实例位置");
    return;
  }

  await api
    .checkProjectToml(projectDir.value)
    .then((resp) => {
      checkIsPass.value = resp.is_pass;
      checkNoticeLevel.value = resp.level;
      checkMsg.value = resp.msg;
      checkDetail.value = resp.detail;
      if (checkDetail.value) {
        projectName.value = checkDetail.value.project_name;
      }
    })
    .catch((error: AxiosError) => {
      let reason: string;
      if (error.response) {
        reason = (error.response.data as { detail: string })?.detail;
      } else {
        reason = error.message;
      }
      notice.error(`扫描失败：${reason}`);
    });
};

const doAddProject = async () => {
  if (!projectMirror.value) {
    notice.warning("请选择 Python 镜像源");
    return;
  }

  await api
    .addProject({
      project_name: projectName.value,
      project_dir: projectDir.value,
      mirror_url: projectMirror.value,
      adapters: checkDetail.value?.adapters.map((obj) => obj.module_name) ?? [],
      plugins: checkDetail.value?.plugins ?? [],
      plugin_dirs: checkDetail.value?.plugin_dirs ?? [],
      builtin_plugins: checkDetail.value?.builtin_plugins ?? [],
    })
    .then((resp) => {
      logKey.value = resp.log_key;
      closeNextModal();
      logShowModal.value?.openModal();
    })
    .catch((error: AxiosError) => {
      let reason: string;
      if (error.response) {
        reason = (error.response.data as { detail: string })?.detail;
      } else {
        reason = error.message;
      }
      notice.error(`添加失败：${reason}`);
    });
};

const finishAddProject = () => {
  notice.success("添加成功");

  projectName.value = "";
  projectDir.value = "";
  projectMirror.value = "";
  checkIsPass.value = false;
  checkNoticeLevel.value = "";
  checkMsg.value = "";
  checkDetail.value = null;
};
</script>

<template>
  <dialog ref="addProjectByPathModal" class="modal">
    <div class="modal-box rounded-lg">
      <h3 class="font-bold text-lg">添加 NoneBot 实例（1/2）</h3>

      <div class="mt-4 w-full flex flex-col items-center gap-4">
        <div class="form-control w-full max-w-[75%]">
          <label class="label">
            <span class="label-text">实例位置（需绝对路径）：</span>
          </label>
          <div class="join">
            <input
              v-model="projectDir"
              type="text"
              placeholder="请键入"
              class="input input-bordered join-item w-full text-sm h-10 min-h-0"
            />
            <button
              class="join-item btn btn-outline btn-primary h-10 min-h-0"
              @click="doCheck()"
            >
              开始扫描
            </button>
          </div>

          <div class="mt-2">
            <div v-if="checkNoticeLevel === 'warning'" class="alert alert-warning">
              <WarningCircleIcon class="flex-shrink-0 h-6 w-6" />
              <div>
                <div v-for="i in checkMsg.split(',')" class="text-sm">
                  {{ i }}
                </div>
              </div>
            </div>

            <div v-if="checkNoticeLevel === 'error'" class="alert alert-error">
              <ErrorCircleIcon class="flex-shrink-0 h-6 w-6" />
              <div>{{ checkMsg }}</div>
            </div>
          </div>
        </div>

        <div v-if="checkIsPass" class="form-control w-full max-w-[75%] gap-4">
          <div v-if="checkDetail?.plugins.length">
            <label class="label">
              <span class="label-text">已扫描到的插件：</span>
            </label>
            <div class="flex flex-wrap gap-2">
              <div v-for="plugin in checkDetail?.plugins" class="badge badge-ghost gap-1">
                <CloseIcon
                  role="button"
                  class="h-4 w-4"
                  @click="
                    checkDetail.plugins = checkDetail.plugins.filter(
                      (obj) => obj !== plugin,
                    )
                  "
                />
                {{ plugin }}
              </div>
            </div>
          </div>

          <div v-if="checkDetail?.plugin_dirs.length">
            <label class="label">
              <span class="label-text">已扫描到的插件目录：</span>
            </label>
            <div class="flex flex-wrap gap-2">
              <div
                v-for="plugin_dir in checkDetail?.plugin_dirs"
                class="badge badge-ghost gap-1"
              >
                <CloseIcon
                  role="button"
                  class="h-4 w-4"
                  @click="
                    checkDetail.plugin_dirs = checkDetail.plugin_dirs.filter(
                      (obj) => obj !== plugin_dir,
                    )
                  "
                />
                {{ plugin_dir }}
              </div>
            </div>
          </div>

          <div v-if="checkDetail?.adapters.length">
            <label class="label">
              <span class="label-text">已扫描到的适配器：</span>
            </label>
            <div class="flex flex-wrap gap-2">
              <div
                v-for="adapter in checkDetail?.adapters"
                class="badge badge-ghost gap-1"
              >
                <CloseIcon
                  role="button"
                  class="h-4 w-4"
                  @click="
                    checkDetail.adapters = checkDetail.adapters.filter(
                      (obj) => obj !== adapter,
                    )
                  "
                />
                {{ adapter.name }}
              </div>
            </div>
          </div>
        </div>

        <div class="w-full max-w-[75%] text-sm">
          <div>* 如误删信息可重新扫描</div>
          <div>* 驱动器（Driver）请稍后在拓展商店中自行安装</div>
          <div>* 受 WebUI 控制的实例将强制启用虚拟环境（venv）</div>
        </div>
      </div>

      <div class="modal-action">
        <button
          class="btn rounded-lg h-10 min-h-0"
          @click="addProjectByPathModal?.close()"
        >
          取消
        </button>

        <button
          :class="{
            'btn btn-primary rounded-lg h-10 min-h-0 text-white': true,
            'btn-disabled': !checkIsPass,
          }"
          @click="addProjectByPathModal?.close(), openNextModal()"
        >
          下一步
        </button>
      </div>
    </div>
  </dialog>

  <dialog ref="addProjectByPathNextModal" class="modal">
    <div class="modal-box rounded-lg">
      <h3 class="font-bold text-lg">添加 NoneBot 实例（2/2）</h3>

      <div class="mt-4 w-full flex flex-col items-center gap4">
        <div class="form-control w-full max-w-[75%]">
          <div>
            <label class="label">
              <span class="label-text">实例名称：</span>
            </label>
            <input
              v-model="projectName"
              type="text"
              placeholder="请键入"
              class="input input-bordered w-full text-sm h-10 min-h-0"
            />
          </div>

          <div>
            <label class="label">
              <span class="label-text">Python 镜像源：</span>
            </label>
            <select
              v-model="projectMirror"
              class="select select-bordered w-full h-10 min-h-0"
            >
              <option disabled value="">请选择</option>
              <option v-for="mirror in mirrorList" :value="mirror.url">
                {{ mirror.name }}
              </option>
            </select>
          </div>
        </div>
      </div>

      <div class="modal-action">
        <button
          class="btn rounded-lg h-10 min-h-0"
          @click="closeNextModal(), addProjectByPathModal?.showModal()"
        >
          上一步
        </button>

        <button
          class="btn btn-primary rounded-lg h-10 min-h-0 text-white"
          @click="doAddProject()"
        >
          添加
        </button>
      </div>
    </div>
  </dialog>

  <LogShow
    ref="logShowModal"
    @is-retry="doAddProject"
    @is-o-k="finishAddProject"
    :log-key="logKey"
  />
</template>
