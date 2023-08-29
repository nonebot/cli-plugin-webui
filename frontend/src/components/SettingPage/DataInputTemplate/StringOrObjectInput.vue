<script setup lang="ts">
import { ref } from "vue";

const props = defineProps<{
  inputID: string;
  needType: string;
  configured: string;
  setAction: Function;
}>();

const isPass = ref(false);
const inputValue = ref(props.configured);

const checkInput = (event: Event) => {
  let target;
  target = event.target as HTMLElement;
  if (target.tagName === "TEXTAREA") {
    target = event.target as HTMLTextAreaElement;
  } else {
    target = event.target as HTMLInputElement;
  }

  inputValue.value = target.value;
  if (!inputValue.value || inputValue.value === props.configured) {
    isPass.value = false;
  } else {
    isPass.value = true;
  }
};
</script>

<template>
  <div>
    <div v-if="configured.length >= 15" class="w-full">
      <textarea
        class="textarea bg-base-300 w-full max-w-md"
        placeholder="请键入内容"
        :value="inputValue"
        @input="checkInput"
      ></textarea>
    </div>
    <div v-else class="tooltip" :data-tip="`当前：${configured}`">
      <input
        class="input input-xs mr-2 rounded bg-base-300"
        placeholder="请键入内容"
        :value="inputValue"
        @input="checkInput"
      />
    </div>

    <button
      :class="{ 'btn btn-xs rounded': true, 'btn-disabled': !isPass }"
      @click="setAction(inputID, inputValue, needType)"
    >
      更改
    </button>
  </div>
</template>
