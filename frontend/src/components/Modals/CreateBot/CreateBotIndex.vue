<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useNoneBotStore } from '@/stores'

import TemplateSelect from './TemplateSelect.vue'
import BotBasic from './BotBasic.vue'
import MirrorSelect from './MirrorSelect.vue'
import DriverSelect from './DriverSelect.vue'
import AdapterSelect from './AdapterSelect.vue'
import Installation from './Installation.vue'

const createBotModal = ref<HTMLDialogElement>()

defineExpose({
  openModal: () => {
    createBotModal.value?.showModal()
  },
  closeModal: () => {
    createBotModal.value?.close()
  }
})

const store = useNoneBotStore()

const createStep = ref(0),
  warningMessage = ref('')

interface StepItem {
  title: string
  pass: () => boolean
  component?: any
}

const steps: StepItem[] = [
  {
    title: '模板选择',
    pass: () => store.template !== '',
    component: TemplateSelect
  },
  {
    title: '基础信息',
    pass: () => store.name !== '' && store.projectPath !== '',
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

const nextStep = () => {
  const check = steps[createStep.value].pass()
  if (check) {
    createStep.value++
    warningMessage.value = ''
  } else {
    warningMessage.value = '请确认信息补充完整'
  }
}

const finishCreate = () => {
  store.reset()
  createBotModal.value?.close()
  createStep.value = 0
  warningMessage.value = ''
}
</script>

<template>
  <dialog ref="createBotModal" class="modal" @close="finishCreate">
    <div class="overflow-hidden modal-box w-11/12 max-w-5xl rounded-xl flex flex-col gap-8">
      <h3 class="font-semibold text-lg">创建 NoneBot 实例</h3>
      <div class="w-full flex justify-center">
        <ul class="steps w-full xl:w-3/4 gap-4">
          <li
            v-for="(step, index) in steps"
            :role="step.pass() && !store.isInstalling && !store.addNoneBotSuccess ? 'button' : ''"
            :data-content="index < createStep ? '✓' : index + 1"
            :class="{
              step: true,
              'step-primary': index <= createStep
            }"
            @click="
              step.pass() && !store.isInstalling && !store.addNoneBotSuccess
                ? (createStep = index)
                : null
            "
          >
            <div :class="{ 'opacity-20': index < createStep }">{{ step.title }}</div>
          </li>
        </ul>
      </div>

      <div v-show="warningMessage.length" class="flex justify-center">
        <div role="alert" class="alert alert-warning w-full max-w-xs">
          <span class="material-symbols-outlined"> warning </span>
          {{ warningMessage }}
        </div>
      </div>

      <div class="overflow-hidden h-full w-full">
        <div v-for="(step, index) in steps">
          <component v-if="index === createStep" :is="step?.component"></component>
        </div>
      </div>

      <div class="flex justify-between">
        <button
          :class="{
            'btn btn-sm btn-primary font-normal text-white': true,
            'btn-disabled': !createStep || store.addNoneBotSuccess || store.isInstalling
          }"
          @click="createStep--, (warningMessage = '')"
        >
          上一步
        </button>

        <button
          v-if="!store.addNoneBotSuccess"
          :class="{
            'btn btn-sm btn-primary font-normal text-white': true,
            'btn-disabled': createStep >= steps.length - 1
          }"
          @click="nextStep"
        >
          下一步
        </button>
        <button
          v-else
          class="btn btn-sm btn-primary font-normal text-white"
          @click="finishCreate()"
        >
          完成
        </button>
      </div>
    </div>
  </dialog>
</template>

<style scoped>
.steps .step-primary + .step-primary:before,
.steps .step-primary:after {
  color: white !important;
}
</style>
