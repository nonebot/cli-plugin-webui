import { getURL } from "@/utils";
import { PlatformInfo } from "@/components/HomePage/schemas";
import { systemStatStore } from "@/store/status";
import { notice } from "@/utils/notification";
import { API } from "@/api";
import { appStore } from "@/store/global";
import { AxiosError } from "axios";

export const api = new API();
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

export let websocketForPlatformMonitor: WebSocket;

export function handlePlatformMonitorWebsocket() {
  const store = systemStatStore();

  websocketForPlatformMonitor?.close();

  websocketForPlatformMonitor = new WebSocket(getURL("/api/status/platform/ws", true));

  websocketForPlatformMonitor.onopen = () => {
    const token = localStorage.getItem("jwtToken") ?? "";
    websocketForPlatformMonitor.send(token);
  };

  websocketForPlatformMonitor.onmessage = (event: MessageEvent) => {
    const wsData: PlatformInfo = JSON.parse(event.data);
    const date = new Date();

    if (store.timeList.length >= 100) {
      store.timeList.shift();
    }
    store.timeList.push(`${date.getHours()}:${date.getMinutes()}:${date.getSeconds()}`);

    const convertToMB = (value: number) => value / 1024 / 1024;
    const convertToKbps = (value: number) => value / 1024 / 8;

    const diskSpeeds = wsData.disk.speed;
    const netSpeeds = wsData.net.speed;

    const updateList = (list: number[], speed: number) => {
      if (list.length >= 100) {
        list.shift();
      }
      list.push(speed);
    };

    updateList(store.diskReadSpeedList, convertToMB(diskSpeeds[0]));
    updateList(store.diskWriteSpeedList, convertToMB(diskSpeeds[1]));
    updateList(store.netSentSpeedList, convertToKbps(netSpeeds[0]));
    updateList(store.netRecvSpeedList, convertToKbps(netSpeeds[1]));
  };
}

export async function getProjectList() {
  await api
    .getProjectList()
    .then((resp) => {
      appStore().projectList = resp.detail;
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
