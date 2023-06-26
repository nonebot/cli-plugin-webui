<script setup lang="ts">
import { notifications } from "@/store/app";
import { ref, computed } from "vue";

const openNoticeCard = ref(false);
const noticeTip = ref(0);
const haveNotice = ref(false);
const manyNotice = ref(false);

const changeNoticeCardState = () => {
  openNoticeCard.value = !openNoticeCard.value;
};

const dismissNotice = (id: number | string) => {
  let notices = notifications().notices;
  notices = notices.filter((item) => {
    return item.id !== id;
  });
  notifications().notices = notices;
};

const notices = computed(() => {
  const notices = notifications().notices;
  if (notices.length !== 0) {
    haveNotice.value = true;
    noticeTip.value = notices.length;

    if (notices.length > 3) {
      manyNotice.value = true;
      return notices.slice(0, 3);
    } else {
      manyNotice.value = false;
    }
  } else {
    haveNotice.value = false;
    noticeTip.value = 0;
  }
  return notices;
});
</script>

<template>
  <div class="status-bar">
    <div class="status-bar-left-item">1</div>
    <div class="status-bar-right-item">
      <div
        class="tooltip"
        style="height: 100%"
        :data-tip="`${haveNotice ? noticeTip + '条新通知' : '暂无通知'}`"
      >
        <button class="status-bar-button" @click="changeNoticeCardState()">
          <div class="indicator">
            <span
              :class="{ 'indicator-item badge badge-secondary': haveNotice }"
            ></span>
            <img height="15" width="15" src="/svgs/bell.svg" />
          </div>
        </button>
      </div>

      <div
        :class="{
          'notice-card dropdown dropdown-top dropdown-end': true,
          'dropdown-open': openNoticeCard,
        }"
        style="height: 100%"
      >
        <div
          class="dropdown-content rounded-lg card card-compact lg:w-96 w-screen p-2 shadow"
          style="background: hsl(var(--b2))"
        >
          <div class="card-body">
            <label
              class="btn btn-sm btn-circle absolute right-2 top-2"
              @click="changeNoticeCardState()"
            >
              <img src="/svgs/chevron-down.svg" />
            </label>
            <span class="font-bold">
              <span v-if="haveNotice">
                <span class="countdown">
                  <span :style="`--value:${noticeTip};`"></span>
                </span>
                条新通知
              </span>
              <span v-else> 暂无通知 </span>
            </span>
          </div>

          <div
            v-for="notice in notices"
            :key="notice.id"
            class="alert-card rounded-lg alert shadow-lg"
          >
            <svg
              v-if="notice.level === 'info'"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              class="fill-info stroke-current flex-shrink-0 w-6 h-6"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              ></path>
            </svg>

            <svg
              v-if="notice.level === 'warning'"
              xmlns="http://www.w3.org/2000/svg"
              class="fill-warning stroke-current flex-shrink-0 h-6 w-6"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
              />
            </svg>

            <svg
              v-if="notice.level === 'error'"
              xmlns="http://www.w3.org/2000/svg"
              class="fill-error stroke-current flex-shrink-0 h-6 w-6"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>

            <div>
              <h3 class="font-bold">{{ notice.content }}</h3>
              <div class="text-xs">From {{ notice.header }}</div>
            </div>

            <div>
              <button
                class="btn btn-sm btn-ghost"
                @click="dismissNotice(notice.id)"
              >
                Close
              </button>
            </div>
          </div>
          <p v-if="manyNotice" class="many-notice-tip">仅展示前三条通知</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
@media screen and (max-width: 1280px) {
  .notice-card.dropdown-end .dropdown-content {
    right: -10px;
  }
}

.status-bar-right-item .tooltip:before,
.tooltip-top:before {
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
  height: 22px;
  width: 100%;
  bottom: 0;

  padding-left: 10px;
  padding-right: 10px;

  background: hsl(var(--b3));

  display: flex;
  justify-content: space-between;
  position: fixed;
}

.status-bar > div {
  width: 100%;
}

.status-bar-left-item {
  display: flex;
  align-items: center;
  justify-content: flex-start;
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
