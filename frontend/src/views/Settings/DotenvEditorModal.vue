<script setup lang="ts">
import { ProjectService } from '@/client/api'
import EditorItem from '@/components/EditorItem.vue'
import { useNoneBotStore, useToastStore } from '@/stores'
import { editor as monacoEditor } from 'monaco-editor/esm/vs/editor/editor.api.js'
import { ref, watch } from 'vue'

const dotenvEditorModal = ref<HTMLDialogElement>()

defineExpose({
  openModal: async () => {
    dotenvEditorModal.value?.showModal()
    await getDotenvFile()
  },
  closeModal: () => dotenvEditorModal.value?.close()
})

const props = defineProps<{
  theme: string
}>()

const nonebotStore = useNoneBotStore()
const toast = useToastStore()

const editorValue = ref<string>('')
const returnEditorValue = ref<string>('')
const editor = ref<monacoEditor.IStandaloneCodeEditor>()

watch(
  () => props.theme,
  (theme) => {
    editor.value?.updateOptions({
      theme: theme === 'dark' ? 'vs-dark' : 'vs'
    })
  }
)

const getDotenvFile = async () => {
  if (!nonebotStore.selectedBot) {
    return
  }

  const { data, error } = await ProjectService.getDotenvFileV1ProjectConfigDotenvGet({
    query: {
      env: nonebotStore.selectedBot.use_env!,
      project_id: nonebotStore.selectedBot.project_id
    }
  })

  if (error) {
    dotenvEditorModal.value?.close()
    toast.add('error', `获取 dotenv 文件失败, 原因：${error.detail?.toString()}`, '', 5000)
  }

  if (data) {
    editorValue.value = data.detail
  }
}

const updateDotenvFile = async () => {
  if (!nonebotStore.selectedBot) {
    return
  }

  const { error } = await ProjectService.updateDotenvFileV1ProjectConfigDotenvPut({
    query: {
      data: returnEditorValue.value,
      env: nonebotStore.selectedBot.use_env!,
      project_id: nonebotStore.selectedBot.project_id
    },
    body: {
      detail: returnEditorValue.value
    }
  })

  if (error) {
    toast.add('error', `更新文件失败, 原因：${error.detail?.toString()}`, '', 5000)
  }

  if (!error) {
    dotenvEditorModal.value?.close()
    toast.add('success', `${nonebotStore.selectedBot.use_env} 文件已更新`, '', 5000)
  }
}
</script>

<template>
  <dialog ref="dotenvEditorModal" class="modal p-4" @close="editorValue = ''">
    <div class="modal-box !w-full !max-w-5xl flex flex-col gap-4">
      <h3 class="font-semibold text-lg">Dotenv 文件编辑</h3>

      <div class="p-2 shadow-inner rounded-lg">
        <EditorItem
          v-model="editorValue"
          class="h-96 md:h-80"
          :editor-optional="{
            language: 'shell',
            minimap: { enabled: false },
            accessibilitySupport: 'off',
            automaticLayout: true,
            lineNumbers: 'off'
          }"
          v-on:editor="
            (event) => {
              editor = event
            }
          "
          v-on:update-value="
            (value) => {
              returnEditorValue = value
            }
          "
        />
      </div>

      <form method="dialog" class="flex items-center justify-center md:justify-end gap-2">
        <button class="btn btn-sm btn-primary text-base-100" @click="updateDotenvFile()">
          保存
        </button>

        <button class="btn btn-sm">取消</button>
      </form>
    </div>
  </dialog>
</template>
