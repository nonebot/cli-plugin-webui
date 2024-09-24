/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { FileResponse } from '../models/FileResponse'
import type { SimpleModel } from '../models/SimpleModel'
import type { CancelablePromise } from '../core/CancelablePromise'
import { OpenAPI } from '../core/OpenAPI'
import { request as __request } from '../core/request'
export class FileService {
  /**
   * Get File List
   * - 根据提供的路径, 基于 base_dir 返回文件列表
   * @param path
   * @returns FileResponse Successful Response
   * @throws ApiError
   */
  public static getFileListV1FileListGet(path: string): CancelablePromise<FileResponse> {
    return __request(OpenAPI, {
      method: 'GET',
      url: '/v1/file/list',
      query: {
        path: path
      },
      errors: {
        422: `Validation Error`
      }
    })
  }
  /**
   * Create File
   * - 根据提供的路径, 基于 base_dir 创建文件
   * @param requestBody
   * @returns FileResponse Successful Response
   * @throws ApiError
   */
  public static createFileV1FileCreatePost(
    requestBody: SimpleModel
  ): CancelablePromise<FileResponse> {
    return __request(OpenAPI, {
      method: 'POST',
      url: '/v1/file/create',
      body: requestBody,
      mediaType: 'application/json',
      errors: {
        422: `Validation Error`
      }
    })
  }
  /**
   * Delete File
   * - 根据提供的路径, 基于 base_dir 删除文件
   * @param path
   * @returns FileResponse Successful Response
   * @throws ApiError
   */
  public static deleteFileV1FileDeleteDelete(path: string): CancelablePromise<FileResponse> {
    return __request(OpenAPI, {
      method: 'DELETE',
      url: '/v1/file/delete',
      query: {
        path: path
      },
      errors: {
        422: `Validation Error`
      }
    })
  }
}
