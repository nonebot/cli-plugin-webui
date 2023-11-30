import { SimpleInfo } from "@/api/schemas";

export function isDebug(): boolean {
  const isDebugString = localStorage.getItem("isDebug");
  return isDebugString === "1" ? true : false;
}

export function limitContent(text: string, limit: number): string {
  return text.slice(0, limit) + (text.length > limit ? "..." : "");
}

export function isEqual(obj1: any, obj2: any): boolean {
  if (obj1 === obj2) {
    return true;
  }

  if (typeof obj1 !== typeof obj2 || Array.isArray(obj1) !== Array.isArray(obj2)) {
    return false;
  }

  const key1 = Object.keys(obj1);
  const key2 = Object.keys(obj2);

  if (key1.length !== key2.length) {
    return false;
  }

  for (let key of key1) {
    if (!isEqual(obj1[key], obj2[key])) {
      return false;
    }
  }

  return true;
}

export function parseStringArray(data: string[]): string {
  if (data.length !== 0 && Array.isArray(data)) {
    return data.join("、");
  } else {
    return "unknown";
  }
}

export function parseSimpleInfo(data: SimpleInfo[]): string {
  if (data.length !== 0 && Array.isArray(data)) {
    return data.map((item) => item.name).join("、");
  } else {
    return "unknown";
  }
}

export function getURL(path: string, isWebSocket?: boolean, params?: any): string {
  let href;
  if (isDebug()) {
    href = `http://${localStorage.getItem("host")}:${localStorage.getItem(
      "port",
    )}/${path}`;
  } else {
    href = location.href;
  }
  const url = new URL(path, href);
  if (isWebSocket) {
    url.protocol = url.protocol === "https:" ? "wss:" : "ws:";
  }
  if (params) {
    Object.keys(params).forEach((key) => {
      url.searchParams.append(key, params[key]);
    });
  }
  return url.href;
}
