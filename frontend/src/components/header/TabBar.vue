<script setup lang="ts">
import { useRoute } from 'vue-router'
import router from '@/router'
import { useViewHistoryRecorderStore } from '@/stores'
import type { NavItem } from '@/router/client'
import { ref } from 'vue'

const route = useRoute()
const store = useViewHistoryRecorderStore()

const isCloseTab = ref(false)
const draggedIndex = ref<number>()

const onDragStart = (index: number) => {
  draggedIndex.value = index
}

const onDragOver = (e: DragEvent) => {
  e.preventDefault()
}

const onDragEnd = (index: number) => {
  store.move(draggedIndex.value!, index)
}

const isCurrentRoute = (path: string) => {
  return path === route.path
}

const operation = (route: NavItem) => {
  if (!isCloseTab.value) {
    router.push(route.routeData.path)
    return
  }

  store.remove(route)
  const routeTo =
    store.viewHistory.length > 0
      ? store.viewHistory[store.viewHistory.length - 1].routeData.path
      : '/'
  router.push(routeTo)
  isCloseTab.value = false
}
</script>

<template>
  <div role="tablist" class="tabs tabs-lifted justify-start">
    <TransitionGroup>
      <a
        v-for="(i, index) in store.viewHistory"
        :key="i.name"
        role="tab"
        :class="{
          'tab flex gap-2 hover:bg-primary/[.2] transition !border-b-0': true,
          '[--tab-bg:oklch(var(--b2))] tab-active': isCurrentRoute(i.routeData.path)
        }"
        @click="operation(i)"
        draggable="true"
        @dragstart="onDragStart(index)"
        @dragover="onDragOver"
        @drop="onDragEnd(index)"
      >
        {{ i.name }}
        <span
          v-if="isCurrentRoute(i.routeData.path)"
          class="text-base material-symbols-outlined"
          @click="isCloseTab = true"
        >
          close
        </span>
      </a>
    </TransitionGroup>
    <div class="tab [--tab-border-color:transparent]"></div>
  </div>
  <div class="border-t border-base-300"></div>
</template>

<style scoped>
.material-symbols-outlined {
  font-variation-settings:
    'FILL' 0,
    'wght' 400,
    'GRAD' -25,
    'opsz' 48;
}

.tabs-lifted > .tab.tab-active:not(.tab-disabled):not([disabled]):before,
.tabs-lifted > .tab:is(input:checked):before {
  z-index: 0;
}
</style>
