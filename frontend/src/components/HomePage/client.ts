import { getURL } from "@/utils";
import type { StatusInfo } from "@/components/HomePage/schemas";
import { useStatusStore } from "@/store/status";
import { notice } from "@/utils/notification";
import api from "@/api";
import { appStore } from "@/store/global";
import type { AxiosError } from "axios";

export const mirrorList = [
  { name: "PyPI", url: "https://pypi.org/simple" },
  {
    name: "校园网联合镜像站",
    url: "https://mirrors.cernet.edu.cn/pypi/web/simple",
  },
  { name: "清华大学", url: "https://pypi.tuna.tsinghua.edu.cn/simple" },
  {
    name: "北京外国语大学",
    url: "https://mirrors.bfsu.edu.cn/pypi/web/simple",
  },
  { name: "腾讯云", url: "https://mirrors.cloud.tencent.com/pypi/simple" },
  { name: "中科院", url: "https://pypi.mirrors.ustc.edu.cn/simple" },
  { name: "豆瓣", url: "https://pypi.douban.com/simple" },
];

export let statusWebSocket: WebSocket | null = null;

export function handleStatusWebsocket() {
  const store = useStatusStore();

  statusWebSocket?.close();

  statusWebSocket = new WebSocket(getURL("/api/v1/status/ws", true));

  statusWebSocket.onopen = () => {
    const token = localStorage.getItem("jwtToken") ?? "";
    statusWebSocket?.send(token);
  };

  statusWebSocket.onclose = () => {
    statusWebSocket = null;
  };

  statusWebSocket.onmessage = (event: MessageEvent) => {
    const wsData: StatusInfo = JSON.parse(event.data);
    const date = new Date();

    const updateList = (list: any[], item: any) => {
      if (list.length >= 100) {
        list.shift();
      }
      list.push(item);
    };

    updateList(
      store.timeList,
      `${date.getHours()}:${date.getMinutes()}:${date.getSeconds()}`,
    );

    const convertToMB = (value: number) => value / 1024 / 1024;
    const convertToKbps = (value: number) => value / 1024 / 8;

    const diskSpeeds = wsData.system.disk.speed;
    const netSpeeds = wsData.system.net.speed;

    updateList(store.system.diskReadSpeedList, convertToMB(diskSpeeds[0]));
    updateList(store.system.diskWriteSpeedList, convertToMB(diskSpeeds[1]));
    updateList(store.system.netSentSpeedList, convertToKbps(netSpeeds[0]));
    updateList(store.system.netRecvSpeedList, convertToKbps(netSpeeds[1]));

    if (wsData.process && wsData.process.performance) {
      updateList(
        store.process.cpuPercentList,
        Number(wsData.process.performance.cpu.toFixed(3)) * 100,
      );
      updateList(
        store.process.memPercentList,
        Number(wsData.process.performance.mem.toFixed(3)) * 100,
      );
    }
  };
}

export async function getProjectList() {
  await api
    .getProjectList()
    .then((resp) => {
      appStore().projectList = resp.data.detail;
    })
    .catch((error: AxiosError) => {
      let reason: string;
      if (error.response) {
        reason = (error.response.data as { detail: string })?.detail;
      } else {
        reason = error.message;
      }
      notice.error(`获取实例列表失败：${reason}`);
    });
}
