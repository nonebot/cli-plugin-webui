<script setup lang="ts">
import { useRoute } from 'vue-router'
import router from '@/router'
import { useViewHistoryRecorderStore } from '@/stores/viewHistoryRecorder'
import type { RouteItem } from '@/router/client'
import { ref } from 'vue'

const route = useRoute()
const store = useViewHistoryRecorderStore()
const isCloseTab = ref(false)

const isCurrentRoute = (path: string) => {
  return path === route.path
}

const operation = (route: RouteItem) => {
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
  <div role="tablist" class="tabs tabs-lifted justify-start bg-base-100">
    <a
      v-for="i in store.viewHistory"
      role="tab"
      :class="{
        'tab flex gap-2': true,
        '[--tab-bg:oklch(var(--b2))] tab-active': isCurrentRoute(i.routeData.path)
      }"
      @click="operation(i)"
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
    <div class="tab [--tab-border-color:transparent]"></div>
  </div>
  <div
    class="border-t border-base-300 -mt-[1px] bg-base-100 pointer-events-none sticky flex h-3 [mask-image:linear-gradient(#000000,transparent)]"
  ></div>
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
