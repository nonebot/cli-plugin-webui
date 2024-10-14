<script setup lang="ts">
import router from '@/router'
import { useNoneBotStore } from '@/stores'
import { computed, ref, type ComputedRef } from 'vue'

type detailItem = {
  title: string
  details?: ComputedRef<string[]>
  editTo?: string
  key?: string
}

const store = useNoneBotStore()

const detailShowModal = ref<HTMLDialogElement>(),
  detailShowModalTitle = ref(''),
  detailShowModalContent = ref<string[]>([])

const basicItems: detailItem[] = [
  {
    title: '实例ID',
    details: computed(() => [store.selectedBot?.project_id ?? 'unknown'])
  },
  {
    title: '实例名称',
    details: computed(() => [store.selectedBot?.project_name ?? 'unknown'])
  },
  {
    title: '实例路径',
    details: computed(() => [store.selectedBot?.project_dir ?? 'unknown'])
  },
  {
    title: '实例 Python 镜像',
    details: computed(() => [store.selectedBot?.mirror_url ?? 'unknown'])
  }
]

const installedItems: detailItem[] = [
  {
    key: 'adapter',
    title: '已安装适配器',
    details: computed(() => store.selectedBot?.adapters.map((adapter) => adapter.name) ?? []),
    editTo: 'adapters'
  },
  {
    key: 'driver',
    title: '已安装驱动',
    details: computed(() => store.selectedBot?.drivers.map((driver) => driver.name) ?? []),
    editTo: 'drivers'
  },
  {
    key: 'plugin',
    title: '已安装插件',
    details: computed(() => store.selectedBot?.plugins.map((plugin) => plugin.name) ?? []),
    editTo: 'plugins'
  }
]

const openModal = (key: string) => {
  const target = installedItems.find((item) => item.key === key)
  detailShowModalTitle.value = target?.title ?? ''
  detailShowModalContent.value = target?.details?.value ?? []
  detailShowModal.value?.showModal()
}
</script>

<template>
  <dialog ref="detailShowModal" class="modal">
    <div class="modal-box rounded-lg flex flex-col gap-4">
      <h3 class="font-semibold text-lg">{{ detailShowModalTitle }}详细</h3>

      <div class="flex flex-wrap gap-2">
        <div v-for="d in detailShowModalContent" :key="d" class="badge badge-ghost">
          {{ d }}
        </div>
        <div v-if="!detailShowModalContent.length">暂无数据</div>
      </div>

      <div class="flex justify-between">
        <div class="flex items-center gap-2">
          <button
            class="btn btn-sm btn-primary font-normal text-base-100"
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
    <div class="w-full p-6 bg-base-200 rounded-box">
      <div class="overflow-x-auto">
        <table class="table table-sm">
          <tbody>
            <tr v-for="item in basicItems" :key="item.title">
              <td class="pl-0 text-base font-semibold">{{ item.title }}</td>
              <td>{{ item.details?.value[0] }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="w-full p-6 bg-base-200 rounded-box">
      <table class="table">
        <tbody>
          <tr v-for="item in installedItems" :key="item.title">
            <td class="pl-0 text-base font-semibold">{{ item.title }}</td>
            <td>
              <div class="badge">{{ item.details?.value.length }} 个</div>
            </td>
            <td class="flex justify-end pr-0">
              <button class="btn btn-sm btn-ghost" @click="openModal(item.key!)">详细</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
