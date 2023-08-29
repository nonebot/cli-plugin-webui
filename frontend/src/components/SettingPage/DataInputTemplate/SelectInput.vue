<script setup lang="ts">
defineProps<{
  inputID: string;
  literal: string[] | number[];
  configured: string;
  setAction: Function;
}>();
</script>

<template>
  <select
    class="select select-sm bg-base-300 rounded w-full max-w-xs"
    @change="
      (event: any) => {
        setAction(inputID, event.target.value, 'select')
      }
    "
  >
    <option v-for="i in literal" :value="i" :selected="configured === i">
      {{ i }}
    </option>
  </select>
</template>
