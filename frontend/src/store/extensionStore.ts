import { defineStore } from "pinia";
import { API } from "@/api";
import { ToastWrapper } from "@/utils/notification";
import { Adapter, Driver, Plugin } from "@/api/models";

const api = new API();

export const nonebotExtensionStore = defineStore("nonebotExtensionStore", {
  state() {
    return {
      searchInput: "",
      requesting: false,
      storeData: [] as Plugin[] | Adapter[] | Driver[],
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

    async updateData(projectID: string, page: number) {
      const log = new ToastWrapper("Nonebot Store");
      const isSearch = this.searchInput ? true : false;
      this.requesting = true;
      if (this.choiceClass === "plugin") {
        await api
          .getPlugins(page, isSearch, projectID)
          .then((resp) => {
            this.requesting = false;
            this.totalPage = resp.total_page;
            this.totalItem = resp.total_item;
            this.storeData = resp.data;
          })
          .catch((error) => {
            this.requesting = false;
            log.error(`获取插件列表失败：${error}`);
          });
      }

      if (this.choiceClass === "adapter") {
        await api
          .getAdapters(page, isSearch, projectID)
          .then((resp) => {
            this.requesting = false;
            this.storeData = resp.data;
            this.totalPage = resp.total_page;
            this.totalItem = resp.total_item;
          })
          .catch((error) => {
            this.requesting = false;
            log.error(`获取适配器列表失败：${error}`);
          });
      }

      if (this.choiceClass === "driver") {
        await api
          .getDrivers(page, isSearch, projectID)
          .then((resp) => {
            this.requesting = false;
            this.storeData = resp.data;
            this.totalPage = resp.total_page;
            this.totalItem = resp.total_item;
          })
          .catch((error) => {
            this.requesting = false;
            log.error(`获取驱动器列表失败：${error}`);
          });
      }
    },

    async updateDataBySearch(projectID: string) {
      this.requesting = true;

      const log = new ToastWrapper("Nonebot Store");
      await api
        .searchStore(projectID, this.choiceClass, this.searchInput)
        .then((resp) => {
          this.requesting = false;
          this.storeData = resp.data;
          this.totalPage = resp.total_page;
          this.totalItem = resp.total_item;
        })
        .catch((error) => {
          this.requesting = false;
          log.error(`搜索商店失败：${error}`);
        });
    },

    async refresh() {
      this.requesting = true;
      const log = new ToastWrapper("Nonebot Store");
      await api
        .refreshStore()
        .then(() => {
          this.requesting = false;
        })
        .catch((error) => {
          this.requesting = false;
          log.error(`Nonebot 商店刷新失败：${error}`);
        });
    },

    switchNavVisible() {
      this.sideNavShow = !this.sideNavShow;
    },
  },
});
