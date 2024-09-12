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
  await ProjectService.getProjectEnvListV1ProjectConfigEnvListGet(
    nonebotStore.selectedBot.project_id
  )
    .then((res) => {
      dotenvList.value = res.detail
    })
    .catch((err) => {
      let detail = ''
      if (err.body) {
        detail = err.body.detail
      } else {
        detail = err
      }
      toast.add('error', `获取环境失败, 原因：${detail}`, '', 5000)
    })
}

const setDotenv = (env: string) => {
  nonebotStore.enabledEnv = env
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

  await ProjectService.createProjectEnvV1ProjectConfigEnvCreatePost(
    inputValue.value,
    nonebotStore.selectedBot.project_id
  )
    .then(() => {
      dotenvList.value.push(inputValue.value)
      cancel()
    })
    .catch((err) => {
      let detail = ''
      if (err.body) {
        detail = err.body.detail
      } else {
        detail = err
      }
      toast.add('error', `添加环境失败, 原因：${detail}`, '', 5000)
    })
}

const removeEnv = async (env: string) => {
  if (!nonebotStore.selectedBot) {
    toast.add('warning', '未选择实例', '', 5000)
    return
  }

  await ProjectService.deleteProjectEnvV1ProjectConfigEnvDeleteDelete(
    env,
    nonebotStore.selectedBot.project_id
  )
    .then(async () => {
      await getDotenvList()
      nonebotStore.enabledEnv = dotenvList.value[0]
    })
    .catch((err) => {
      let detail = ''
      if (err.body) {
        detail = err.body.detail
      } else {
        detail = err
      }
      toast.add('error', `删除环境失败, 原因：${detail}`, '', 5000)
    })
}

const cancel = () => {
  isAddEnv.value = false
  inputValue.value = ''
}
</script>

<template>
  <dialog ref="dotenvManageModal" class="modal">
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
            <td role="btn" @click="setDotenv(i)">
              {{ i }}
              <span
                v-if="i === nonebotStore.enabledEnv"
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

      <div class="flex items-center justify-between">
        <button v-if="!isAddEnv" class="btn btn-ghost btn-sm" @click="isAddEnv = true">
          + 添加
        </button>
        <div v-else class="flex gap-2">
          <input v-model="inputValue" class="input input-sm bg-base-200" placeholder="请输入" />
          <button class="btn btn-sm btn-ghost" @click="addEnv()">确认</button>
          <button class="btn btn-sm btn-ghost" @click="cancel()">取消</button>
        </div>

        <button
          class="btn btn-sm btn-primary text-base-100"
          @click="cancel(), dotenvManageModal?.close()"
        >
          完成
        </button>
      </div>
    </div>
  </dialog>
</template>
