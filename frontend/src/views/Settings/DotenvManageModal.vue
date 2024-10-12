<script setup lang="ts">
import { ProjectService } from '@/client/api'
import { useNoneBotStore, useToastStore } from '@/stores'
import { ref } from 'vue'

const dotenvManageModal = ref<HTMLDialogElement>()

defineExpose({
  openModal: () => {
    dotenvManageModal.value?.showModal()
    getDotenvList()
  },
  closeModal: () => dotenvManageModal.value?.close()
})

const nonebotStore = useNoneBotStore()
const toast = useToastStore()

const dotenvList = ref<string[]>([])
const isAddEnv = ref(false)
const inputValue = ref()

const getDotenvList = async () => {
  if (!nonebotStore.selectedBot) {
    toast.add('warning', '未选择实例', '', 5000)
    return
  }
  const { data, error } = await ProjectService.getProjectEnvListV1ProjectConfigEnvListGet({
    query: {
      project_id: nonebotStore.selectedBot.project_id
    }
  })

  if (error) {
    toast.add('error', `获取环境失败, 原因：${error.detail?.toString()}`, '', 5000)
  }

  if (data) {
    dotenvList.value = data.detail
  }
}

const addEnv = async () => {
  if (!inputValue.value) {
    toast.add('warning', '请输入环境名称', '', 5000)
    return
  }

  if (!nonebotStore.selectedBot) {
    toast.add('warning', '未选择实例', '', 5000)
    return
  }

  const { data, error } = await ProjectService.createProjectEnvV1ProjectConfigEnvCreatePost({
    query: {
      env: inputValue.value,
      project_id: nonebotStore.selectedBot.project_id
    }
  })

  if (error) {
    toast.add('error', `添加环境失败, 原因：${error.detail?.toString()}`, '', 5000)
  }

  if (data) {
    dotenvList.value.push(inputValue.value)
    cancel()
  }
}

const removeEnv = async (env: string) => {
  if (!nonebotStore.selectedBot) {
    toast.add('warning', '未选择实例', '', 5000)
    return
  }

  const { data, error } = await ProjectService.deleteProjectEnvV1ProjectConfigEnvDeleteDelete({
    query: {
      env: env,
      project_id: nonebotStore.selectedBot.project_id
    }
  })

  if (error) {
    toast.add('error', `删除环境失败, 原因：${error.detail?.toString()}`, '', 5000)
  }

  if (data) {
    await getDotenvList()
    await nonebotStore.updateEnv(dotenvList.value[0])
  }
}

const cancel = () => {
  isAddEnv.value = false
  inputValue.value = ''
}
</script>

<template>
  <dialog ref="dotenvManageModal" class="modal" @close="cancel()">
    <div class="modal-box w-11/12 max-5-xl rounded-xl flex flex-col gap-4">
      <h3 class="font-semibold text-lg">Dotenv 管理</h3>

      <table class="table table-sm">
        <thead>
          <tr class="border-b border-b-base-content/10">
            <th class="w-full">环境名称</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="i in dotenvList" :key="i" class="transition-colors hover:bg-base-300">
            <td role="btn" @click="nonebotStore.updateEnv(i)">
              {{ i }}
              <span
                v-if="i === nonebotStore.selectedBot?.use_env"
                class="badge badge-primary badge-sm text-base-100"
              >
                已选择
              </span>
            </td>
            <td>
              <button
                :class="{ 'btn btn-xs btn-square btn-ghost': true, 'btn-disabled': i === '.env' }"
                @click="removeEnv(i)"
              >
                <span class="material-symbols-outlined text-base"> close </span>
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <div class="flex items-center flex-wrap justify-between gap-4 md:gap-0">
        <button v-if="!isAddEnv" class="btn btn-ghost btn-sm" @click="isAddEnv = true">
          + 添加
        </button>
        <div v-else class="flex gap-2">
          <input v-model="inputValue" class="input input-sm bg-base-200" placeholder="请输入" />
          <button class="btn btn-sm btn-ghost" @click="addEnv()">确认</button>
          <button class="btn btn-sm btn-ghost" @click="cancel()">取消</button>
        </div>

        <form method="dialog">
          <button class="btn btn-sm btn-primary text-base-100">完成</button>
        </form>
      </div>
    </div>
  </dialog>
</template>
