/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Body_search_nonebot_store_item_v1_store_nonebot_search_post } from '../models/Body_search_nonebot_store_item_v1_store_nonebot_search_post'
import type { GenericResponse_str_ } from '../models/GenericResponse_str_'
import type { nb_cli_plugin_webui__app__store__schemas__ModuleInfo } from '../models/nb_cli_plugin_webui__app__store__schemas__ModuleInfo'
import type { nb_cli_plugin_webui__app__store__schemas__Plugin } from '../models/nb_cli_plugin_webui__app__store__schemas__Plugin'
import type { StoreListResponse } from '../models/StoreListResponse'
import type { CancelablePromise } from '../core/CancelablePromise'
import { OpenAPI } from '../core/OpenAPI'
import { request as __request } from '../core/request'
export class StoreService {
  /**
   *  Install Nonebot Module
   * - 安装模块至 NoneBot 实例
   * @param env
   * @param projectId
   * @param requestBody
   * @returns GenericResponse_str_ Successful Response
   * @throws ApiError
   */
  public static installNonebotModuleV1StoreNonebotInstallPost(
    env: string,
    projectId: string,
    requestBody:
      | nb_cli_plugin_webui__app__store__schemas__ModuleInfo
      | nb_cli_plugin_webui__app__store__schemas__Plugin
  ): CancelablePromise<GenericResponse_str_> {
    return __request(OpenAPI, {
      method: 'POST',
      url: '/v1/store/nonebot/install',
      query: {
        env: env,
        project_id: projectId
      },
      body: requestBody,
      mediaType: 'application/json',
      errors: {
        422: `Validation Error`
      }
    })
  }
  /**
   *  Uninstall Nonebot Module
   * - 卸载 NoneBot 实例中的模块
   * @param env
   * @param projectId
   * @param requestBody
   * @returns GenericResponse_str_ Successful Response
   * @throws ApiError
   */
  public static uninstallNonebotModuleV1StoreNonebotUninstallPost(
    env: string,
    projectId: string,
    requestBody:
      | nb_cli_plugin_webui__app__store__schemas__ModuleInfo
      | nb_cli_plugin_webui__app__store__schemas__Plugin
  ): CancelablePromise<GenericResponse_str_> {
    return __request(OpenAPI, {
      method: 'POST',
      url: '/v1/store/nonebot/uninstall',
      query: {
        env: env,
        project_id: projectId
      },
      body: requestBody,
      mediaType: 'application/json',
      errors: {
        422: `Validation Error`
      }
    })
  }
  /**
   *  Get Nonebot Store Items
   * - 获取 NoneBot Store 中的模块列表
   * @param moduleType
   * @param page
   * @param isSearch
   * @param showAll
   * @param projectId
   * @returns StoreListResponse Successful Response
   * @throws ApiError
   */
  public static getNonebotStoreItemsV1StoreNonebotListGet(
    moduleType: 'plugin' | 'adapter' | 'driver' | 'project' | 'toml',
    page: number,
    isSearch: boolean = false,
    showAll: boolean = false,
    projectId?: string
  ): CancelablePromise<StoreListResponse> {
    return __request(OpenAPI, {
      method: 'GET',
      url: '/v1/store/nonebot/list',
      query: {
        module_type: moduleType,
        page: page,
        is_search: isSearch,
        show_all: showAll,
        project_id: projectId
      },
      errors: {
        422: `Validation Error`
      }
    })
  }
  /**
   * Search Nonebot Store Item
   * - 搜索 NoneBot Store 中的模块
   * @param projectId
   * @param requestBody
   * @returns StoreListResponse Successful Response
   * @throws ApiError
   */
  public static searchNonebotStoreItemV1StoreNonebotSearchPost(
    projectId: string,
    requestBody: Body_search_nonebot_store_item_v1_store_nonebot_search_post
  ): CancelablePromise<StoreListResponse> {
    return __request(OpenAPI, {
      method: 'POST',
      url: '/v1/store/nonebot/search',
      query: {
        project_id: projectId
      },
      body: requestBody,
      mediaType: 'application/json',
      errors: {
        422: `Validation Error`
      }
    })
  }
}
