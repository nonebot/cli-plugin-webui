<script setup lang="ts">
import NavTab from "./NavTab.vue";

import { settingStore } from "@/store/setting";
</script>

<template>
  <div class="m-2 mt-6 overflow-hidden flex flex-col flex-nowarp">
    <div class="tabs pl-2">
      <a class="tab tab-sm tab-lifted tab-active">Global</a>
    </div>
    <ul class="menu menu-sm w-full bg-base-100 rounded">
      <li>
        <details>
          <summary class="rounded">WebUI</summary>
          <ul>
            <li v-for="config in settingStore().webuiConfigList.properties">
              <details>
                <summary class="rounded">
                  {{ config.title }}
                </summary>
                <ul>
                  <li v-for="detail in config.properties">
                    <a :href="`#webui:${config.name}:${detail.name}`">{{
                      detail.title
                    }}</a>
                  </li>
                </ul>
              </details>
            </li>
          </ul>
        </details>
      </li>
    </ul>

    <Transition>
      <div
        v-if="settingStore().nonebotConfigList.title"
        class="mt-6 overflow-hidden flex flex-col flex-nowarp"
      >
        <NavTab />
        <div class="custom-y-scrollbar overflow-y-auto grow">
          <ul class="menu menu-sm w-full bg-base-100 rounded">
            <li v-if="settingStore().projectMetaConfigList.title">
              <details>
                <summary class="rounded">Project</summary>
                <ul>
                  <li
                    v-for="i in settingStore().projectMetaConfigList.properties"
                  >
                    <details>
                      <summary class="rounded">
                        {{ i.title }}
                      </summary>
                      <ul>
                        <li v-for="detail in i.properties">
                          <a :href="`#project:${i.name}:${detail.name}`">
                            {{ detail.title }}
                          </a>
                        </li>
                      </ul>
                    </details>
                  </li>
                </ul>
              </details>
            </li>
            <li>
              <details>
                <summary class="rounded">Nonebot</summary>
                <ul>
                  <li
                    v-for="config in settingStore().nonebotConfigList
                      .properties"
                  >
                    <details>
                      <summary class="rounded">
                        {{ config.title }}
                      </summary>
                      <ul>
                        <li v-for="detail in config.properties">
                          <a :href="`#nonebot:${config.name}:${detail.name}`">{{
                            detail.title
                          }}</a>
                        </li>
                      </ul>
                    </details>
                  </li>
                </ul>
              </details>
            </li>
            <li v-if="settingStore().pluginConfigList.title">
              <details>
                <summary class="rounded">插件</summary>
                <ul>
                  <li
                    v-for="plugin in settingStore().pluginConfigList.properties"
                  >
                    <details>
                      <summary class="rounded">
                        {{ plugin.title.replace("nonebot_plugin_", "") }}
                      </summary>
                      <ul>
                        <li v-for="detail in plugin.properties">
                          <a
                            :href="`#nonebot_plugin:${plugin.name}:${detail.name}`"
                          >
                            {{ detail.title }}
                          </a>
                        </li>
                      </ul>
                    </details>
                  </li>
                </ul>
              </details>
            </li>
          </ul>
        </div>
      </div>
    </Transition>
  </div>
</template>
