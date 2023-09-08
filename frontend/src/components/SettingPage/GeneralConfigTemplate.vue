<script setup lang="ts" generic="T extends Config">
import SettingIcon from "@/components/Icons/SettingIcon.vue";

import NumberInput from "./DataInputTemplate/NumberInput.vue";
import StringOrObjectInput from "./DataInputTemplate/StringOrObjectInput.vue";
import BooleanInput from "./DataInputTemplate/BooleanInput.vue";
import SelectInput from "./DataInputTemplate/SelectInput.vue";

import { marked } from "marked";
import { settingStore } from "@/store/setting";
import type { Config } from "@/types";
import { computed } from "vue";
import ArrayInput from "./DataInputTemplate/ArrayInput.vue";

const props = defineProps<{ config: T }>();
const config = computed(() => {
  return props.config;
});
</script>

<template>
  <div class="p-4 border-t hover:bg-base-200">
    <div class="setting-board-title">{{ config.title }}</div>
    <div
      class="setting-board-desc markdown"
      v-html="marked.parse(config.description ? config.description : '')"
    ></div>
  </div>
  <div>
    <div v-for="father in config.properties">
      <div class="setting-board-father p-4 hover:bg-base-200">
        <div class="setting-board-father-title">{{ father.title }}</div>
        <div
          class="setting-board-desc markdown"
          v-html="marked.parse(father.description ? father.description : '')"
        ></div>
      </div>
      <div class="setting-board-father-content">
        <div
          v-for="child in father.properties"
          :class="{
            'setting-board-child p-4 hover:bg-base-200': true,
            'bg-base-200': settingStore().isActive(
              `${config.name}:${father.name}:${child.name}`,
            ),
          }"
          :id="`${config.name}:${father.name}:${child.name}`"
          @click="settingStore().setActive(`${config.name}:${father.name}:${child.name}`)"
        >
          <div
            :id="`${config.title}:${father.title}:${child.title}`"
            class="setting-board-child-title"
          >
            {{ father.title.replace("nonebot_plugin_", "") }}:<span>{{
              child.title
            }}</span>

            <div
              :class="{
                'more-action dropdown': true,
                '!opacity-100': settingStore().isActive(
                  `${config.name}:${father.name}:${child.name}`,
                ),
              }"
            >
              <label tabindex="0" class="tooltip tooltip-right" data-tip="更多操作">
                <SettingIcon class="h-5 w-5" />
              </label>
              <ul
                tabindex="0"
                class="dropdown-content rounded z-[1] menu p-2 shadow bg-base-100 rounded-lg w-52"
              >
                <li :class="{ disabled: !child.default }">
                  <a
                    @click="
                      () => {
                        if (child.default) {
                          config.setAction(
                            `${father.name}:${child.name}`,
                            child.default,
                            child.item_type,
                          );
                        }
                      }
                    "
                    >恢复默认值</a
                  >
                </li>
                <!-- <li><a>在 dotenv 中编辑</a></li> -->
              </ul>
            </div>
          </div>
          <div
            class="setting-board-desc markdown"
            v-html="marked.parse(child.description ? child.description : '')"
          ></div>
          <div class="setting-board-child-content">
            <div v-if="child.latest_change" class="py-2 text-xs">
              最后修改于：{{ child.latest_change }}
            </div>

            <NumberInput
              v-if="
                (child.item_type === 'number' || child.item_type === 'integer') &&
                !child.enum.length
              "
              :input-i-d="`${father.name}:${child.name}`"
              :configured="child.configured"
              :set-action="config.setAction"
              :exclusive-minimum="child.exclusiveMinimum"
              :minimum="child.minimum"
              :exclusive-maximum="child.exclusiveMaximum"
              :maximum="child.maximum"
            />

            <StringOrObjectInput
              v-if="
                (child.item_type === 'string' || child.item_type === 'object') &&
                !child.enum.length
              "
              :input-i-d="`${father.name}:${child.name}`"
              :need-type="child.item_type"
              :configured="child.configured"
              :set-action="config.setAction"
            />

            <SelectInput
              v-if="child.item_type === 'string' && child.enum?.length"
              :input-i-d="`${father.name}:${child.name}`"
              :literal="child.enum"
              :configured="child.configured"
              :set-action="config.setAction"
            />

            <ArrayInput
              v-if="child.item_type === 'array'"
              :input-i-d="`${father.name}:${child.name}`"
              :literal="child.enum"
              :configured="child.configured"
              :set-action="config.setAction"
            />

            <BooleanInput
              v-if="child.item_type === 'boolean'"
              :input-i-d="`${father.name}:${child.name}`"
              :configured="child.configured"
              :set-action="config.setAction"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
