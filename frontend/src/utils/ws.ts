import { isDebug } from ".";

export class WebUIWebSocket {
  path: string;
  client: WebSocket | undefined;

  constructor(path: string) {
    this.path = path;

    const wsURL = this.getWebSocketURL(this.path);
    this.client = new WebSocket(wsURL);
  }

  private getWebSocketURL(path: string): string {
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

  async connect(): Promise<WebSocket> {
    return new Promise<WebSocket>((resolve, reject) => {
      if (!this.client) {
        reject("WebSocket 未初始化");
        return;
      }
      this.client.addEventListener("open", () => {
        let token = localStorage.getItem("jwtToken");
        if (!token) {
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

  isConnected(): boolean {
    return this.client?.readyState === WebSocket.OPEN;
  }
}
