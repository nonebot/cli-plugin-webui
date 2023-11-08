export type GenericResponse<T> = T extends void ? {} : { detail: T };

export interface SimpleInfo {
  module_name: string;
  project_link: string;
  name: string;
  desc: string;
  author: string;
  homepage: string;
  tags?: {
    label: string;
    color: string;
  }[];
  is_official: boolean;
  is_download: boolean;
}

export interface Plugin extends SimpleInfo {
  type?: string;
  supported_adapters?: string[];
  valid: boolean;
  time: string;
  version: string;
}

export type Adapter = SimpleInfo;
export type Driver = SimpleInfo;

interface FileSimpleInfo {
  name: string;
  is_dir: boolean;
  path: string;
}

export interface FileInfo extends FileSimpleInfo {
  modified_time: string;
  absolute_path: string;
}

export type FileResponse = GenericResponse<FileInfo[]>;

export interface CreateProjectData {
  is_bootstrap: boolean;
  project_name: string;
  project_dir: string;
  mirror_url: string;
  drivers: Driver[];
  adapters: Adapter[];
  use_src: boolean;
}

export interface NoneBotProjectMeta {
  project_id: string;
  project_name: string;
  project_dir: string;
  mirror_url: string;
  adapters: SimpleInfo[];
  drivers: SimpleInfo[];
  plugins: Plugin[];
  plugin_dirs: string[];
  builtin_plugins: string[];

  is_running: boolean;

  use_run_script: boolean;
  run_script_name: string;
}

export interface ProcessLog {
  time: string;
  level: string;
  message: string;
}

interface ProcessPerformance {
  cpu: number;
  mem: number;
}

export interface ProcessInfo {
  status_code?: number;
  total_logs: number;
  is_running: boolean;
  performance?: ProcessPerformance;
}

export interface StoreListResponse
  extends GenericResponse<Plugin[] & Adapter[] & Driver[]> {
  now_page: number;
  total_page: number;
  total_item: number;
}

interface ModuleConfigSimpleInfo {
  title: string;
  description: string;
  name: string;
}

export interface ModuleConfigChild extends ModuleConfigSimpleInfo {
  default: any;
  item_type: string;
  enum: string[] | number[];
  configured: any;
  latest_change: string;
}

export interface ModuleConfigFather extends ModuleConfigSimpleInfo {
  properties: ModuleConfigChild[];
}

export type ModuleConfigResponse = GenericResponse<ModuleConfigFather[]>;

export interface CheckProjectTomlDetail {
  project_name: string;
  adapters: {
    name: string;
    module_name: string;
  }[];
  plugins: string[];
  plugin_dirs: string[];
  builtin_plugins: string[];
}

export interface CheckProjectTomlResponse
  extends GenericResponse<CheckProjectTomlDetail> {
  msg: string;
  level: "success" | "warn" | "error";
}

export interface AddProjectData {
  project_name: string;
  project_dir: string;
  mirror_url: string;
  adapters: string[];
  plugins: string[];
  plugin_dirs: string[];
  builtin_plugins: string[];
}
