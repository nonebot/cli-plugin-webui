/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { SearchTag } from './SearchTag'
export type SearchRequest = {
  module_type: SearchRequest.module_type
  tags?: Array<SearchTag>
  content: string
}
export namespace SearchRequest {
  export enum module_type {
    PLUGIN = 'plugin',
    ADAPTER = 'adapter',
    DRIVER = 'driver'
  }
}
