<script setup lang="ts">
import type { ConfigType, ModuleConfigChild, ModuleType } from "@/client/api";
import { updateConfig } from "../client";

defineProps<{ moduleType: ModuleType | ConfigType; data: ModuleConfigChild }>();
</script>

<template>
  <input
    type="checkbox"
    class="toggle toggle-sm"
    :checked="data.configured as boolean"
    @click="
      async () => {
        await updateConfig(moduleType, data.conf_type, data.name, !data.configured).then(
          () => {
            data.configured! = !data.configured;
          },
        );
      }
    "
  />
</template>
