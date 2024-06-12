<script setup lang="ts">
import router from '@/router'
import { useNoneBotStore } from '@/stores'
import { computed, ref, type ComputedRef } from 'vue'

type detailItem = {
  t: string
  title: string
  details: ComputedRef<string[]>
  editTo: string
}

const store = useNoneBotStore()

const detailShowModal = ref<HTMLDialogElement>(),
  detailShowModalTitle = ref(''),
  detailShowModalContent = ref<string[]>([])

const items: detailItem[] = [
  {
    t: 'adapter',
    title: '已安装适配器',
    details: computed(() => store.selectedBot?.adapters.map((adapter) => adapter.name) ?? []),
    editTo: 'adapters'
  },
  {
    t: 'driver',
    title: '已安装驱动',
    details: computed(() => store.selectedBot?.drivers.map((driver) => driver.name) ?? []),
    editTo: 'drivers'
  },
  {
    t: 'plugin',
    title: '已安装插件',
    details: computed(() => store.selectedBot?.plugins.map((plugin) => plugin.name) ?? []),
    editTo: 'plugins'
  }
]

const openModal = (t: string) => {
  const target = items.find((item) => item.t === t)
  detailShowModalTitle.value = target?.title ?? ''
  detailShowModalContent.value = target?.details.value ?? []
  detailShowModal.value?.showModal()
}
</script>

<template>
  <dialog ref="detailShowModal" class="modal">
    <div class="modal-box rounded-lg flex flex-col gap-4">
      <h3 class="font-semibold text-lg">{{ detailShowModalTitle }}详细</h3>

      <div class="flex flex-wrap gap-2">
        <div
          v-if="detailShowModalContent.length > 0"
          v-for="d in detailShowModalContent"
          class="badge badge-ghost"
        >
          {{ d }}
        </div>
        <div v-else>暂无数据</div>
      </div>

      <div class="flex justify-between">
        <div class="flex items-center gap-2">
          <button
            class="btn btn-sm btn-primary font-normal text-white"
            @click="router.push('/store'), detailShowModal?.close()"
          >
            管理
          </button>
        </div>

        <div class="flex items-center gap-2">
          <button class="btn btn-sm btn-ghost" @click="detailShowModal?.close()">关闭</button>
        </div>
      </div>
    </div>
  </dialog>

  <div class="grid gap-4 grid-cols-1 xl:grid-cols-2">
    <div class="w-full p-6 bg-base-200 rounded-box flex items-center justify-center">
      <table class="table">
        <tbody>
          <tr>
            <th class="pl-0">实例ID</th>
            <td>{{ store.selectedBot?.project_id }}</td>
          </tr>
          <tr>
            <th class="pl-0">实例名称</th>
            <td>{{ store.selectedBot?.project_name }}</td>
          </tr>
          <tr>
            <th class="pl-0">实例路径</th>
            <td>{{ store.selectedBot?.project_dir }}</td>
          </tr>
          <tr>
            <th class="pl-0">实例 Python 镜像</th>
            <td>{{ store.selectedBot?.mirror_url }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="w-full p-6 bg-base-200 rounded-box flex items-center justify-center">
      <table class="table">
        <tbody>
          <tr v-for="item in items">
            <th class="pl-0">{{ item.title }}</th>
            <td>
              <div class="badge">{{ item.details.value.length }} 个</div>
            </td>
            <td class="flex justify-end pr-0">
              <button class="btn btn-sm btn-ghost" @click="openModal(item.t)">详细</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
