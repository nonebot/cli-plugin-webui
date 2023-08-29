import type { Config } from "@/types";

export class BaseConfig {
  title: string;
  description: string;
  name: string;

  constructor(title: string, description: string, name: string) {
    this.title = title;
    this.description = description;
    this.name = name;
  }

  getItem(key: string) {
    const item = localStorage.getItem(`${this.name}:${key}`);
    return item != null ? item : "1";
  }

  setItem(key: string, value: string) {
    localStorage.setItem(`${this.name}:${key}`, value);
  }
}

class WebUIConfig extends BaseConfig {
  constructor() {
    super(
      "Nonebot WebUI",
      "Nonebot (CLI)WebUI 相关设置。（不受实例环境影响）",
      "webui",
    );
  }

  init() {
    const themeColor = this.getItem("theme:color");
    if (!themeColor) {
      const _match = window.matchMedia("(prefers-color-scheme: dark)").matches;
      const color = _match ? "dark" : "light";
      this.setItem("theme:color", color);
    } else {
      document.documentElement.setAttribute("data-theme", themeColor);
    }

    const followSystem = this.getItem("theme:colorFollowSystem");
    if (!followSystem || followSystem === "1") {
      this.setItem("theme:colorFollowSystem", "1");

      const _match = window.matchMedia("(prefers-color-scheme: dark)").matches;
      const color = _match ? "dark" : "light";
      document.documentElement.setAttribute("data-theme", color);

      window
        .matchMedia("(prefers-color-scheme: dark)")
        .addEventListener("change", (event: MediaQueryListEvent) => {
          const color = event.matches ? "dark" : "light";
          this.setItem("theme:color", color);
          document.documentElement.setAttribute("data-theme", color);
        });
    }
  }

  genConfig(): Config {
    const setAction = (config: string, v: string) => {
      switch (config) {
        case "theme:color":
          document.documentElement.setAttribute("data-theme", v);
          this.setItem(config, v);
          break;
        default:
          v = v ? "1" : "0";
          this.setItem(config, v);
      }
    };

    const getAction = (config: string) => {
      return this.getItem(config);
    };

    return {
      title: this.title,
      description: this.description,
      name: this.name,
      setAction: setAction,
      getAction: getAction,
      properties: [
        {
          title: "主题",
          description: "自定义 WebUI 主题。",
          name: "theme",
          properties: [
            {
              title: "颜色",
              description: "指定 WebUI 颜色主题。",
              name: "color",
              default: "light",
              item_type: "string",
              enum: ["light", "dark"],
              configured: this.getItem("theme:color"),
            },
            {
              title: "跟随系统",
              description: "让 WebUI 颜色主题跟随系统。（刷新后生效）",
              name: "colorFollowSystem",
              default: "1",
              item_type: "boolean",
              enum: [],
              configured:
                this.getItem("theme:colorFollowSystem") === "1" ? true : false,
            },
          ],
        },
      ],
    };
  }
}

export const webuiConfig = new WebUIConfig();
