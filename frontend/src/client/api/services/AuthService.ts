/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { GenericResponse_str_ } from '../models/GenericResponse_str_'
import type { LoginRequest } from '../models/LoginRequest'
import type { VerifyRequest } from '../models/VerifyRequest'
import type { CancelablePromise } from '../core/CancelablePromise'
import { OpenAPI } from '../core/OpenAPI'
import { request as __request } from '../core/request'
export class AuthService {
  /**
   * Auth Token
   * - 登录, 成功后返回 JWT 密钥
   * @param requestBody
   * @returns GenericResponse_str_ Successful Response
   * @throws ApiError
   */
  public static authTokenV1AuthLoginPost(
    requestBody: LoginRequest
  ): CancelablePromise<GenericResponse_str_> {
    return __request(OpenAPI, {
      method: 'POST',
      url: '/v1/auth/login',
      body: requestBody,
      mediaType: 'application/json',
      errors: {
        422: `Validation Error`
      }
    })
  }
  /**
   * Verify Token
   * - 验证 JWT 密钥是否可用, 返回到期时间戳
   * @param requestBody
   * @returns GenericResponse_str_ Successful Response
   * @throws ApiError
   */
  public static verifyTokenV1AuthVerifyPost(
    requestBody: VerifyRequest
  ): CancelablePromise<GenericResponse_str_> {
    return __request(OpenAPI, {
      method: 'POST',
      url: '/v1/auth/verify',
      body: requestBody,
      mediaType: 'application/json',
      errors: {
        422: `Validation Error`
      }
    })
  }
}
