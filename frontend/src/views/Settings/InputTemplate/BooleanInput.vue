<script setup lang="ts">
import type { ModuleConfigChild, ModuleConfigFather } from '@/client/api'
import { updateConfig } from '../client'
import { useNoneBotStore } from '@/stores'

const store = useNoneBotStore()

defineProps<{ moduleType: ModuleConfigFather.module_type; data: ModuleConfigChild }>()
</script>

<template>
  <input
    type="checkbox"
    class="toggle toggle-sm"
    :checked="data.configured"
    @click="
      async () => {
        await updateConfig(
          moduleType,
          store.enabledEnv,
          data.conf_type,
          data.name,
          !data.configured
        ).then(() => {
          data.configured! = !data.configured
        })
      }
    "
  />
</template>
