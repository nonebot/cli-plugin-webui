import { defineStore } from "pinia";
import { NonebotProjectMeta } from "@/api/models";
import { NoticeDetail } from "@/utils/notification";

export const appStore = defineStore("appStore", {
  state: () => {
    return {
      isAuth: false,
      projectList: {} as { [key: string]: NonebotProjectMeta },
      choiceProject: Object() as NonebotProjectMeta,
      enabledEnv: ".env",
      nowPath: "/",
    };
  },
  actions: {
    projectIsRunning() {
      this.choiceProject.is_running = true;
    },

    projectIsStop() {
      this.choiceProject.is_running = false;
    },
  },
});

export const noticeStore = defineStore("noticeStore", {
  state: (): { notices: NoticeDetail[] } => {
    return {
      notices: [],
    };
  },
});
