import { defineStore } from "pinia";
import { WebUIWebSocket } from "@/utils/ws";

export const systemStatStore = defineStore("systemStatStore", {
  state() {
    return {
      websocket: null as WebUIWebSocket | null,
      diskReadSpeedList: Array(100).fill(0) as number[],
      diskWriteSpeedList: Array(100).fill(0) as number[],
      netSentSpeedList: Array(100).fill(0) as number[],
      netRecvSpeedList: Array(100).fill(0) as number[],
      timeList: Array(100).fill(0) as string[],
    };
  },
});

export const projectStatStore = defineStore("projectStatStore", {
  state() {
    return {
      cpuList: Array(100).fill(0) as number[],
      memList: Array(100).fill(0) as number[],
      timeList: Array(100).fill(0) as string[],
    };
  },

  actions: {
    clearList() {
      this.cpuList = Array(100).fill(0) as number[];
      this.memList = Array(100).fill(0) as number[];
      this.timeList = Array(100).fill(0) as string[];
    },
  },
});
