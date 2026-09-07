<script setup lang="ts">
import type { ConfigType, ModuleConfigChild, ModuleType } from "@/client/api";
import { ref, watch } from "vue";
import { updateConfig } from "../client";

const props = defineProps<{
  moduleType: ModuleType | ConfigType;
  data: ModuleConfigChild;
}>();

const data = props.data as Omit<ModuleConfigChild, "configured" | "default"> & {
  configured: string;
  default: string;
};

const inputValue = ref(data.configured),
  inEditing = ref(false),
  isNumber = ref(true);

const update = async () => {
  if (!inputValue.value) {
    return;
  }
  await updateConfig(props.moduleType, data.conf_type, data.name, inputValue.value);
};

watch(inputValue, (value) => {
  isNumber.value =
    value !== undefined && value.trim().length !== 0 && !isNaN(Number(value.trim()));
});
</script>

<template>
  <div class="flex items-center gap-2">
    <label class="form-control">
      <input
        ref="element"
        v-model="inputValue"
        :class="{ 'input input-sm !bg-base-100': true, 'input-error': !isNumber }"
        :disabled="!inEditing"
        @blur="update()"
      />
      <div v-if="!isNumber" class="label">
        <span class="label-text-alt text-error">请键入数字</span>
      </div>
    </label>

    <div class="join">
      <button
        class="btn btn-xs btn-ghost join-item tooltip font-normal"
        data-tip="恢复默认"
      >
        <span class="material-symbols-outlined text-base"> refresh </span>
      </button>

      <button
        class="btn btn-xs btn-ghost join-item tooltip font-normal"
        data-tip="编辑"
        @click="inEditing = !inEditing"
      >
        <span
          :class="{
            'material-symbols-outlined text-base': true,
            'text-primary': inEditing,
          }"
        >
          edit
        </span>
      </button>
    </div>
  </div>
</template>
