<script setup lang="ts">
import FolderSelect from "@/components/HomePage/FolderSelect.vue";
import LogViewCard from "../Cards/LogViewCard.vue";
import { API } from "@/api";
import { globalLog as log } from "@/main";
import { Driver, Adapter } from "@/api/models";
import { onMounted, ref } from "vue";

const mirrorList = [
  { name: "PyPI", url: "https://pypi.org/simple" },
  {
    name: "校园网联合镜像站",
    url: "https://mirrors.cernet.edu.cn/pypi/web/simple",
  },
  { name: "清华大学", url: "https://pypi.tuna.tsinghua.edu.cn/simple" },
  {
    name: "北京外国语大学",
    url: "https://mirrors.bfsu.edu.cn/pypi/web/simple",
  },
  { name: "腾讯云", url: "https://mirrors.cloud.tencent.com/pypi/simple" },
  { name: "中科院", url: "https://pypi.mirrors.ustc.edu.cn/simple" },
  { name: "豆瓣", url: "https://pypi.douban.com/simple" },
];
const driverList = ref([] as Driver[]);
const adapterList = ref([] as Adapter[]);
const projectName = ref("");
const projectFolder = ref("");
const projectMirror = ref("");
const projectDriver = ref(Object() as Driver);
const projectAdapter = ref(Object() as Adapter);
const logKey = ref("");

const api = new API();

const getDrivers = async () => {
  try {
    const resp = await api.getDrivers();
    driverList.value = resp.drivers;
  } catch (error) {
    log.error(`获取驱动器列表失败：${error}`);
    return;
  }
};

const getAdapters = async () => {
  try {
    const resp = await api.getAdapters();
    adapterList.value = resp.adapters;
  } catch (error) {
    log.error(`获取适配器列表失败：${error}`);
    return;
  }
};

const selectedFolder = (data: string) => {
  projectFolder.value = data;
};

const isRetry = (data: boolean) => {
  if (data) {
    doCreate();
  }
};

const isClear = (data: boolean) => {
  if (data) {
    projectName.value = "";
    projectFolder.value = "";
    projectMirror.value = "";
    projectDriver.value = Object();
    projectAdapter.value = Object();
    logKey.value = "";
  }
};

const doCheck = () => {
  try {
    if (projectName.value === "") {
      throw new Error("缺少实例名称");
    }
    if (projectFolder.value === "") {
      throw new Error("缺少实例路径");
    }
    if (projectMirror.value === "") {
      throw new Error("缺少镜像源");
    }
    if (projectDriver.value === Object()) {
      throw new Error("缺少驱动器");
    }
    if (projectAdapter.value === Object()) {
      throw new Error("缺少适配器");
    }
  } catch (error) {
    log.warning(`检查未通过：${error}`);
    throw error;
  }
};

const doCreate = async () => {
  try {
    const resp = await api.createProject({
      project_name: projectName.value,
      project_dir: projectFolder.value.replace("(实例名称)", ""),
      mirror_url: projectMirror.value,
      driver: projectDriver.value,
      adapter: projectAdapter.value,
    });
    logKey.value = resp.log_key;
  } catch (error) {
    log.error(`初始化项目失败：${error}`);
    return;
  }
};

getDrivers();
getAdapters();

onMounted(() => {
  const create = document.getElementById("doCreate")!;
  create.addEventListener("click", (event) => {
    event.preventDefault();

    try {
      doCheck();
    } catch (error) {
      return;
    }
    doCreate();

    window.location.href = create.getAttribute("href")!;
  });
});
</script>

<template>
  <FolderSelect @onSelectedFolder="selectedFolder" />
  <LogViewCard @is-retry="isRetry" @is-o-k="isClear" :logKey="logKey" />

  <div class="modal" id="create-nonebot-user">
    <div class="modal-box rounded-lg">
      <h3 class="font-bold text-lg">创建 NoneBot 实例</h3>

      <div class="mt-4 w-full flex flex-col items-center">
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
          <a
            href="#folder-select"
            class="btn btn-outline btn-primary rounded-lg h-10 min-h-0"
            >选择文件夹</a
          >
          <label class="label">
            <span class="label-text overflow-x-auto text-xs">
              (Base Dir)\{{ projectFolder.replace("(实例名称)", projectName) }}
            </span>
          </label>
        </div>

        <div class="form-control w-full max-w-[75%]">
          <label class="label">
            <span class="label-text">Python 镜像源</span>
          </label>
          <select v-model="projectMirror" class="select select-bordered">
            <option v-for="mirror in mirrorList" :value="mirror.url">
              {{ mirror.name }}
            </option>
          </select>
        </div>

        <div class="form-control w-full max-w-[75%]">
          <label class="label">
            <span class="label-text">驱动器</span>
          </label>
          <select v-model="projectDriver" class="select select-bordered">
            <option v-for="driver in driverList" :value="driver">
              {{ driver.name }} - {{ driver.desc }}
            </option>
          </select>
        </div>

        <div class="form-control w-full max-w-[75%]">
          <label class="label">
            <span class="label-text">适配器</span>
          </label>
          <select v-model="projectAdapter" class="select select-bordered">
            <option v-for="adapter in adapterList" :value="adapter">
              {{ adapter.name }} - {{ adapter.desc }}
            </option>
          </select>
        </div>
      </div>

      <div class="modal-action">
        <a href="#" class="btn rounded-lg h-10 min-h-0" @click="isClear(true)"
          >取消</a
        >
        <a
          id="doCreate"
          href="#log-view"
          class="btn btn-primary rounded-lg h-10 min-h-0 text-white"
          >创建</a
        >
      </div>
    </div>
  </div>
</template>
