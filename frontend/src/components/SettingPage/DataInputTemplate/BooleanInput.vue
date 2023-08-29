<script setup lang="ts">
defineProps<{
  inputID: string;
  configured: boolean;
  setAction: Function;
}>();
</script>

<template>
  <div class="form-control">
    <label class="p-0 label cursor-pointer">
      <input
        type="checkbox"
        class="checkbox checkbox-xs rounded"
        :checked="configured"
        @click="setAction(inputID, !configured, 'boolean')"
      />
      <span class="label-text">启用</span>
    </label>
  </div>
</template>
