<script setup lang="ts">
import StoreSideNav from "@/components/NonebotStore/StoreSideNav.vue";
import ExtensionShowArea from "@/components/NonebotStore/ExtensionShowArea.vue";
import { nonebotExtensionStore } from "@/store/extensionStore";
import { appStore } from "@/store/global";

if (appStore().choiceProject.project_id) {
  nonebotExtensionStore().updateData(appStore().choiceProject.project_id);
}
</script>

<template>
  <div class="overflow-hidden h-full w-full flex">
    <div
      :class="{
        'z-10 h-full w-full top-0 left-0 shrink-0 flex md:w-72 visible md:!visible absolute md:relative': true,
        'transition-all ease-in-out': true,
        '!bg-inherit !invisible': !nonebotExtensionStore().sideNavShow,
      }"
      style="background-color: hsl(var(--n) / 0.3)"
    >
      <StoreSideNav />

      <button
        :class="{
          'h-full w-full flex md:hidden opacity-30': true,
          '!hidden': !nonebotExtensionStore().sideNavShow,
        }"
        @click="nonebotExtensionStore().switchNavVisible()"
      ></button>
    </div>

    <ExtensionShowArea />
  </div>
</template>
