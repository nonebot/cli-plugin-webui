<script setup lang="ts">
import { globalStore } from "@/store/app";

const toggleMenu = () => {
  globalStore().showMenu = !globalStore().showMenu;
};
</script>

<template>
  <div
    class="z-30 fixed w-full h-10 border-b pl-2 pr-2 hidden max-[390px]:flex items-center bg-base-100"
  >
    <div class="m-2" role="button" @click="toggleMenu()">
      <svg
        class="swap-off fill-current"
        xmlns="http://www.w3.org/2000/svg"
        width="28"
        height="28"
        viewBox="0 0 512 512"
      >
        <path
          d="M64,384H448V341.33H64Zm0-106.67H448V234.67H64ZM64,128v42.67H448V128Z"
        />
      </svg>
    </div>
    <div>test</div>
  </div>
</template>
