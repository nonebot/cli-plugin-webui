<script setup lang="ts">
import AddProjectByCreate from "@/components/HomePage/Modals/AddProjectByCreate.vue";
import AddProjectByPath from "@/components/HomePage/Modals/AddProjectByPath.vue";

import { ref } from "vue";

const addProjectChoiceModal = ref<HTMLDialogElement>();

defineExpose({
  openModal() {
    addProjectChoiceModal.value?.showModal();
  },
  closeModal() {
    addProjectChoiceModal.value?.close();
  },
});

const createProjectModal = ref<InstanceType<typeof AddProjectByCreate> | null>();
const createProjectByPathModal = ref<InstanceType<typeof AddProjectByPath> | null>();
</script>

<template>
  <AddProjectByCreate ref="createProjectModal" />
  <AddProjectByPath ref="createProjectByPathModal" />

  <dialog ref="addProjectChoiceModal" class="modal">
    <div class="modal-box rounded-lg">
      <h3 class="font-bold text-lg">创建/添加 NoneBot 实例</h3>
      <button
        class="btn btn-sm btn-circle absolute right-2 top-2"
        @click="addProjectChoiceModal?.close()"
      >
        ✕
      </button>

      <div class="custom-flex mt-4 p-8 w-full">
        <div class="flex flex-col justify-center">
          <div>没有 NoneBot 实例？</div>
          <button
            class="mt-2 btn btn-primary rounded-lg h-10 min-h-0 text-white"
            @click="createProjectModal?.openModal(), addProjectChoiceModal?.close()"
          >
            创建一个！
          </button>
        </div>

        <div class="flex flex-col justify-center">
          <div>已有 NoneBot 实例？</div>
          <button
            class="mt-2 btn btn-primary rounded-lg h-10 min-h-0 text-white"
            @click="createProjectByPathModal?.openModal(), addProjectChoiceModal?.close()"
          >
            即刻添加！
          </button>
        </div>
      </div>
    </div>
    <form method="dialog" class="modal-backdrop">
      <button>close</button>
    </form>
  </dialog>
</template>

<style scoped>
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
