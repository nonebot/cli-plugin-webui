/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ConfigType } from './ConfigType'
import type { ModuleConfigChild } from './ModuleConfigChild'
import type { ModuleType } from './ModuleType'
export type ModuleConfigFather = {
  title: string
  description: string
  name: string
  module_type: ModuleType | ConfigType
  properties: Array<ModuleConfigChild>
}
