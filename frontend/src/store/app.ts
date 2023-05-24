import { defineStore } from "pinia";
import { NoticeDetail } from "@/core/notification";

export const GlobalStore = defineStore("globalStore", {
  state: () => {
    return {
      nowPageName: "",
    };
  },
});

export const Notifications = defineStore("notifications", {
  state: (): { notices: NoticeDetail[] } => {
    return {
      notices: [],
    };
  },
});
