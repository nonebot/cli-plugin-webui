import { ref } from "vue";
import { defineStore } from "pinia";
import type { NavItem } from "@/router/client";
import { defaultRoutes } from "@/router/client";

export const useViewHistoryRecorderStore = defineStore("viewHistoryRecorder", () => {
  const viewHistory = ref<NavItem[]>([]);

  const viewHistoryFromLocalStorage = localStorage.getItem("viewHistory");
  if (viewHistoryFromLocalStorage) {
    const storedHistory = JSON.parse(viewHistoryFromLocalStorage);
    viewHistory.value = storedHistory
      .map((name: string) => defaultRoutes.find((route) => route.name === name))
      .filter((item: NavItem | undefined): item is NavItem => item !== undefined);
  }

  const _record = () => {
    localStorage.setItem(
      "viewHistory",
      JSON.stringify(viewHistory.value.map((item) => item.name)),
    );
  };

  const record = (route: NavItem) => {
    viewHistory.value.push(route);
    _record();
  };

  const remove = (route: NavItem) => {
    const index = viewHistory.value.findIndex((item) => item.name === route.name);
    if (index !== -1) {
      viewHistory.value.splice(index, 1);
    }
    _record();
  };

  const move = (from: number, to: number) => {
    const item = viewHistory.value.splice(from, 1)[0];
    viewHistory.value.splice(to, 0, item);
    _record();
  };

  return { viewHistory, record, remove, move };
});
