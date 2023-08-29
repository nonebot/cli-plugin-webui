import { defineStore } from "pinia";
import { Config } from "@/types";

export const settingStore = defineStore("settingStore", {
  state() {
    return {
      activeItem: "",
      webuiConfigList: Object() as Config,
      projectMetaConfigList: Object() as Config,
      nonebotConfigList: Object() as Config,
      pluginConfigList: Object() as Config,
      sideNavShow: true,
    };
  },
  actions: {
    isActive(item: string) {
      return item === this.activeItem;
    },

    setActive(item: string) {
      this.activeItem = item;
    },

    switchNavVisible() {
      this.sideNavShow = !this.sideNavShow;
    },
  },
});
