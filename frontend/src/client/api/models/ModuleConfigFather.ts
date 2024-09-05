/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ModuleConfigChild } from './ModuleConfigChild'
export type ModuleConfigFather = {
  title: string
  description: string
  name: string
  module_type: ModuleConfigFather.module_type
  properties: Array<ModuleConfigChild>
}
export namespace ModuleConfigFather {
  export enum module_type {
    PLUGIN = 'plugin',
    ADAPTER = 'adapter',
    DRIVER = 'driver',
    PROJECT = 'project',
    TOML = 'toml'
  }
}
