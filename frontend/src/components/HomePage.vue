<script setup lang="ts">
import CreateNonebotCustom from "@/components/HomePage/CreateNonebotCustom.vue";
import CreateNonebotForUser from "@/components/HomePage/CreateNonebotForUser.vue";

import { API } from "@/api";
import { NonebotProjectMeta } from "@/api/models";
import { globalLog as log } from "@/main";
import { globalStore } from "@/store/app";
import { ref } from "vue";

globalStore().nowPageName = "Home";

const projectList = ref(Object() as { [key: string]: NonebotProjectMeta });

const api = new API();

const getProjectList = async () => {
  try {
    const resp = await api.getProjectList();
    projectList.value = resp.projects;
  } catch (error) {
    log.error(`获取实例列表失败：${error}`);
    return;
  }
};

const deleteProject = async (project_id: string) => {
  try {
    await api.deleteProject(project_id);
  } catch (error) {
    log.error(`删除操作失败：${error}`);
    return;
  }
  globalStore().choiceProjectID = "";
};

const choiceProject = (data: string) => {
  globalStore().choiceProjectID = data;
};

getProjectList();
</script>

<template>
  <div class="lg:p-16 sm:p-8">
    <div class="w-full">
      <div class="w-full tracking-tight font-light">
        <p class="text-lg">欢迎使用</p>
        <div class="mt-2 mb-2 lg:text-8xl sm:text-6xl text-6xl">
          <span class="main-word">N</span>one<span class="main-word">B</span>ot
        </div>
        <p class="text-lg">跨平台 PYTHON 异步机器人框架</p>
      </div>
    </div>

    <div class="mt-8">
      链接
      <div class="flex flex-col font-light w-fit">
        <a
          class="link link-hover text-sm leading-8"
          href="https://v2.nonebot.dev"
          >NoneBot2 官网</a
        >
        <a
          class="link link-hover text-sm leading-8"
          href="https://github.com/nonebot/nonebot2"
          >NoneBot2 GitHub 仓库</a
        >
      </div>
    </div>
  </div>

  <div class="lg:pr-16 lg:pl-16 sm:pr-8 sm:pl-8">
    <CreateNonebotCustom />
    <CreateNonebotForUser />

    <div class="nonebot-list p-6 rounded shadow-lg">
      <div class="flex justify-between items-center">
        <h3 class="text-xl">NoneBot 实例管理</h3>
        <a
          href="#create-nonebot"
          class="btn btn-primary rounded-lg h-10 min-h-0 text-white"
          >添加实例</a
        >
      </div>

      <div class="overflow-x-auto">
        <table class="table table-sm w-full mt-2">
          <thead>
            <tr>
              <th>实例 ID</th>
              <th>实例名称</th>
              <th>驱动器</th>
              <th>适配器</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody class="transition">
            <tr
              v-for="project in projectList"
              :key="project.project_id"
              class="hover:bg-neutral-content duration-150 hover:ease-in-out"
              @click="choiceProject(project.project_id)"
            >
              <th class="w-40">
                {{ project.project_id }}
                <div
                  v-if="globalStore().choiceProjectID === project.project_id"
                  class="badge badge-primary badge-outline"
                >
                  选择中
                </div>
              </th>
              <th>{{ project.project_name }}</th>
              <td>{{ project.drivers.map((item) => item.name).join("、") }}</td>
              <td>
                {{ project.adapters.map((item) => item.name).join("、") }}
              </td>
              <td>
                <div class="flex items-center">
                  <label class="swap">
                    <input type="checkbox" />
                    <svg
                      class="swap-on fill-current"
                      xmlns="http://www.w3.org/2000/svg"
                      width="24"
                      height="24"
                      viewBox="0 0 24 24"
                    >
                      <title>启动</title>
                      <path d="M14,19H18V5H14M6,19H10V5H6V19Z" />
                    </svg>
                    <svg
                      class="swap-off fill-current"
                      xmlns="http://www.w3.org/2000/svg"
                      width="24"
                      height="24"
                      viewBox="0 0 24 24"
                    >
                      <title>终止运行</title>
                      <path d="M8,5.14V19.14L19,12.14L8,5.14Z" />
                    </svg>
                  </label>

                  <label class="swap mr-2">
                    <input type="checkbox" />
                    <svg
                      class="swap-on fill-current"
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 24 24"
                      width="24"
                      height="24"
                    >
                      <title>删除实例</title>
                      <path
                        d="M21,7L9,19L3.5,13.5L4.91,12.09L9,16.17L19.59,5.59L21,7Z"
                      />
                    </svg>
                    <svg
                      class="swap-off fill-current"
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 24 24"
                      width="24"
                      height="24"
                      @click="
                        deleteProject(project.project_id), getProjectList()
                      "
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
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<style>
.nonebot-list {
  background-color: hsl(var(--b2));
}

.main-word {
  color: hsl(var(--p));
}
</style>
