import { Notifications } from "@/store/app";
import { ToastOptions } from "vue3-toastify";
import { Id } from "vue3-toastify";
import { Content } from "vue3-toastify";
import { toast } from "vue3-toastify";

export interface NoticeDetail {
  id: number | string;
  header: string;
  content: string;
  level: "info" | "warning" | "error";
}

let rawNotice: NoticeDetail[] = [];

export class ToastWrapper {
  header: string;

  constructor(header: string) {
    this.header = header;
  }

  private addToNotifications(
    type: "info" | "warning" | "error",
    id: Id,
    content: any,
  ): void {
    rawNotice = Notifications().notices;
    rawNotice = rawNotice || [];
    rawNotice.push({
      id: id,
      header: this.header,
      content: content,
      level: type,
    });
    Notifications().notices = rawNotice;
  }

  info(content: Content, options?: ToastOptions): void {
    this.addToNotifications("info", toast.info(content, options), content);
  }

  warn(content: Content, options?: ToastOptions): void {
    this.addToNotifications("warning", toast.warn(content, options), content);
  }

  error(content: Content, options?: ToastOptions): void {
    this.addToNotifications("error", toast.error(content, options), content);
  }

  success(content: Content, options?: ToastOptions): void {
    toast.success(content, options);
  }
}
