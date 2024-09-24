/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { GenericResponse_int_ } from '../models/GenericResponse_int_'
import type { GenericResponse_List_nb_cli_plugin_webui_app_handlers_process_schemas_ProcessLog__ } from '../models/GenericResponse_List_nb_cli_plugin_webui_app_handlers_process_schemas_ProcessLog__'
import type { GenericResponse_str_ } from '../models/GenericResponse_str_'
import type { CancelablePromise } from '../core/CancelablePromise'
import { OpenAPI } from '../core/OpenAPI'
import { request as __request } from '../core/request'
export class ProcessService {
  /**
   * Run Process
   * - 运行 NoneBot 实例
   * @param projectId
   * @returns GenericResponse_str_ Successful Response
   * @throws ApiError
   */
  public static runProcessV1ProcessRunPost(
    projectId: string
  ): CancelablePromise<GenericResponse_str_> {
    return __request(OpenAPI, {
      method: 'POST',
      url: '/v1/process/run',
      query: {
        project_id: projectId
      },
      errors: {
        422: `Validation Error`
      }
    })
  }
  /**
   *  Stop Process
   * - 终止 NoneBot 实例
   * @param projectId
   * @returns GenericResponse_str_ Successful Response
   * @throws ApiError
   */
  public static stopProcessV1ProcessStopPost(
    projectId: string
  ): CancelablePromise<GenericResponse_str_> {
    return __request(OpenAPI, {
      method: 'POST',
      url: '/v1/process/stop',
      query: {
        project_id: projectId
      },
      errors: {
        422: `Validation Error`
      }
    })
  }
  /**
   * Write To Process
   * - 向 NoneBot 实例进程写入数据
   * @param content
   * @param projectId
   * @returns GenericResponse_int_ Successful Response
   * @throws ApiError
   */
  public static writeToProcessV1ProcessWritePost(
    content: string,
    projectId: string
  ): CancelablePromise<GenericResponse_int_> {
    return __request(OpenAPI, {
      method: 'POST',
      url: '/v1/process/write',
      query: {
        content: content,
        project_id: projectId
      },
      errors: {
        422: `Validation Error`
      }
    })
  }
  /**
   * Get Log History
   * - 获取历史进程日志
   * @param logCount
   * @param logId
   * @returns GenericResponse_List_nb_cli_plugin_webui_app_handlers_process_schemas_ProcessLog__ Successful Response
   * @throws ApiError
   */
  public static getLogHistoryV1ProcessLogHistoryGet(
    logCount: number,
    logId: string
  ): CancelablePromise<GenericResponse_List_nb_cli_plugin_webui_app_handlers_process_schemas_ProcessLog__> {
    return __request(OpenAPI, {
      method: 'GET',
      url: '/v1/process/log/history',
      query: {
        log_count: logCount,
        log_id: logId
      },
      errors: {
        422: `Validation Error`
      }
    })
  }
}
