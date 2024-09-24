/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { nb_cli_plugin_webui__app__schemas__ModuleInfo } from './nb_cli_plugin_webui__app__schemas__ModuleInfo'
export type CreateProjectData = {
  is_bootstrap: boolean
  project_name: string
  project_dir: string
  mirror_url: string
  drivers: Array<nb_cli_plugin_webui__app__schemas__ModuleInfo>
  adapters: Array<nb_cli_plugin_webui__app__schemas__ModuleInfo>
  use_src: boolean
}
