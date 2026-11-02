<script setup lang="ts">
import LoginForm from "@/views/Login/LoginForm.vue";
import Footer from "@/components/FooterItem.vue";
</script>

<template>
  <div class="hero min-h-screen">
    <div class="hero-content text-center flex-col">
      <span class="material-symbols-outlined text-primary" style="font-size: 14rem">
        circle
      </span>

      <h1 class="text-5xl font-normal"><span class="text-primary">None</span>Bot</h1>
      <p
        class="whitespace-nowrap text-base-content opacity-70 font-medium text-sm tracking-wide"
      >
        跨平台 PYTHON 异步机器人框架
      </p>

      <LoginForm />
    </div>
  </div>

  <Footer />
</template>

<style scoped>
.material-symbols-outlined {
  font-variation-settings:
    "FILL" 0,
    "wght" 50,
    "GRAD" -25,
    "opsz" 20;
}
</style>
