import { ModuleConfigFather, ProjectService } from '@/client/api'
import { useNoneBotStore } from '@/stores'
import { useToastStore } from '@/stores/ToastStorage'

const store = useNoneBotStore()
const toast = useToastStore()

export const updateConfig = async (
  moduleType: ModuleConfigFather.module_type,
  env: string,
  confType: string,
  k: string,
  v: any
) => {
  if (!store.selectedBot) {
    toast.add('warning', '未选择实例', '', 5000)
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
  )
    .then(() => {
      toast.add('success', '更新成功', '', 5000)
    })
    .catch((err) => {
      let detail = ''
      if (err.body) {
        detail = err.body.detail
      } else {
        detail = err
      }
      toast.add('error', `更新失败, 原因：${detail}`, '', 5000)
    })
}
