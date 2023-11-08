import { defineStore } from "pinia";
import { NoneBotProjectMeta } from "@/api/schemas";
import { NoticeDetail } from "@/utils/notification";

export const appStore = defineStore("appStore", {
  state: () => {
    return {
      isAuth: false,
      projectList: {} as { [key: string]: NoneBotProjectMeta },
      choiceProject: Object() as NoneBotProjectMeta,
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
