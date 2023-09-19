<script setup lang="ts">
import AppSideNav from "@/layouts/AppSideNav.vue";
import AppStatusBar from "@/layouts/AppStatusBar.vue";
</script>

<template>
  <AppSideNav />
  <div class="view pl-0 md:pl-14 pt-12 md:pt-0">
    <router-view />
  </div>
  <AppStatusBar />
</template>

<style scoped>
.view {
  position: fixed;
  top: 0;
  left: 0;
  height: 100%;
  padding-bottom: 1.5rem;

  width: 100%;
  overflow: hidden;
}
</style>
