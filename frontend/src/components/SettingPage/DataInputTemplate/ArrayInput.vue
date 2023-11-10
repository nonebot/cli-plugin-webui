<script setup lang="ts">
import { ref } from "vue";

const props = defineProps<{
  inputID: string;
  literal: any[];
  configured: any[];
  setAction: Function;
}>();

const isPass = ref(false);
const inputValue = ref("");
const submitData = ref(props.configured);

const checkInput = (event: Event) => {
  const target = event.target as HTMLInputElement;
  inputValue.value = target.value;
  isPass.value = inputValue.value ? true : false;
  if (isPass.value) {
    submitData.value = [inputValue.value, ...props.configured];
  }
};

const addAction = () => {
  props.setAction(props.inputID, submitData.value, "array");
  props.configured.push(inputValue.value);
};

const deleteAction = (item: any) => {
  const sd = submitData.value.filter((i) => i !== item);
  props.setAction(props.inputID, sd, "array");
  const itemIndex = props.configured.indexOf(item);
  if (itemIndex !== -1) {
    props.configured.splice(itemIndex, 1);
  }
};
</script>

<template>
  <div>
    <table class="table table-xs">
      <thead>
        <tr>
          <th>值</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="i in configured" class="hover:bg-base-300">
          <td>{{ i }}</td>
          <td class="flex">
            <label
              class="swap pl-1 pr-1 rounded opacity-30 hover:opacity-100 transition-all ease-in"
            >
              <input type="checkbox" />
              <span
                class="swap-off material-symbols-outlined text-xl leading-5"
                @click="deleteAction(i)"
              >
                delete
              </span>
              <span class="swap-on material-symbols-outlined text-xl leading-5">
                check
              </span>
            </label>
          </td>
        </tr>
      </tbody>
    </table>

    <div class="flex mt-2">
      <input
        v-if="!literal.length"
        class="input input-xs rounded bg-base-300"
        :value="inputValue"
        @input="checkInput"
      />
      <select
        v-else
        class="select select-xs rounded bg-base-300 w-full max-w-xs"
        @change="
          (event: any) => {
            inputValue = event.target.value;
          }
        "
      >
        <option v-for="i in literal">{{ i }}</option>
      </select>

      <button
        :class="{
          'ml-2 btn btn-xs rounded': true,
          'btn-disabled': !literal.length && !isPass,
        }"
        @click="addAction()"
      >
        添加
      </button>
    </div>
  </div>
</template>
