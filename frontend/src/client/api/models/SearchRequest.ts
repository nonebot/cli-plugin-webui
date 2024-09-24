/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ModuleType } from './ModuleType'
import type { nb_cli_plugin_webui__app__schemas__SearchTag } from './nb_cli_plugin_webui__app__schemas__SearchTag'
export type SearchRequest = {
  module_type: ModuleType
  tags?: Array<nb_cli_plugin_webui__app__schemas__SearchTag>
  content: string
}
