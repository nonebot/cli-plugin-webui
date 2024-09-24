<script setup lang="ts">
import OperationBar from '@/views/Operation/OperationBar.vue'
import BotDetails from '@/views/Operation/BotDetails.vue'
import Terminal from '@/views/Operation/Terminal.vue'
</script>

<template>
  <div class="flex flex-col gap-4">
    <OperationBar />

    <BotDetails />

    <Terminal />
  </div>
</template>
