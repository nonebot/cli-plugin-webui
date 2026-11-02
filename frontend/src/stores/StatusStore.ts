import { defineStore } from "pinia";
import { ref } from "vue";

interface StatusItem {
  css: string[];
  text: string;
}

export const useStatusStore = defineStore("statusStore", () => {
  const statusItems = ref<{ [key: string]: StatusItem }>({});

  const update = (id: string, css: string, text: string) => {
    if (!statusItems.value[id]) {
      statusItems.value[id] = { css: [css], text };
    }

    statusItems.value[id].css = [css];
    statusItems.value[id].text = text;
  };

  const deleteStatus = (id: string) => {
    delete statusItems.value[id];
  };

  return {
    statusItems,
    update,
    deleteStatus,
  };
});
