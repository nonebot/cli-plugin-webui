<script setup lang="ts">
import NoticeDetailCard from "./AppStatusBar/NoticeDetailCard.vue";

import { appStore } from "@/store/global";

const showChoiceProject = () => {
  if (appStore().choiceProject.project_id) {
    return `已选实例 ID：${appStore().choiceProject.project_id}`;
  } else {
    return "未选择实例";
  }
};
</script>

<template>
  <div class="status-bar">
    <div class="status-bar-left-item">
      <div
        :class="{
          'choice-project-item h-full flex items-center pl-1 pr-1': true,
          'bg-success': appStore().choiceProject.is_running,
          'bg-error': !appStore().choiceProject.is_running,
        }"
      >
        <div
          class="tooltip h-full flex items-center gap-1 text-black"
          :data-tip="showChoiceProject()"
        >
          <span class="material-symbols-outlined text-lg"> book </span>
          <div class="text-xs">
            {{
              appStore().choiceProject.project_name
                ? appStore().choiceProject.project_name
                : "unknown"
            }}
          </div>
        </div>
      </div>

      <div class="enabled-env-show h-full flex items-center">
        <div
          class="tooltip h-full flex items-center gap-1"
          :data-tip="`当前环境：${appStore().enabledEnv}`"
        >
          <span class="material-symbols-outlined text-lg"> bolt </span>
          <div class="text-xs">
            {{ appStore().enabledEnv }}
          </div>
        </div>
      </div>
    </div>

    <div class="status-bar-right-item">
      <NoticeDetailCard />
    </div>
  </div>
</template>

<style>
.choice-project-item .tooltip:before,
.choice-project-item .tooltip-top:before {
  transform: translateX(-15%);
}

.enabled-env-show .tooltip:before,
.enabled-env-show .tooltip-top:before {
  transform: translateX(-20%);
}

.status-bar {
  height: 1.5rem;
  width: 100%;
  bottom: 0;

  background: hsl(var(--b3));

  display: flex;
  justify-content: space-between;
  position: fixed;

  z-index: 233;
}

.status-bar > div {
  width: 100%;
}

.status-bar-left-item {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 0.25rem;
}

.status-bar-right-item {
  display: flex;
  align-items: center;
  justify-content: flex-end;
}

.status-bar-button {
  height: 100%;
  width: 25px;

  display: flex;
  align-items: center;
  justify-content: center;
}

.status-bar-button:hover {
  background: hsl(var(--b2));
}
</style>
