<script setup lang="ts">
import type { ModuleConfigFather } from '@/client/api'
import StringInput from './InputTemplate/StringInput.vue'
import BooleanInput from './InputTemplate/BooleanInput.vue'
import ArrayInput from './InputTemplate/ArrayInput.vue'
import NumberInput from './InputTemplate/NumberInput.vue'
import SelectInput from './InputTemplate/SelectInput.vue'

const props = defineProps<{ data: ModuleConfigFather }>()
</script>

<template>
  <div class="w-full p-6 bg-base-200 rounded-box flex flex-col gap-4">
    <!-- Title with desc -->
    <div class="flex flex-col gap-2">
      <h2 class="text-xl font-semibold">{{ props.data.title }}</h2>
      <div class="text-sm opacity-50 text-base-content">{{ props.data.description }}</div>
      <div class="bg-base-content/10 h-[1px]"></div>
    </div>

    <!-- config area -->
    <div v-for="i in props.data.properties" :key="i.name" class="flex flex-col gap-1">
      <!-- config desc -->
      <div class="flex items-center gap-1">
        <div class="text-opacity-80 text-base-content font-medium">
          {{ i.title }}
        </div>

        <span
          v-if="i.description"
          class="material-symbols-outlined text-base tooltip"
          :data-tip="i.description"
        >
          info
        </span>
      </div>

      <div v-if="i.latest_change" class="text-xs text-opacity-50 text-base-content">
        最后修改于：{{ i.latest_change }}
      </div>

      <SelectInput v-if="i.enum" :data="i" :module-type="data.module_type" />
      <StringInput
        v-else-if="['string', 'object'].indexOf(i.conf_type) !== -1"
        :data="i"
        :module-type="data.module_type"
      />
      <BooleanInput
        v-else-if="i.conf_type === 'boolean'"
        :data="i"
        :module-type="data.module_type"
      />
      <ArrayInput v-else-if="i.conf_type === 'array'" :data="i" :module-type="data.module_type" />
      <NumberInput
        v-else-if="i.conf_type === 'integer'"
        :data="i"
        :module-type="data.module_type"
      />
    </div>
  </div>
</template>
