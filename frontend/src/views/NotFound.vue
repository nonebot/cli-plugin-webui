<script setup lang="ts">
import { RouterLink } from 'vue-router'
import Footer from '@/components/Footer.vue'

defineProps<{ pathMatched?: string }>()
</script>

<template>
  <div class="hero min-h-screen">
    <div class="hero-content text-center">
      <div class="max-w-md">
        <h1 class="text-5xl">404 Not Found</h1>
        <p class="py-6">{{ pathMatched }}</p>
        <RouterLink to="/">
          <button class="btn btn-primary text-white">返回主页</button>
        </RouterLink>
      </div>
    </div>
  </div>

  <Footer />
</template>
