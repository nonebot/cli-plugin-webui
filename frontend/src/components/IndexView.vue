<script setup lang="ts">
import AppTopBar from "@/layouts/AppTopBar.vue";
import AppSideNav from "@/layouts/AppSideNav.vue";
import AppStatusBar from "@/layouts/AppStatusBar.vue";
</script>

<template>
  <div class="webui" style="height: 100vh">
    <AppTopBar />
    <div class="content max-[390px]:pt-[40px] pb-[22px]">
      <AppSideNav />
      <div class="view">
        <router-view />
      </div>
    </div>
    <AppStatusBar />
  </div>
</template>

<style>
.view {
  width: 100%;
  padding: 30px;
  overflow-y: auto;
}

@media screen and (max-width: 1280px) {
  .view {
    padding: 16px;
  }
}

.webui {
  overflow: hidden;

  background: hsl(var(--b1));
}

.content {
  height: 100%;
  width: 100%;
  display: flex;
}
</style>
