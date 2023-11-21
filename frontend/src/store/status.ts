import { defineStore } from "pinia";

const ARRAY_LENGTH = 100;
const initialArray = Array.from({ length: ARRAY_LENGTH }, () => 0);

interface SystemState {
  diskReadSpeedList: number[];
  diskWriteSpeedList: number[];
  netSentSpeedList: number[];
  netRecvSpeedList: number[];
}

interface ProcessState {
  cpuPercentList: number[];
  memPercentList: number[];
}

interface State {
  system: SystemState;
  process: ProcessState;
  timeList: string[];
}

export const useStatusStore = defineStore("useStatusStore", {
  state: (): State => {
    return {
      system: {
        diskReadSpeedList: [...initialArray],
        diskWriteSpeedList: [...initialArray],
        netSentSpeedList: [...initialArray],
        netRecvSpeedList: [...initialArray],
      },
      process: {
        cpuPercentList: [...initialArray],
        memPercentList: [...initialArray],
      },
      timeList: Array.from({ length: ARRAY_LENGTH }, () => "00:00:00"),
    };
  },

  actions: {
    clearProcessList() {
      this.process.cpuPercentList = [...initialArray];
      this.process.memPercentList = [...initialArray];
    },
  },
});
