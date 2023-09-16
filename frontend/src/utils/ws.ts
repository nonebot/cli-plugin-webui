import { defineStore } from "pinia";
import { isDebug } from ".";
import { reactive } from "vue";

export function getWebSocketURL(path: string): string {
  let host, port;
  if (isDebug()) {
    host = localStorage.getItem("host");
    port = localStorage.getItem("port");
  }
  return `${
    isDebug() ? `ws://${host}:${port}` : window.location.origin.replace(/^http/, "ws")
  }${path}`;
}

interface State {
  connected: boolean;
}

const stateStore = defineStore("stateStore", () => {
  const state: State = reactive({
    connected: false,
  });

  return state;
});

export class WebsocketWrapper {
  client: WebSocket;
  state: ReturnType<typeof stateStore>;

  constructor(path: string) {
    this.client = new WebSocket(getWebSocketURL(path));
    this.state = stateStore();
  }

  connect() {
    this.client.addEventListener("open", () => {
      let token = localStorage.getItem("jwtToken");
      if (!token) {
        token = "";
      }
      this.client?.send(token);

      if (this.client.readyState === WebSocket.OPEN) {
        this.state.connected = true;
      }
    });

    this.client.addEventListener("close", () => {
      this.state.connected = false;
    });
  }

  close(code: number = 1000, reason?: string) {
    this.client?.close(code, reason);
  }
}
