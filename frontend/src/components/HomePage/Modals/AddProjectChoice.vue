<script setup lang="ts">
import CreateProject from "./CreateProject.vue";

import { ref } from "vue";

const createProjectModal = ref<InstanceType<typeof CreateProject> | null>();
const showModal = ref(false);

const openModal = () => {
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
};

defineExpose({
  openModal,
  closeModal,
});
</script>

<template>
  <CreateProject ref="createProjectModal" />

  <dialog :class="{ 'modal pl-0 md:pl-14': true, 'modal-open': showModal }">
    <form method="dialog" class="modal-box rounded-lg">
      <h3 class="font-bold text-lg">创建/添加 NoneBot 实例</h3>
      <button
        class="btn btn-sm btn-circle absolute right-2 top-2"
        @click="closeModal()"
      >
        ✕
      </button>

      <div class="custom-flex mt-4 p-8 w-full">
        <div class="flex flex-col justify-center">
          <div>没有 NoneBot 实例？</div>
          <button
            class="mt-2 btn btn-primary rounded-lg h-10 min-h-0 text-white"
            @click="createProjectModal?.openModal(), closeModal()"
          >
            创建一个！
          </button>
        </div>

        <div class="flex flex-col justify-center">
          <div>已有 NoneBot 实例？</div>
          <button
            class="mt-2 btn btn-primary rounded-lg h-10 min-h-0 text-white"
          >
            即刻添加！
          </button>
        </div>
      </div>
    </form>
    <form method="dialog" class="modal-backdrop">
      <button @click="closeModal()">close</button>
    </form>
  </dialog>
</template>

<style>
.custom-flex {
  display: flex;
  justify-content: space-around;
  align-items: center;
}

@media screen and (max-width: 640px) {
  .custom-flex {
    flex-direction: column;
  }
}
</style>
