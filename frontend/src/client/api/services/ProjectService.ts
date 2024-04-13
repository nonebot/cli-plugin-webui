/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { AddProjectData } from '../models/AddProjectData'
import type { CheckProjectTomlResponse } from '../models/CheckProjectTomlResponse'
import type { CreateProjectData } from '../models/CreateProjectData'
import type { GenericResponse_List_str__ } from '../models/GenericResponse_List_str__'
import type { GenericResponse_NoneBotProjectMeta_ } from '../models/GenericResponse_NoneBotProjectMeta_'
import type { GenericResponse_str_ } from '../models/GenericResponse_str_'
import type { ListProjectResponse } from '../models/ListProjectResponse'
import type { ModuleConfigResponse } from '../models/ModuleConfigResponse'
import type { ModuleConfigUpdateRequest } from '../models/ModuleConfigUpdateRequest'
import type { CancelablePromise } from '../core/CancelablePromise'
import { OpenAPI } from '../core/OpenAPI'
import { request as __request } from '../core/request'
export class ProjectService {
  /**
   *  Get Project Env List
   * - 获取 NoneBot 实例中的环境文件列表
   * @param projectId
   * @returns GenericResponse_List_str__ Successful Response
   * @throws ApiError
   */
  public static getProjectEnvListV1ProjectConfigEnvListGet(
    projectId: string
  ): CancelablePromise<GenericResponse_List_str__> {
    return __request(OpenAPI, {
      method: 'GET',
      url: '/v1/project/config/env/list',
      query: {
        project_id: projectId
      },
      errors: {
        422: `Validation Error`
      }
    })
  }
  /**
   *  Create Project Env
   * - 创建 NoneBot 实例中的环境文件
   * @param env
   * @param projectId
   * @returns GenericResponse_str_ Successful Response
   * @throws ApiError
   */
  public static createProjectEnvV1ProjectConfigEnvCreatePost(
    env: string,
    projectId: string
  ): CancelablePromise<GenericResponse_str_> {
    return __request(OpenAPI, {
      method: 'POST',
      url: '/v1/project/config/env/create',
      query: {
        env: env,
        project_id: projectId
      },
      errors: {
        422: `Validation Error`
      }
    })
  }
  /**
   *  Delete Project Env
   * - 删除 NoneBot 实例中的环境文件
   * @param env
   * @param projectId
   * @returns GenericResponse_str_ Successful Response
   * @throws ApiError
   */
  public static deleteProjectEnvV1ProjectConfigEnvDeleteDelete(
    env: string,
    projectId: string
  ): CancelablePromise<GenericResponse_str_> {
    return __request(OpenAPI, {
      method: 'DELETE',
      url: '/v1/project/config/env/delete',
      query: {
        env: env,
        project_id: projectId
      },
      errors: {
        422: `Validation Error`
      }
    })
  }
  /**
   *  Use Project Env
   * - 切换 NoneBot 实例所应用的环境文件
   * @param env
   * @param projectId
   * @returns GenericResponse_str_ Successful Response
   * @throws ApiError
   */
  public static useProjectEnvV1ProjectConfigEnvUsePost(
    env: string,
    projectId: string
  ): CancelablePromise<GenericResponse_str_> {
    return __request(OpenAPI, {
      method: 'POST',
      url: '/v1/project/config/env/use',
      query: {
        env: env,
        project_id: projectId
      },
      errors: {
        422: `Validation Error`
      }
    })
  }
  /**
   *  Get Project Meta Config
   * - 获取 NoneBot 实例配置信息
   * @param projectId
   * @returns ModuleConfigResponse Successful Response
   * @throws ApiError
   */
  public static getProjectMetaConfigV1ProjectConfigMetaDetailGet(
    projectId: string
  ): CancelablePromise<ModuleConfigResponse> {
    return __request(OpenAPI, {
      method: 'GET',
      url: '/v1/project/config/meta/detail',
      query: {
        project_id: projectId
      },
      errors: {
        422: `Validation Error`
      }
    })
  }
  /**
   *  Get Project Nonebot Config
   * - 获取 NoneBot 实例中 NoneBot 配置信息
   * @param projectId
   * @returns ModuleConfigResponse Successful Response
   * @throws ApiError
   */
  public static getProjectNonebotConfigV1ProjectConfigNonebotDetailGet(
    projectId: string
  ): CancelablePromise<ModuleConfigResponse> {
    return __request(OpenAPI, {
      method: 'GET',
      url: '/v1/project/config/nonebot/detail',
      query: {
        project_id: projectId
      },
      errors: {
        422: `Validation Error`
      }
    })
  }
  /**
   *  Get Project Nonebot Plugin Config
   * - 获取 NoneBot 实例中所有 NoneBot 插件设置信息
   * @param projectId
   * @returns ModuleConfigResponse Successful Response
   * @throws ApiError
   */
  public static getProjectNonebotPluginConfigV1ProjectConfigNonebotPluginsDetailGet(
    projectId: string
  ): CancelablePromise<ModuleConfigResponse> {
    return __request(OpenAPI, {
      method: 'GET',
      url: '/v1/project/config/nonebot/plugins/detail',
      query: {
        project_id: projectId
      },
      errors: {
        422: `Validation Error`
      }
    })
  }
  /**
   *  Update Project Config
   * - 根据模块类型及环境更新配置信息
   * @param moduleType
   * @param projectId
   * @param requestBody
   * @returns GenericResponse_str_ Successful Response
   * @throws ApiError
   */
  public static updateProjectConfigV1ProjectConfigUpdatePost(
    moduleType: string,
    projectId: string,
    requestBody: ModuleConfigUpdateRequest
  ): CancelablePromise<GenericResponse_str_> {
    return __request(OpenAPI, {
      method: 'POST',
      url: '/v1/project/config/update',
      query: {
        module_type: moduleType,
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
   * Create Project
   * - 创建 NoneBot 实例
   * - 返回对应的日志密钥, 用于日志展现
   * @param requestBody
   * @returns GenericResponse_str_ Successful Response
   * @throws ApiError
   */
  public static createProjectV1ProjectCreatePost(
    requestBody: CreateProjectData
  ): CancelablePromise<GenericResponse_str_> {
    return __request(OpenAPI, {
      method: 'POST',
      url: '/v1/project/create',
      body: requestBody,
      mediaType: 'application/json',
      errors: {
        422: `Validation Error`
      }
    })
  }
  /**
   * Add Project
   * - 添加 NoneBot 实例
   * - 返回对应的日志密钥, 用于日志展现
   * @param requestBody
   * @returns GenericResponse_str_ Successful Response
   * @throws ApiError
   */
  public static addProjectV1ProjectAddPost(
    requestBody: AddProjectData
  ): CancelablePromise<GenericResponse_str_> {
    return __request(OpenAPI, {
      method: 'POST',
      url: '/v1/project/add',
      body: requestBody,
      mediaType: 'application/json',
      errors: {
        422: `Validation Error`
      }
    })
  }
  /**
   * Get Project Profile
   * - 获取 NoneBot 实例的配置信息
   * @param projectId
   * @returns GenericResponse_NoneBotProjectMeta_ Successful Response
   * @throws ApiError
   */
  public static getProjectProfileV1ProjectProfileGet(
    projectId: string
  ): CancelablePromise<GenericResponse_NoneBotProjectMeta_> {
    return __request(OpenAPI, {
      method: 'GET',
      url: '/v1/project/profile',
      query: {
        project_id: projectId
      },
      errors: {
        422: `Validation Error`
      }
    })
  }
  /**
   * Delete Project
   * - 删除 NoneBot 实例
   * @param projectId
   * @param deleteFully
   * @returns GenericResponse_str_ Successful Response
   * @throws ApiError
   */
  public static deleteProjectV1ProjectDeleteDelete(
    projectId: string,
    deleteFully: boolean = false
  ): CancelablePromise<GenericResponse_str_> {
    return __request(OpenAPI, {
      method: 'DELETE',
      url: '/v1/project/delete',
      query: {
        delete_fully: deleteFully,
        project_id: projectId
      },
      errors: {
        422: `Validation Error`
      }
    })
  }
  /**
   * List Project
   * - 获取所有 NoneBot 实例基本信息
   * @returns ListProjectResponse Successful Response
   * @throws ApiError
   */
  public static listProjectV1ProjectListGet(): CancelablePromise<ListProjectResponse> {
    return __request(OpenAPI, {
      method: 'GET',
      url: '/v1/project/list'
    })
  }
  /**
   * Check Project Toml
   * - 检查 NoneBot 实例的 toml 文件并从中获取所需信息
   * - 如返回报错信息, 则说明检查失败
   * @param projectDir
   * @returns CheckProjectTomlResponse Successful Response
   * @throws ApiError
   */
  public static checkProjectTomlV1ProjectCheckTomlPost(
    projectDir: string
  ): CancelablePromise<CheckProjectTomlResponse> {
    return __request(OpenAPI, {
      method: 'POST',
      url: '/v1/project/check_toml',
      query: {
        project_dir: projectDir
      },
      errors: {
        422: `Validation Error`
      }
    })
  }
}
