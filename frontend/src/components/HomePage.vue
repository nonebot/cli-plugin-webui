<script setup lang="ts">
import ProjectOverview from "@/components/HomePage/ProjectOverview.vue";
import ProjectProfile from "@/components/HomePage/ProjectProfile.vue";
import StatDashboard from "@/components/HomePage/StatDashboard.vue";
import LogView from "@/components/HomePage/LogView.vue";
import WelcomeAndGuide from "@/components/HomePage/WelcomeAndGuide.vue";
import ProjectAction from "@/components/HomePage/ProjectAction.vue";

import {
  handlePlatformMonitorWebsocket,
  websocketForPlatformMonitor,
} from "./HomePage/client";
import { onMounted, onUnmounted } from "vue";

onMounted(() => {
  handlePlatformMonitorWebsocket();
});

onUnmounted(() => {
  if (websocketForPlatformMonitor?.state.connected) {
    websocketForPlatformMonitor.close();
  }
});
</script>

<template>
  <div class="overflow-hidden h-full w-full flex flex-col flex-nowarp">
    <div class="overflow-y-auto show-area-scrollbar grow p-4 md:p-6 flex flex-col gap-8">
      <WelcomeAndGuide />

      <ProjectOverview />

      <ProjectAction />

      <div
        class="w-full grid xs:grid-cols-1 md:grid-cols-2 gap-8 !pt-0 !pb-0 sm:p-8 md:p-12 lg:p-16 xl:p-20 2xl:p-28"
      >
        <ProjectProfile />

        <StatDashboard />
      </div>

      <LogView />
    </div>
  </div>
</template>

<style>
.main-word {
  color: hsl(var(--p));
}
</style>
