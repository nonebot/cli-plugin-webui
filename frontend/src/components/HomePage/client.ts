import { WebUIWebSocket } from "@/utils/ws";
import { SystemStatsData } from "@/components/HomePage/models";
import { systemStatStore } from "@/store/status";
import { notice } from "@/utils/notification";

export async function handlePlatformPerformanceWebsocket() {
  const store = systemStatStore();

  if (store.websocket?.isConnected()) {
    store.websocket?.client?.close();
  }

  if (!store.websocket) {
    store.websocket = new WebUIWebSocket("/api/performance/ws");
  }

  const maxRetries = 3;
  let retries = 0;
  let connected = false;

  while (!connected && retries < maxRetries) {
    try {
      await store.websocket.connect();
      connected = true;
    } catch (error: any) {
      notice.error(`连接至平台性能检测 WebSocket 失败...(${retries + 1}/${maxRetries})`);
      retries++;
    }
  }

  if (!connected) {
    notice.error("连接至性能性能检测 WebSocket 失败");
    return;
  }

  store.websocket!.client!.onmessage = (event: MessageEvent) => {
    const wsData: SystemStatsData = JSON.parse(event.data);
    const date = new Date();

    if (store.timeList.length >= 100) {
      store.timeList.shift();
    }
    store.timeList.push(`${date.getHours()}:${date.getMinutes()}:${date.getSeconds()}`);

    const convertToMB = (value: number) => value / 1024 / 1024;
    const convertToKbps = (value: number) => value / 1024 / 8;

    const diskSpeeds = wsData.system_stats.disk.speed;
    const netSpeeds = wsData.system_stats.net.speed;

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
