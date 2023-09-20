<script setup lang="ts">
import { parseStringArray, parseSimpleInfo } from "@/utils";
import { appStore as store } from "@/store/global";
import { ref } from "vue";

const checkPluginModal = ref<HTMLDialogElement>();
const pluginList = ref<string[]>();

const parseString = (data: string) => {
  return data ? data : "unknown";
};

const genPluginList = () => {
  checkPluginModal.value?.showModal();
  pluginList.value = store().choiceProject.plugins.map((obj) => obj.module_name);
};
</script>

<template>
  <dialog ref="checkPluginModal" class="modal">
    <div class="modal-box rounded-lg">
      <h3 class="font-bold text-lg">已安装的插件</h3>
      <p class="py-4">
        {{ pluginList?.join("、") }}
      </p>
      <div class="modal-action">
        <button class="btn rounded-lg h-10 min-h-0" @click="checkPluginModal?.close()">
          关闭
        </button>
      </div>
    </div>
    <form method="dialog" class="modal-backdrop">
      <button>close</button>
    </form>
  </dialog>

  <div
    :class="{
      'overflow-hidden relative w-full p-4 md:p-6 rounded shadow-none md:shadow-lg bg-base-200': true,
      hidden: !store().choiceProject.project_id,
    }"
  >
    <h3 class="xs:text-base md:text-xl">实例信息</h3>

    <Transition>
      <div
        v-if="store().choiceProject.project_id"
        class="overflow-x-auto custom-x-scrollbar"
      >
        <table id="project-profile" class="table table-sm w-full mt-2">
          <tbody>
            <tr>
              <th class="w-30">实例 ID</th>
              <td>{{ parseString(store().choiceProject.project_id) }}</td>
            </tr>
            <tr>
              <th>实例名称</th>
              <td>
                {{ parseString(store().choiceProject.project_name) }}
              </td>
            </tr>
            <tr>
              <th>实例路径</th>
              <td>
                {{ parseString(store().choiceProject.project_dir) }}
              </td>
            </tr>
            <tr>
              <th>PIP 镜像</th>
              <td>{{ parseString(store().choiceProject.mirror_url) }}</td>
            </tr>
            <tr>
              <th>适配器</th>
              <td>
                {{ parseSimpleInfo(store().choiceProject.adapters) }}
              </td>
            </tr>
            <tr>
              <th>驱动器</th>
              <td>
                {{ parseSimpleInfo(store().choiceProject.drivers) }}
              </td>
            </tr>
            <tr>
              <th>插件列表</th>
              <td>
                <div
                  v-if="store().choiceProject.plugins.length >= 2"
                  class="tooltip"
                  data-tip="点击查看列表"
                  @click="genPluginList()"
                >
                  {{
                    parseStringArray(
                      store()
                        .choiceProject.plugins.map((obj) => obj.module_name)
                        .slice(0, 2),
                    )
                  }}
                  ...
                </div>
                <div v-else>
                  {{
                    parseStringArray(
                      store().choiceProject.plugins.map((obj) => obj.module_name),
                    )
                  }}
                </div>
              </td>
            </tr>
            <tr>
              <th>插件读取路径</th>
              <td>
                <tbody>
                  <tr v-if="store().choiceProject.plugin_dirs.length == 0">
                    <td class="p-0">unknown</td>
                  </tr>
                  <tr v-for="dir in store().choiceProject.plugin_dirs">
                    <td class="p-0 pt-1">{{ parseString(dir) }}</td>
                  </tr>
                </tbody>
              </td>
            </tr>
            <tr>
              <th>内置插件</th>
              <td>
                {{ parseStringArray(store().choiceProject.builtin_plugins) }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </Transition>
  </div>
</template>

<style scoped>
#project-profile th,
#project-profile td {
  white-space: nowrap;
}
</style>
