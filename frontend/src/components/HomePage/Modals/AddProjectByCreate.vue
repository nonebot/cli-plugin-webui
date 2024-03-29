<script setup lang="ts">
import LogShow from "@/components/CustomModal/LogShow.vue";
import FolderSelect from "@/components/HomePage/Modals/FolderSelect.vue";

import { notice } from "@/utils/notification";
import { Driver, Adapter } from "@/api/schemas";
import { onMounted, ref, watch } from "vue";
import { mirrorList, getProjectList } from "../client";
import type { AxiosError } from "axios";
import api from "@/api";

const addProjectByCreateModal = ref<HTMLDialogElement>();

defineExpose({
  openModal: () => {
    addProjectByCreateModal.value?.showModal();
  },
  closeModal: () => {
    addProjectByCreateModal.value?.close();
  },
});

const logShowModal = ref<InstanceType<typeof LogShow> | null>();
const folderSelectModal = ref<InstanceType<typeof FolderSelect> | null>();

const driverList = ref<Driver[]>([]);
const adapterList = ref<Adapter[]>([]);

const projectIsBootstrap = ref(true);
const projectName = ref("");
const projectFolder = ref("");
const projectMirror = ref("");
const projectDriver = ref<Driver[]>([]);
const projectAdapter = ref<Adapter[]>([]);
const projectUseSrc = ref(false);

const logKey = ref("");
const doCreateButton = ref<HTMLElement>();
const selectedDriver = ref<Driver>();
const selectedAdapter = ref<Adapter>();
const selectedDriverList = ref<Driver[]>([]);
const selectedAdapterList = ref<Adapter[]>([]);

const getDrivers = async () => {
  await api
    .getNoneBotModules("driver", 0, "", false, true)
    .then((resp) => {
      driverList.value = resp.data.detail;
    })
    .catch((error: AxiosError) => {
      let reason: string;
      if (error.response) {
        reason = (error.response.data as { detail: string })?.detail;
      } else {
        reason = error.message;
      }
      notice.error(`获取驱动器列表失败：${reason}`);
    });
};

const getAdapters = async () => {
  await api
    .getNoneBotModules("adapter", 0, "", false, true)
    .then((resp) => {
      adapterList.value = resp.data.detail;
    })
    .catch((error: AxiosError) => {
      let reason: string;
      if (error.response) {
        reason = (error.response.data as { detail: string })?.detail;
      } else {
        reason = error.message;
      }
      notice.error(`获取驱动器列表失败：${reason}`);
    });
};

const selectedFolder = (data: string) => {
  projectFolder.value = data;
  addProjectByCreateModal.value?.showModal();
};

const isRetry = async (data: boolean) => {
  if (data) {
    await doCreate();
  }
};

const allDone = async (data: boolean) => {
  if (data) {
    await getProjectList();
    notice.success("添加成功");
  }
  projectIsBootstrap.value = true;
  projectName.value = "";
  projectFolder.value = "";
  projectMirror.value = "";
  projectDriver.value = [];
  projectAdapter.value = [];
  projectUseSrc.value = false;
  logKey.value = "";
};

const doCheck = () => {
  try {
    if (!projectName.value) {
      throw new Error("缺少实例名称");
    }
    if (!projectMirror.value) {
      throw new Error("缺少镜像源");
    }
    if (!projectDriver.value.length) {
      throw new Error("缺少驱动器");
    }
    if (!projectAdapter.value.length) {
      throw new Error("缺少适配器");
    }
  } catch (error) {
    notice.warning(`检查未通过：${error}`);
    throw error;
  }
};

const doCreate = async () => {
  await api
    .createProject({
      is_bootstrap: projectIsBootstrap.value,
      project_name: projectName.value,
      project_dir: projectFolder.value,
      mirror_url: projectMirror.value,
      drivers: projectDriver.value,
      adapters: projectAdapter.value,
      use_src: projectUseSrc.value,
    })
    .then((resp) => {
      logKey.value = resp.data.detail;
    })
    .catch((error: AxiosError) => {
      let reason: string;
      if (error.response) {
        reason = (error.response.data as { detail: string })?.detail;
      } else {
        reason = error.message;
      }
      notice.error(`创建项目失败：${reason}`);
    });
};

const selectDriver = (driver: Driver) => {
  if (projectDriver.value.includes(driver)) {
    const change = projectDriver.value.filter((obj) => obj !== driver);
    projectDriver.value = change;
    selectedDriverList.value = change;
  } else {
    projectDriver.value.push(driver);
    selectedDriverList.value.push(driver);
  }
};

interface SelectDriver {
  selected: boolean;
  driver: Driver;
}

const genSelectDriverList = () => {
  let result: SelectDriver[] = [];
  for (const driver of driverList.value) {
    if (projectDriver.value.includes(driver)) {
      result.push({ selected: true, driver: driver });
    } else {
      result.push({ selected: false, driver: driver });
    }
  }
  return result;
};

const selectAdapter = (adapter: Adapter) => {
  if (projectAdapter.value.includes(adapter)) {
    const change = projectAdapter.value.filter((obj) => obj !== adapter);
    projectAdapter.value = change;
    selectedAdapterList.value = change;
  } else {
    projectAdapter.value.push(adapter);
    selectedAdapterList.value?.push(adapter);
  }
};

interface SelectAdapter {
  selected: boolean;
  adapter: Adapter;
}

