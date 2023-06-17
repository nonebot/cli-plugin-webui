import { router } from "@/router";

export function isDebug(): boolean {
  const isDebugString = localStorage.getItem("isDebug");
  return isDebugString === "1" ? true : false;
}

export function limitContent(text: string, limit: number): string {
  return text.slice(0, limit) + (text.length > limit ? "..." : "");
}

export function routerTo(to: string): void {
  router.push(to);
}

export function isEqual(obj1: any, obj2: any): boolean {
  if (obj1 === obj2) {
    return true;
  }

  if (
    typeof obj1 !== typeof obj2 ||
    Array.isArray(obj1) !== Array.isArray(obj2)
  ) {
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
