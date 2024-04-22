<script setup lang="ts">
import { computed, ref } from 'vue'
import { useNoneBotStore } from '@/stores'
import CreateBotIndex from '@/components/Modals/CreateBot/CreateBotIndex.vue'

const store = useNoneBotStore()

const createBotModal = ref<InstanceType<typeof CreateBotIndex> | null>()

const getBotIsRunning = computed(() => {
  return store.getExtendedBotsList().filter((bot) => bot.is_running).length
})
</script>

<template>
  <CreateBotIndex ref="createBotModal" />

  <div class="grid gap-4">
    <div class="grid gap-4 grid-cols-1 xl:grid-cols-3">
      <div class="col-span-2 card bg-primary/[.2]">
        <div class="card-body justify-center gap-4">
          <h2 class="card-title">欢迎 👋</h2>
          <div class="text-sm">
            <p>这是什么？这是 NoneBot CLI 图形化控制端</p>
            <p>可以干啥？创建并同时管理多个 NoneBot 实例</p>
            <p>
              意见反馈&交流:
              <a class="link" href="https://nonebot.dev/docs/community/contact" target="_blank">
                直达链接
              </a>
            </p>
          </div>
          <div class="card-actions justify-start">
            <button class="btn btn-primary btn-sm font-normal text-white">即刻上手</button>
          </div>
        </div>
      </div>

      <div class="grid gap-4 grid-cols-2 xl:grid-cols-none">
        <div class="stats stats-vertical lg:stats-horizontal">
          <div class="stat">
            <div class="stat-title">已有实例</div>
            <div class="stat-value">{{ store.getExtendedBotsList().length }}</div>
          </div>

          <div class="stat">
            <div class="stat-title">正在运行</div>
            <div class="stat-value">{{ getBotIsRunning }}</div>
          </div>
        </div>

        <div class="card bg-base-200">
          <div class="card-body items-center">
            <p>实例操作</p>
            <div class="card-actions justify-center gap-8">
              <button
                class="btn btn-md lg:btn-sm btn-primary font-normal text-white"
                @click="createBotModal?.openModal()"
              >
                创建实例
              </button>
              <button class="btn btn-md lg:btn-sm btn-primary font-normal btn-outline">
                添加实例
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="grid gap-4 grid-cols-3">
      <div class="stats shadow-md border border-base-200">
        <div class="stat">
          <div class="stat-title">Total Page Views</div>
          <div class="stat-value">89,400</div>
          <div class="stat-desc">21% more than last month</div>
        </div>
      </div>

      <div class="stats shadow-md border border-base-200">
        <div class="stat">
          <div class="stat-title">Total Page Views</div>
          <div class="stat-value">89,400</div>
          <div class="stat-desc">21% more than last month</div>
        </div>
      </div>

      <div class="stats shadow-md border border-base-200">
        <div class="stat">
          <div class="stat-title">Total Page Views</div>
          <div class="stat-value">89,400</div>
          <div class="stat-desc">21% more than last month</div>
        </div>
      </div>
    </div>
    <div></div>
  </div>
</template>
