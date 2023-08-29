import { ToastOptions, ToastTheme, Id, Content, toast } from "vue3-toastify";
import { noticeStore } from "@/store/global";

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

  private getNowTheme(): ToastTheme | undefined {
    return document.documentElement.getAttribute("data-theme") as
      | ToastTheme
      | undefined;
  }

  private addToNotifications(
    type: "info" | "warning" | "error",
    id: Id,
    content: any,
  ): void {
    rawNotice = noticeStore().notices;
    rawNotice = rawNotice || [];
    rawNotice.push({
      id: id,
      header: this.header,
      content: content,
      level: type,
    });
    noticeStore().notices = rawNotice;
  }

  info(content: Content, options?: ToastOptions): void {
    this.addToNotifications(
      "info",
      toast.info(content, { theme: this.getNowTheme(), ...options }),
      content,
    );
  }

  warning(content: Content, options?: ToastOptions): void {
    this.addToNotifications(
      "warning",
      toast.warn(content, { theme: this.getNowTheme(), ...options }),
      content,
    );
  }

  error(content: Content, options?: ToastOptions): void {
    this.addToNotifications(
      "error",
      toast.error(content, { theme: this.getNowTheme(), ...options }),
      content,
    );
  }

  success(content: Content, options?: ToastOptions): void {
    toast.success(content, { theme: this.getNowTheme(), ...options });
  }
}
