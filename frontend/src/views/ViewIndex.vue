<script setup lang="ts">
import HeaderIndex from '@/components/header/HeaderIndex.vue'
import SidebarIndex from '@/components/sidebar/SidebarIndex.vue'

import { RouterView } from 'vue-router'
</script>

<template>
  <div class="h-screen flex">
    <HeaderIndex />
    <SidebarIndex />
    <div class="w-full pt-[7rem] p-4 2xl:px-20">
      <RouterView />
    </div>
  </div>
</template>
