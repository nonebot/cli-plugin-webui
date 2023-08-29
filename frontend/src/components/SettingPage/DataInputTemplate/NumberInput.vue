<script setup lang="ts">
import { ref } from "vue";

const props = defineProps<{
  inputID: string;
  configured: string | number;
  setAction: Function;

  exclusiveMinimum?: number;
  minimum?: number;
  exclusiveMaximum?: number;
  maximum?: number;
}>();

const isPass = ref(false);
const isValueError = ref(false);
const isExclusiveMinimum = ref(false);
const isMinimum = ref(false);
const isExclusiveMaximum = ref(false);
const isMaximum = ref(false);
const inputValue = ref(props.configured);

const checkInput = (event: Event) => {
  const target = event.target as HTMLInputElement;
  inputValue.value = target.value;

  const inputIsEmpty = !target.value;
  const inputIsConfigured = target.value === props.configured;

  if (inputIsEmpty || inputIsConfigured) {
    isPass.value = false;
    isValueError.value = false;
    isExclusiveMinimum.value = false;
    isMinimum.value = false;
    isExclusiveMaximum.value = false;
    isMaximum.value = false;
    return;
  }

  const parsedValue = Number(target.value);
  if (isNaN(parsedValue)) {
    isValueError.value = true;
    isPass.value = false;
    return;
  }

  if (props.exclusiveMinimum) {
    isExclusiveMinimum.value = parsedValue < props.exclusiveMinimum;
  }
  if (props.minimum) {
    isMinimum.value = parsedValue <= props.minimum;
  }
  if (props.exclusiveMaximum) {
    isExclusiveMaximum.value = parsedValue > props.exclusiveMaximum;
  }
  if (props.maximum) {
    isMaximum.value = parsedValue >= props.maximum;
  }

  isPass.value =
    !isValueError.value &&
    !isExclusiveMinimum.value &&
    !isMinimum.value &&
    !isExclusiveMaximum.value &&
    !isMaximum.value;
};
</script>

<template>
  <div class="flex items-end">
    <div class="tooltip" :data-tip="`当前：${configured}`">
      <div class="form-control w-full max-w-xs">
        <label class="label p-0 pb-1">
          <TransitionGroup>
            <span
              v-if="isValueError"
              class="label-text text-xs"
              style="color: hsl(var(--er))"
              >请键入数字</span
            >
            <span
              v-if="isExclusiveMinimum || isMinimum"
              class="label-text text-xs"
              style="color: hsl(var(--er))"
              >小于最小值</span
            >
            <span
              v-if="isExclusiveMaximum || isMaximum"
              class="label-text text-xs"
              style="color: hsl(var(--er))"
              >超出最大值</span
            >
          </TransitionGroup>
        </label>
        <input
          class="input input-xs rounded bg-base-300"
          placeholder="请键入内容"
          :value="inputValue"
          @input="checkInput"
        />
      </div>
    </div>

    <button
      :class="{ 'ml-2 btn btn-xs rounded': true, 'btn-disabled': !isPass }"
      @click="setAction(inputID, inputValue, 'number')"
    >
      更改
    </button>
  </div>
</template>
