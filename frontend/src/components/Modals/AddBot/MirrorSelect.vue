<script setup lang="ts">
import { useAddBotStore } from '.'

const store = useAddBotStore()

interface MirrorItem {
  abbr: string
  url: string
  name: string
}

const mirrors: MirrorItem[] = [
  {
    abbr: 'pypi',
    url: 'https://pypi.org/simple',
    name: 'PyPI'
  },
  {
    abbr: 'CERNET',
    url: 'https://mirrors.cernet.edu.cn/pypi/web/simple',
    name: '校园网联合镜像站'
  },
  {
    abbr: 'TUNA',
    url: 'https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple',
    name: '清华大学开源软件镜像站'
  },
  {
    abbr: 'PKU',
    url: 'https://mirrors.pku.edu.cn/pypi/web/simple',
    name: '北京大学开源软件镜像站'
  },
  {
    abbr: 'STSTech CRA',
    url: 'https://mirrors.sustech.edu.cn/pypi/web/simple',
    name: '南方科技大学开源软件镜像站'
  }
]
</script>

<template>
  <div class="flex flex-col items-center gap-4 md:gap-8">
    <div class="flex flex-col justify-center items-center w-full max-w-xs">
      <div class="form-control w-full">
        <div class="label">
          <span class="label-text">请选择:</span>
        </div>
        <select class="select select-bordered" v-model="store.pythonMirror">
          <option v-for="mirror in mirrors" :value="mirror.url" :key="mirror.name">
            {{ mirror.abbr }} - {{ mirror.name }}
          </option>
        </select>

        <div class="label">
          <span class="label-text">或自行填写:</span>
        </div>
        <input
          type="text"
          placeholder="请输入"
          class="input input-bordered"
          v-model="store.pythonMirror"
        />
      </div>

      <div role="alert" class="mt-4 alert w-full max-w-xs">
        <span class="material-symbols-outlined text-info"> info </span>
        <div>
          更多镜像请前往:
          <a class="link" target="_blank" href="https://help.mirrors.cernet.edu.cn/pypi/"
            >MirrorZ</a
          >
        </div>
      </div>
    </div>

    <div class="w-full flex justify-between">
      <button class="btn btn-sm btn-primary text-base-100" @click="store.step--">上一步</button>
      <button
        :class="{
          'btn btn-sm btn-primary text-base-100': true,
          'btn-disabled': !store.pythonMirror.length
        }"
        @click="store.step++"
      >
        下一步
      </button>
    </div>
  </div>
</template>
