/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { nb_cli_plugin_webui__app__schemas__ModuleInfo } from './nb_cli_plugin_webui__app__schemas__ModuleInfo'
import type { nb_cli_plugin_webui__app__schemas__Plugin } from './nb_cli_plugin_webui__app__schemas__Plugin'
export type NoneBotProjectMeta = {
  project_id: string
  project_name: string
  project_dir: string
  mirror_url: string
  adapters: Array<nb_cli_plugin_webui__app__schemas__ModuleInfo>
  drivers: Array<nb_cli_plugin_webui__app__schemas__ModuleInfo>
  plugins: Array<nb_cli_plugin_webui__app__schemas__Plugin>
  plugin_dirs: Array<string>
  builtin_plugins: Array<string>
  is_running?: boolean
  use_run_script?: boolean
  run_script_name?: string
}
