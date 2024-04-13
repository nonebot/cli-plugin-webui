/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ModuleTag } from './ModuleTag'
export type nb_cli_plugin_webui__app__schemas__Plugin = {
  module_name: string
  project_link: string
  name: string
  desc: string
  author: string
  homepage: string
  tags?: Array<ModuleTag>
  is_official: boolean
  is_download?: boolean
  type?: string
  supported_adapters?: Array<string>
  valid: boolean
  version: string
  time: string
  skip_test: boolean
  config_detail?: Record<string, any>
}
