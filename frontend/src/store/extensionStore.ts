import { defineStore } from "pinia";
import api from "@/api";
import { ToastWrapper } from "@/utils/notification";
import { Adapter, Driver, Plugin, SearchTag } from "@/api/schemas";
import type { AxiosError } from "axios";

const notice = new ToastWrapper("Nonebot Store");

export const nonebotExtensionStore = defineStore("nonebotExtensionStore", {
  state() {
    return {
      searchInput: "",
      searchTags: [] as SearchTag[],
      requesting: false,
      storeData: [] as Plugin[] | Adapter[] | Driver[],
      nowPage: 0,
      totalPage: 0,
      totalItem: 0,
      choiceModule: "plugin",
      choiceItem: Object() as Plugin | Adapter | Driver,
      sideNavShow: true,
    };
  },
  actions: {
    assignClass(cls: string) {
      this.choiceModule = cls;
    },

    turnPage(page: number) {
      if (page >= 0) {
        this.nowPage = page;
      } else {
        this.nowPage = 0;
      }

      if (page >= this.totalPage) {
        this.nowPage = this.totalPage;
      }
    },

    async updateData(projectID: string) {
      const isSearch = this.searchInput || this.searchTags.length ? true : false;
      this.requesting = true;
      await api
        .getNoneBotModules(this.choiceModule, this.nowPage, projectID, isSearch)
        .then((resp) => {
          this.requesting = false;
          this.storeData = resp.data.detail;
          this.totalPage = resp.data.total_page;
          this.totalItem = resp.data.total_item;
        })
        .catch((error: AxiosError) => {
          this.requesting = false;
          let reason: string;
          if (error.response) {
            reason = (error.response.data as { detail: string })?.detail;
          } else {
            reason = error.message;
          }
          notice.error(`获取 NoneBot 拓展商店模块 ${this.choiceModule} 失败：${reason}`);
        });
    },

    async updateDataBySearch(projectID: string) {
      this.requesting = true;
      await api
        .searchStore(projectID, this.choiceModule, this.searchTags, this.searchInput)
        .then((resp) => {
          this.requesting = false;
          this.storeData = resp.data.detail;
          this.totalPage = resp.data.total_page;
          this.totalItem = resp.data.total_item;
        })
        .catch((error: AxiosError) => {
          this.requesting = false;
          let reason: string;
          if (error.response) {
            reason = (error.response.data as { detail: string })?.detail;
          } else {
            reason = error.message;
          }
          notice.error(`搜索 NoneBot 拓展商店失败：${reason}`);
        });
    },

    addSearchTag(tag: SearchTag) {
      this.searchTags.push(tag);
    },

    removeSearchTag(tag: SearchTag) {
      const index = this.searchTags.indexOf(tag);
      if (index !== -1) {
        this.searchTags.splice(index, 1);
      }
    },

    switchNavVisible() {
      this.sideNavShow = !this.sideNavShow;
    },
  },
});
