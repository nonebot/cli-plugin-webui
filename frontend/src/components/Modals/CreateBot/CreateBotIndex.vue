<script setup lang="ts">
import { ref } from 'vue'
import TemplateSelect from './TemplateSelect.vue'
import BotBasic from './BotBasic.vue'
import MirrorSelect from './MirrorSelect.vue'
import DriverSelect from './DriverSelect.vue'
import AdapterSelect from './AdapterSelect.vue'
import Installation from './Installation.vue'
import { useCreateBotStore } from '.'

const store = useCreateBotStore()

const createBotModal = ref<HTMLDialogElement>()

defineExpose({
  openModal: () => createBotModal.value?.showModal(),
  closeModal: () => createBotModal.value?.close()
})

interface StepItem {
  title: string
  pass: () => boolean
  component?: any
}

const steps: StepItem[] = [
  {
    title: '模板选择',
    pass: () => true,
    component: TemplateSelect
  },
  {
    title: '基础信息',
    pass: () => store.projectName !== '' && store.projectPath !== '',
    component: BotBasic
  },
  {
    title: '镜像选择',
    pass: () => store.pythonMirror !== '',
    component: MirrorSelect
  },
  {
    title: '驱动器选择',
    pass: () => store.drivers.length > 0,
    component: DriverSelect
  },
  {
    title: '适配器选择',
    pass: () => store.adapters.length > 0,
    component: AdapterSelect
  },
  {
    title: '安装依赖',
    pass: () => false,
    component: Installation
  }
]
</script>

<template>
  <dialog ref="createBotModal" class="modal" @close="store.reset()">
    <div class="overflow-hidden modal-box w-11/12 max-w-5xl rounded-xl flex flex-col gap-4">
      <h3 class="font-semibold text-lg">创建 NoneBot 实例</h3>
      <div class="w-full flex justify-center">
        <ul class="steps w-full xl:w-3/4 gap-4">
          <li
            v-for="(step, index) in steps"
            :key="step.title"
            :role="
              step.pass() && !store.isInstalling && !store.createBotSuccess ? 'button' : undefined
            "
            :data-content="index < store.step ? '✓' : index + 1"
            :class="{
              step: true,
              'step-primary': index <= store.step
            }"
            @click="
              step.pass() && !store.isInstalling && !store.createBotSuccess
                ? (store.step = index)
                : null
            "
          >
            <div :class="{ 'opacity-20': index < store.step }">{{ step.title }}</div>
          </li>
        </ul>
      </div>

      <div v-show="store.warningMessage" class="flex justify-center">
        <div role="alert" class="alert alert-warning w-full max-w-xs">
          <span class="material-symbols-outlined"> warning </span>
          {{ store.warningMessage }}
        </div>
      </div>

      <div class="overflow-auto h-full w-full">
        <component :is="steps[store.step].component" />
      </div>
    </div>
  </dialog>
</template>

<style scoped>
.steps .step-primary + .step-primary:before,
.steps .step-primary:after {
  @apply !text-base-100;
}
</style>
