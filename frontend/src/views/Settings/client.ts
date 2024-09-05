import { ModuleConfigFather, ProjectService } from '@/client/api'
import { useNoneBotStore } from '@/stores'

const store = useNoneBotStore()

export const updateConfig = async (
  moduleType: ModuleConfigFather.module_type,
  env: string,
  confType: string,
  k: string,
  v: any
) => {
  if (!store.selectedBot) {
    // TODO: 补全提醒
    return
  }

  await ProjectService.updateProjectConfigV1ProjectConfigUpdatePost(
    moduleType,
    store.selectedBot.project_id,
    {
      env: env,
      conf_type: confType,
      k: k,
      v: v
    }
  ).then(() => {
    // 添加完成后应提示
  })
}
