/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Adapter } from './Adapter'
import type { Driver } from './Driver'
import type { nb_cli_plugin_webui__app__schemas__Plugin } from './nb_cli_plugin_webui__app__schemas__Plugin'
export type StoreListResponse = {
  detail: Array<nb_cli_plugin_webui__app__schemas__Plugin> | Array<Adapter> | Array<Driver>
  now_page: number
  total_page: number
  total_item: number
}
