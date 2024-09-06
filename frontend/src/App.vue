<script setup lang="ts">
import { RouterView } from 'vue-router'
import Toast from './components/Toast.vue'
import { useToastStore } from './stores/ToastStorage'

const store = useToastStore()
</script>

<template>
  <RouterView />

  <TransitionGroup name="list" tag="div" class="toast-container">
    <Toast v-for="toast in store.visibleToasts" :key="toast.id" :data="toast" />
  </TransitionGroup>
</template>

<style lang="css" scoped>
.toast-container {
  position: fixed;
  bottom: 1rem;
  right: 1rem;
  z-index: 9999;

  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.list-move,
.list-enter-active,
.list-leave-active {
  transition: all 0.5s ease;
}

.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateX(30px);
}
</style>
