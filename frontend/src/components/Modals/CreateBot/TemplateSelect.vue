<script setup lang="ts">
import { useCreateBotStore } from ".";

const store = useCreateBotStore();

interface OptionItem {
  value: "bootstrap" | "simple";
  text: string;
}

const options: OptionItem[] = [
  {
    value: "bootstrap",
    text: "初学者 / 普通用户",
  },
  {
    value: "simple",
    text: "开发者",
  },
];
</script>

<template>
  <div class="flex flex-col items-center gap-8">
    <div class="flex flex-col justify-center gap-4 w-full">
      <div class="text-center">请选择一个要使用的模板</div>

      <div class="flex flex-col items-center gap-4">
        <button
          v-for="i in options"
          :key="i.text"
          :class="{
            'w-full md:w-1/3 btn btn-primary font-normal text-base-100': true,
            'btn-outline': store.template !== i.value,
          }"
          @click="store.template = i.value"
        >
          {{ i.text }}
        </button>
      </div>

      <div v-if="store.template === 'simple'" class="flex flex-col items-center">
        插件存储位置
        <div class="form-control w-1/2 xl:w-1/3">
          <label class="label cursor-pointer">
            <span class="label-text">在 src 中</span>
            <input
              type="radio"
              name="radio-1"
              class="radio"
              :checked="store.useSrc"
              @click="store.useSrc = true"
            />
          </label>
        </div>
        <div class="form-control w-1/2 xl:w-1/3">
          <label class="label cursor-pointer">
            <span class="label-text">在实例名称命名的文件夹下</span>
            <input
              type="radio"
              name="radio-1"
              class="radio"
              :checked="!store.useSrc"
              @click="store.useSrc = false"
            />
          </label>
        </div>
      </div>
    </div>

    <div class="w-full flex items-center justify-end gap-2">
      <form method="dialog">
        <button class="btn btn-sm">取消</button>
      </form>

      <button
        :class="{
          'btn btn-sm btn-primary text-base-100': true,
          'btn-disabled': !store.template.length,
        }"
        @click="store.step++"
      >
        下一步
      </button>
    </div>
  </div>
</template>
