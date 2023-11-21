import { defineStore } from "pinia";
import api from "@/api";
import { ToastWrapper } from "@/utils/notification";
import { Adapter, Driver, Plugin } from "@/api/schemas";
import type { AxiosError } from "axios";

const notice = new ToastWrapper("Nonebot Store");

export const nonebotExtensionStore = defineStore("nonebotExtensionStore", {
  state() {
    return {
      searchInput: "",
      requesting: false,
      storeData: [] as Plugin[] | Adapter[] | Driver[],
      nowPage: 0,
      totalPage: 0,
      totalItem: 0,
      choiceClass: "plugin",
      choiceItem: Object() as Plugin | Adapter | Driver,
      sideNavShow: true,
    };
  },
  actions: {
    assignClass(cls: string) {
      this.choiceClass = cls;
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
      const isSearch = this.searchInput ? true : false;
      this.requesting = true;
      await api
        .getNoneBotModules(this.choiceClass, this.nowPage, projectID, isSearch)
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
          notice.error(`获取 NoneBot 拓展商店模块 ${this.choiceClass} 失败：${reason}`);
        });
    },

    async updateDataBySearch(projectID: string) {
      this.requesting = true;
      await api
        .searchStore(projectID, this.choiceClass, this.searchInput)
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

    // async refresh() {
    //   this.requesting = true;
    //   await api
    //     .refreshStore()
    //     .then(() => {
    //       this.requesting = false;
    //     })
    //     .catch((error: AxiosError) => {
    //       this.requesting = false;
    //       let reason: string;
    //       if (error.response) {
    //         reason = (error.response.data as { detail: string })?.detail;
    //       } else {
    //         reason = error.message;
    //       }
    //       notice.error(`NoneBot 拓展商店刷新失败：${reason}`);
    //     });
    // },

    switchNavVisible() {
      this.sideNavShow = !this.sideNavShow;
    },
  },
});
