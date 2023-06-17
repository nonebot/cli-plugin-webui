<script setup lang="ts">
import AppSideNav from "@/layouts/AppSideNav.vue";
import AppStatusBar from "@/layouts/AppStatusBar.vue";
</script>

<template>
  <div class="webui" style="height: 100vh">
    <div class="content">
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
}

@media screen and (max-width: 1280px) {
  .view {
    padding: 10px;
  }
}

.webui {
  overflow: hidden;

  background: hsl(var(--b1));
}

.content {
  height: calc(100% - 22px);
  width: 100%;
  display: flex;
}
</style>
