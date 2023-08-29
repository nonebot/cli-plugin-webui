<script setup lang="ts">
import RobotIcon from "@/components/Icons/RobotIcon.vue";
import FlashOnIcon from "@/components/Icons/FlashOnIcon.vue";
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
          <RobotIcon class="h-4 w-4 mr-1" />
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
          <FlashOnIcon class="h-4 w-4" />
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
@media screen and (max-width: 1280px) {
  .notice-card.dropdown-end .dropdown-content {
    right: -10px;
  }
}

.choice-project-item .tooltip:before,
.choice-project-item .tooltip-top:before {
  transform: translateX(-15%);
}

.enabled-env-show .tooltip:before,
.enabled-env-show .tooltip-top:before {
  transform: translateX(-20%);
}

.notice-item .tooltip:before,
.notice-item .tooltip-top:before {
  left: -50%;
}

.status-bar-button .indicator :where(.indicator-item) {
  right: 4px;
  top: 2px;
}

.status-bar-button .badge {
  height: 6px;
  padding-left: 2px;
  padding-right: 2px;
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

.alert-card {
  margin-top: 5px;
  background: hsl(var(--b1));
}

.many-notice-tip {
  font-size: 0.875rem;
  line-height: 1.25rem;

  opacity: 0.5;

  margin-top: 5px;

  text-align: center;
}
</style>
