<script setup lang="ts">
import { ref, watch } from 'vue'
import GetBotBasicInfo from './GetBotBasicInfo.vue'
import MirrorSelect from './MirrorSelect.vue'
import Installation from './Installation.vue'
import { useAddBotStore } from '.'

const store = useAddBotStore()

const addBotModal = ref<HTMLDialogElement>()

defineExpose({
  openModal: () => addBotModal.value?.showModal(),
  closeModal: () => addBotModal.value?.close()
})

interface StepItem {
  title: string
  pass: () => boolean
  component?: any
}

const steps: StepItem[] = [
  {
    title: '信息获取',
    pass: () => true,
    component: GetBotBasicInfo
  },
  {
    title: '镜像选择',
    pass: () => store.searchBotSuccess,
    component: MirrorSelect
  },
  {
    title: '确认&安装依赖',
    pass: () => store.pythonMirror !== '',
    component: Installation
  }
]

watch(
  () => store.cancelAddBot,
  (newValue) => {
    if (newValue) {
      addBotModal.value?.close()
      store.cancelAddBot = false
    }
  }
)
</script>

<template>
  <dialog ref="addBotModal" class="modal">
    <div class="modal-box overflow-hidden w-11/12 max-w-5xl rounded-xl flex flex-col gap-8">
      <h3 class="font-semibold text-lg">添加 NoneBot 实例</h3>
      <div class="w-full flex justify-center">
        <ul class="steps w-full xl:w-3/4 gap-4">
          <li
            v-for="(step, index) in steps"
            :key="step.title"
            :role="step.pass() && !store.isInstalling && !store.addBotSuccess ? 'button' : ''"
            :data-content="index < store.step ? '✓' : index + 1"
            :class="{
              step: true,
              'step-primary': index <= store.step
            }"
            @click="
              step.pass() && !store.isInstalling && !store.addBotSuccess
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

      <div class="overflow-hidden h-full w-full">
        <div v-for="(step, index) in steps" :key="step.title">
          <component :is="step.component" v-show="index === store.step" />
        </div>
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
