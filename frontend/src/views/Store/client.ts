import {
  type SearchTag,
  type Adapter,
  type Driver,
  type nb_cli_plugin_webui__app__schemas__Plugin,
  SearchRequest,
  StoreService
} from '@/client/api'
import { useToastStore } from '@/stores/ToastStorage'
import { defineStore } from 'pinia'
import { ref } from 'vue'

const toast = useToastStore()

export const useSearchStore = defineStore('searchStore', () => {
  const searchInput = ref(''),
    searchTags = ref<SearchTag[]>([]),
    storeData = ref<(nb_cli_plugin_webui__app__schemas__Plugin | Adapter | Driver)[]>([]),
    nowPage = ref(1),
    totalPage = ref(1),
    totalItem = ref(0),
    viewModule = ref<SearchRequest.module_type>(SearchRequest.module_type.PLUGIN),
    isRequesting = ref(false)

  const clear = () => {
    searchInput.value = ''
    searchTags.value = []
    storeData.value = []
    nowPage.value = 1
    totalPage.value = 1
    totalItem.value = 0
  }

  const isTagExisted = (tag: SearchTag) => {
    return searchTags.value.some((t) => t.label === tag.label && t.text === tag.text)
  }

  const removeTag = (tag: SearchTag) => {
    const index = searchTags.value.findIndex((t) => t.label === tag.label && t.text === tag.text)
    if (index !== -1) {
      searchTags.value.splice(index, 1)
    }
  }

  const updateTag = (tag: SearchTag) => {
    if (isTagExisted(tag)) {
      removeTag(tag)
    } else {
      searchTags.value.push(tag)
    }
  }

  const updateData = async (projectID: string, isShowAll: boolean) => {
    isRequesting.value = true
    const isSearch = searchInput.value !== '' || searchTags.value.length > 0
    await StoreService.getNonebotStoreItemsV1StoreNonebotListGet(
      viewModule.value,
      nowPage.value,
      isSearch,
      isShowAll,
      projectID
    )
      .then((res) => {
        storeData.value = res.detail
        totalPage.value = res.total_page
        totalItem.value = res.total_item
      })
      .catch((err) => {
        let detail = ''
        if (err.body) {
          detail = err.body.detail
        } else {
          detail = err
        }
        toast.add('error', `获取商店数据失败, 原因：${detail}`, '', 5000)
      })
      .finally(() => {
        isRequesting.value = false
      })
  }

  const selectModule = async (module: SearchRequest.module_type, projectID: string) => {
    viewModule.value = module
    clear()
    await updateData(projectID, false)
  }

  const turnPage = async (page: number, projectID: string) => {
    nowPage.value = page >= 0 ? page : 0

    if (page >= totalPage.value) {
      nowPage.value = totalPage.value
    }
    await updateData(projectID, false)
  }

  const upDataBySearch = async (projectID: string) => {
    isRequesting.value = true
    await StoreService.searchNonebotStoreItemV1StoreNonebotSearchPost(projectID, {
      data: {
        module_type: viewModule.value,
        tags: searchTags.value,
        content: searchInput.value
      }
    })
      .then((res) => {
        nowPage.value = 1

        storeData.value = res.detail
        totalPage.value = res.total_page
        totalItem.value = res.total_item
      })
      .catch((err) => {
        let detail = ''
        if (err.body) {
          detail = err.body.detail
        } else {
          detail = err
        }
        toast.add('error', `搜索失败, 原因：${detail}`, '', 5000)
      })
      .finally(() => {
        isRequesting.value = false
      })
  }

  return {
    searchInput,
    searchTags,
    storeData,
    nowPage,
    totalPage,
    totalItem,
    viewModule,
    isRequesting,
    clear,
    isTagExisted,
    removeTag,
    updateTag,
    updateData,
    selectModule,
    turnPage,
    upDataBySearch
  }
})
