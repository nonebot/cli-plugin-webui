<script lang="ts">
import { GlobalStore } from "@/store/app";

export default {
  created() {
    GlobalStore().nowPageName = "Home";
  },
  methods: {},
};
</script>

<script setup lang="ts"></script>

<template>
  <div class="index-header">
    <div class="custom-padding w-1/2">
      <div class="w-full tracking-tight font-light">
        <p class="text-lg">欢迎使用</p>
        <div class="mt-2 mb-2 text-7xl">
          <span class="main-word">N</span>one<span class="main-word">B</span>ot
        </div>
        <p class="text-lg">跨平台 PYTHON 异步机器人框架</p>
      </div>
    </div>
  </div>
</template>

<style>
.index-header {
  height: 100%;
  width: 100%;

  display: flex;
}

/* TODO: Support Mobile Terminal */
.custom-padding {
  padding: 100px;
}

.main-word {
  color: hsl(var(--p));
}
</style>
