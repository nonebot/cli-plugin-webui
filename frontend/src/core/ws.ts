import { isDebug } from "./utils";

function getWebSocketURL(path: string): string {
  let host, port;
  if (isDebug()) {
    host = localStorage.getItem("host");
    port = localStorage.getItem("port");
  }
  return `${
    isDebug()
      ? `ws://${host}:${port}`
      : window.location.origin.replace(/^http/, "ws")
  }${path}`;
}

export class WebUIWebSocket {
  path: string;
  client: WebSocket | undefined;

  constructor(path: string) {
    this.path = path;
  }

  init(): WebUIWebSocket {
    const wsURL = getWebSocketURL(this.path);
    this.client = new WebSocket(wsURL);

    return this;
  }

  connect() {
    return new Promise<WebSocket>((resolve, reject) => {
      if (!this.client) {
        reject("WebSocket 未初始化");
        return;
      }
      this.client.addEventListener("open", () => {
        let token = localStorage.getItem("jwtToken");
        if (token === null) {
          token = "";
        }
        this.client!.send(token);

        resolve(this.client as WebSocket);
      });
      this.client.addEventListener("error", (event) => {
        reject(event);
      });
    });
  }
}
