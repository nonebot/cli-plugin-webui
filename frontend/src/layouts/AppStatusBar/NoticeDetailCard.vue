<script setup lang="ts">
import { ref, computed } from "vue";
import { noticeStore } from "@/store/global";

const openNoticeCard = ref(false);
const noticeTip = ref(0);
const haveNotice = ref(false);
const manyNotice = ref(false);

const notices = computed(() => {
  const notices = noticeStore().notices;
  if (notices.length) {
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

const changeNoticeCardState = () => {
  openNoticeCard.value = !openNoticeCard.value;
};

const dismissNotice = (id: number | string) => {
  let notices = noticeStore().notices;
  notices = notices.filter((item) => {
    return item.id !== id;
  });
  noticeStore().notices = notices;
};
</script>

<template>
  <div class="notice-item h-full flex items-center">
    <div
      class="tooltip h-full"
      :data-tip="`${haveNotice ? noticeTip + '条新通知' : '暂无通知'}`"
    >
      <button class="status-bar-button" @click="changeNoticeCardState()">
        <div class="indicator">
          <span
            :class="{
              'badge h-1.5 pl-0.5 pr-0.5 badge-primary indicator-item': haveNotice,
            }"
          ></span>
          <span class="material-symbols-outlined text-lg leading-3"> notifications </span>
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
        class="dropdown-content rounded-lg card card-compact lg:w-96 w-screen p-2 shadow-lg"
        style="background: hsl(var(--b2))"
      >
        <div class="card-body">
          <label
            class="btn btn-sm btn-circle absolute right-2 top-2"
            @click="changeNoticeCardState()"
          >
            <span class="material-symbols-outlined text-2xl"> expand_more </span>
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
          <span
            v-if="notice.level === 'info'"
            class="material-symbols-outlined text-info"
          >
            info
          </span>

          <span
            v-if="notice.level === 'warning'"
            class="material-symbols-outlined text-warning"
          >
            warning
          </span>

          <span
            v-if="notice.level === 'error'"
            class="material-symbols-outlined text-error"
          >
            error
          </span>

          <div>
            <h3 class="font-bold">{{ notice.content }}</h3>
            <div class="text-xs">From {{ notice.header }}</div>
          </div>

          <div>
            <button class="btn btn-sm btn-ghost" @click="dismissNotice(notice.id)">
              Close
            </button>
          </div>
        </div>
        <p v-if="manyNotice" class="many-notice-tip">仅展示前三条通知</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.material-symbols-outlined {
  font-variation-settings:
    "FILL" 0,
    "wght" 400,
    "GRAD" 0,
    "opsz" 48;
}

@media screen and (max-width: 1280px) {
  .notice-card .dropdown-end .dropdown-content {
    right: -10px;
  }
}

.indicator :where(.indicator-item) {
  right: 4px;
  top: 2px;
}

.notice-item .tooltip:before,
.notice-item .tooltip-top:before {
  left: -50%;
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
