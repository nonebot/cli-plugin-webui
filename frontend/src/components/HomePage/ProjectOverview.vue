<script setup lang="ts">
import AddProjectChoice from "@/components/HomePage/Modals/AddProjectChoice.vue";

import { API } from "@/api";
import { NonebotProjectMeta } from "@/api/models";
import { globalLog as log } from "@/main";
import { appStore as store } from "@/store/global";
import { parseSimpleInfo } from "@/utils";
import { ref } from "vue";

const addProjectChoiceModal = ref<InstanceType<
  typeof AddProjectChoice
> | null>();

const choiceProjectInfo = ref<NonebotProjectMeta>();

const api = new API();

const choiceProject = (data: NonebotProjectMeta) => {
  store().choiceProject = data;
  choiceProjectInfo.value = data;
};

const getProjectList = async () => {
  try {
    const resp = await api.getProjectList();
    store().projectList = resp.projects;
  } catch (error) {
    log.error(`获取实例列表失败：${error}`);
    return;
  }
};

getProjectList();
</script>

<template>
  <AddProjectChoice ref="addProjectChoiceModal" />

  <Transition>
    <div
      v-if="store().projectList"
      class="p-4 md:p-6 rounded shadow-none md:shadow-lg bg-base-200 !mb-0 sm:m-8 md:m-12 lg:m-16 xl:m-20 2xl:m-28"
    >
      <div class="flex justify-between items-center">
        <h3 class="xs:text-base md:text-xl">实例概览</h3>

        <div class="grid grid-cols-2 gap-4">
          <button
            class="btn btn-xs md:btn-sm h-auto md:!h-10 rounded-lg"
            @click="getProjectList()"
          >
            刷新
          </button>

          <button
            class="btn btn-xs md:btn-sm h-auto md:!h-10 btn-primary rounded-lg text-white"
            @click="addProjectChoiceModal?.openModal()"
          >
            添加实例
          </button>
        </div>
      </div>

      <div class="overflow-x-auto custom-x-scrollbar">
        <table id="project-list" class="table table-sm mt-2">
          <thead>
            <tr>
              <th>实例 ID</th>
              <th>实例名称</th>
              <th>驱动器</th>
              <th>适配器</th>
              <th>状态</th>
            </tr>
          </thead>
          <tbody>
            <tr
              role="button"
              v-for="project in store().projectList"
              :key="project.project_id"
              :class="{
                'hover:hover:bg-[hsl(var(--bc)/0.1)] duration-150 hover:ease-in-out': true,
                'bg-[hsl(var(--bc)/0.1)]':
                  store().choiceProject.project_id === project.project_id,
              }"
              @click="choiceProject(project)"
            >
              <th class="w-40">{{ project.project_id }}</th>
              <th>{{ project.project_name }}</th>
              <td>{{ parseSimpleInfo(project.drivers) }}</td>
              <td>{{ parseSimpleInfo(project.adapters) }}</td>
              <td>
                <div class="flex items-center">
                  <div
                    v-if="project.is_running"
                    class="badge badge-success badge-sm"
                  ></div>
                  <div v-else class="badge badge-error badge-sm"></div>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </Transition>
</template>

<style>
#project-list th,
#project-list td {
  white-space: nowrap;
}
</style>
