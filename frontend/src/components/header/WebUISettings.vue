<script setup lang="ts">
import { ref } from 'vue'
import { useCustomStore } from '@/stores'
import DrawerItem from '@/components/DrawerItem.vue'

const store = useCustomStore()

const drawerRef = ref<InstanceType<typeof DrawerItem> | null>()
</script>

<template>
  <DrawerItem ref="drawerRef">
    <template v-slot:button>
      <button class="btn btn-sm btn-ghost btn-square" @click="drawerRef?.showDrawer()">
        <span class="material-symbols-outlined"> tune </span>
      </button>
    </template>

    <template v-slot:drawer-title>WebUI 设置</template>

    <template v-slot:drawer-body>
      <div class="h-full flex flex-col gap-4">
        <div class="form-control">
          <label class="label cursor-pointer">
            <span class="label-text">主题跟随系统</span>
            <input
              type="checkbox"
              class="toggle"
              :checked="store.isThemeFollowSystem"
              @click="store.toggleThemeFollowSystem"
            />
          </label>
        </div>

        <div class="form-control">
          <label class="label cursor-pointer">
            <span class="label-text">启用开发模式</span>
            <input
              type="checkbox"
              class="toggle"
              :checked="store.isDebug"
              @click="store.toggleDebug"
            />
          </label>
        </div>

        <div class="form-control">
          <label class="label cursor-pointer">
            <span class="label-text">是否即时搜索</span>
            <input
              type="checkbox"
              class="toggle"
              :checked="store.isInstantSearch"
              @click="store.toggleInstantSearch()"
            />
          </label>
        </div>
      </div>
    </template>
  </DrawerItem>
</template>

<style scoped>
.material-symbols-outlined {
  font-variation-settings:
    'FILL' 0,
    'wght' 400,
    'GRAD' -25,
    'opsz' 48;
}
</style>