const genSelectAdapterList = () => {
  let result: SelectAdapter[] = [];
  for (const adapter of adapterList.value) {
    if (projectAdapter.value.includes(adapter)) {
      result.push({ selected: true, adapter: adapter });
    } else {
      result.push({ selected: false, adapter: adapter });
    }
  }
  return result;
};

onMounted(() => {
  const create = doCreateButton.value!;
  create.addEventListener("click", () => {
    try {
      doCheck();
    } catch (error) {
      return;
    }
    doCreate();

    addProjectByCreateModal.value?.close();
    logShowModal.value?.openModal();
  });
});

watch(addProjectByCreateModal, async (newValue) => {
  if (newValue) {
    await getDrivers();
    await getAdapters();
  }
});
</script>

<template>
  <dialog ref="addProjectByCreateModal" class="modal">
    <div class="modal-box rounded-lg flex flex-col flex-nowrap">
      <h3 class="font-bold text-lg">创建 NoneBot 实例</h3>

      <div
        class="mt-4 w-full flex flex-col items-center overflow-y-auto custom-y-scrollbar"
      >
        <div class="form-control w-full max-w-[75%]">
          <label class="label">
            <span class="label-text">要使用的模板</span>
          </label>
          <label class="label cursor-pointer">
            <span class="label-text">bootstrap （初学者或用户）</span>
            <input
              type="radio"
              name="radio-1"
              class="radio radio-sm checked:bg-primary"
              @click="projectIsBootstrap = true"
            />
          </label>
          <label class="label cursor-pointer">
            <span class="label-text">simple （插件开发者）</span>
            <input
              type="radio"
              name="radio-1"
              class="radio radio-sm checked:bg-blue-500"
              @click="projectIsBootstrap = false"
            />
          </label>
        </div>

        <div class="form-control w-full max-w-[75%]">
          <label class="label">
            <span class="label-text">实例名称</span>
          </label>
          <input
            v-model="projectName"
            type="text"
            placeholder="请键入"
            class="input input-bordered w-full text-sm"
          />
        </div>

        <div class="form-control w-full max-w-[75%]">
          <label class="label">
            <span class="label-text">实例绝对路径</span>
          </label>
          <button
            class="btn btn-outline btn-primary rounded-lg h-10 min-h-0"
            @click="folderSelectModal?.openModal()"
          >
            选择文件夹
          </button>
          <label class="label">
            <span class="label-text overflow-x-auto text-xs">
              (Base Dir)/{{ projectFolder }}{{ projectFolder === "" ? projectFolder : "/"
              }}{{ projectName }}
            </span>
          </label>
        </div>

        <div class="form-control w-full max-w-[75%]">
          <label class="label">
            <span class="label-text">Python 镜像源</span>
          </label>
          <select v-model="projectMirror" class="select select-bordered">
            <option disabled value="">请选择</option>
            <option v-for="mirror in mirrorList" :value="mirror.url">
              {{ mirror.name }}
            </option>
          </select>
        </div>

        <div class="form-control w-full max-w-[75%]">
          <label class="label">
            <span class="label-text">
              驱动器
              <div class="badge badge-ghost">已选：{{ projectDriver.length }} 个</div>
            </span>
          </label>
          <select
            class="select select-bordered"
            v-model="selectedDriver"
            @change="selectDriver(selectedDriver!)"
          >
            <option disabled value="">请选择</option>
            <option v-for="item in genSelectDriverList()" :value="item.driver">
              <div v-if="item.selected">√&nbsp;</div>
              <div v-else>&nbsp;</div>
              {{ item.driver.name }} - {{ item.driver.desc }}
            </option>
          </select>
        </div>

        <div class="form-control w-full max-w-[75%]">
          <label class="label">
            <span class="label-text">
              适配器
              <div class="badge badge-ghost">已选：{{ projectAdapter.length }} 个</div>
            </span>
          </label>
          <select
            class="select select-bordered"
            v-model="selectedAdapter"
            @change="selectAdapter(selectedAdapter!)"
          >
            <option disabled value="">请选择</option>
            <option v-for="item in genSelectAdapterList()" :value="item.adapter">
              <div v-if="item.selected">√&nbsp;</div>
              <div v-else>&nbsp;</div>
              {{ item.adapter.name }} - {{ item.adapter.desc }}
            </option>
          </select>
        </div>

        <div v-if="!projectIsBootstrap" class="form-control w-full max-w-[75%]">
          <label class="label">
            <span class="label-text">插件存储位置</span>
          </label>
          <label class="label cursor-pointer">
            <span class="label-text">
              在 {{ projectName ? projectName : "ignore" }} 中
            </span>
            <input
              type="radio"
              name="radio-2"
              class="radio radio-sm checked:bg-primary"
              @click="projectUseSrc = false"
            />
          </label>
          <label class="label cursor-pointer">
            <span class="label-text">在 src 中</span>
            <input
              type="radio"
              name="radio-2"
              class="radio radio-sm checked:bg-blue-500"
              @click="projectUseSrc = true"
            />
          </label>
        </div>
      </div>

      <div class="modal-action">
        <button
          class="btn rounded-lg h-10 min-h-0"
          @click="allDone(false), addProjectByCreateModal?.close()"
        >
          取消
        </button>

        <button
          ref="doCreateButton"
          class="btn btn-primary rounded-lg h-10 min-h-0 text-white"
        >
          创建
        </button>
      </div>
    </div>
  </dialog>

  <FolderSelect ref="folderSelectModal" @onSelectedFolder="selectedFolder" />
  <LogShow ref="logShowModal" @is-retry="isRetry" @is-o-k="allDone" :logKey="logKey" />
</template>
