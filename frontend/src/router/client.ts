import { router } from "@/router";
import { notice } from "@/utils/notification";
import { appStore as store } from "@/store/global";

export function routerTo(to: string): void {
  if (!store().choiceProject.project_id) {
    notice.warning("请先选择一项实例");
    return;
  }
  store().nowPath = to;
  router.push(to);
}
