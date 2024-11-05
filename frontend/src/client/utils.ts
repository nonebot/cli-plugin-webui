import { client } from "./api";

export const covertTimestampToDateString = (
  timestamp: string,
  options: any = {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  },
) => {
  const fixedTimestamp = Number(timestamp) * 1000;
  const date = new Date(fixedTimestamp);
  return date.toLocaleDateString(navigator.language, options);
};

export const limitContentShow = (content: string, limit: number) => {
  if (content.length <= limit) {
    return content;
  }
  return content.slice(0, limit) + "...";
};

export const generateURLForWebUI = (path: string, isWebsocket = false) => {
  const base = client.getConfig().baseUrl!;
  const protocol = isWebsocket ? "ws" : "http";
  return `${protocol}://${base}${path}`;
};

export const sleep = (ms: number) => {
  return new Promise((resolve) => setTimeout(resolve, ms));
};
