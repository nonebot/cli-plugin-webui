<script setup lang="ts">
import { ref } from 'vue'
import { useNoneBotStore } from '@/stores'
import Drawer from '@/components/Drawer.vue'
import CreateBotIndex from '@/components/Modals/CreateBot/CreateBotIndex.vue'

const store = useNoneBotStore()

const createBotModal = ref<InstanceType<typeof CreateBotIndex> | null>(null)
const drawerRef = ref<InstanceType<typeof Drawer> | null>(null)
</script>

<template>
  <CreateBotIndex ref="createBotModal" />

  <Drawer ref="drawerRef">
    <template v-slot:button>
      <button class="btn btn-sm btn-ghost btn-square" @click="drawerRef?.showDrawer()">
        <span class="material-symbols-outlined"> robot_2 </span>
      </button>
    </template>

    <template v-slot:drawer-title>实例选择</template>

    <template v-slot:drawer-body>
      <div v-if="store.getExtendedBotsList().length" class="grid gap-2">
        <div
          v-for="bot in store.getExtendedBotsList()"
          :key="bot.project_id"
          role="button"
          class="flex items-center justify-between gap-4 transition bg-base-200/50 hover:bg-base-200 rounded-lg p-4"
          @click="store.selectBot(bot)"
        >
          <div class="shrink-0 flex items-center">
            <span class="material-symbols-outlined text-4xl"> deployed_code </span>
          </div>
          <div class="w-full">
            {{ bot.project_name }}
            <div class="text-xs opacity-50">{{ bot.project_id }}</div>
          </div>
          <div class="shrink-0 flex gap-2">
            <div
              v-if="store.selectedBot?.project_id === bot.project_id"
              class="badge bg-blue-400 text-white"
            >
              选择中
            </div>
            <div v-if="bot.is_running" class="badge badge-success text-white">运行中</div>
          </div>
        </div>
      </div>
      <div v-else class="flex justify-center items-center">
        <div class="flex flex-col items-center gap-4">
          暂无实例
          <div class="flex gap-4">
            <button
              class="btn btn-md lg:btn-sm btn-primary font-normal text-white"
              @click="createBotModal?.openModal()"
            >
              创建一个
            </button>
            <button class="btn btn-md lg:btn-sm btn-outline btn-primary font-normal">
              添加一个
            </button>
          </div>
        </div>
      </div>
    </template>
  </Drawer>
</template>

<style scoped>
.material-symbols-outlined {
  font-variation-settings:
    'FILL' 0,
    'wght' 400,
    'GRAD' -25,
    'opsz' 48;
}
</style>
