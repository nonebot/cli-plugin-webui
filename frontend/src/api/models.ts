export interface LoginResponse {
  jwt_token: string;
}

export interface IsAvailableResponse {
  detail: string;
}

interface Tag {
  label: string;
  color: string;
}

export interface SimpleInfo {
  module_name: string;
  project_link: string;
  name: string;
  desc: string;
  author: string;
  homepage: string;
  tags?: Tag[];
  is_official: boolean;
  is_download: boolean;
}

export interface Plugin extends SimpleInfo {
  type?: string;
  supported_adapters?: string[];
  valid: boolean;
  time: string;
}

export interface Adapter extends SimpleInfo {}

export interface Driver extends SimpleInfo {}

export interface FileDetails {
  name: string;
  is_dir: number;
  path: string;
  modified_time: string;
  absolute_path: string;
}

export interface FileInfo {
  name: string;
  modified_time: string;
  is_dir: number;
  path: string;
}

export interface FileListResponse {
  files: FileDetails[];
}

export interface CreateProjectData {
  is_bootstrap: boolean;
  project_name: string;
  project_dir: string;
  mirror_url: string;
  drivers: Driver[];
  adapters: Adapter[];
  use_src: boolean;
}

export interface CreateProjectResponse {
  log_key: string;
}

export interface NonebotProjectMeta {
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

  use_run_script: boolean
  run_script_name: string
}

export interface NonebotProjectListResponse {
  projects: {
    [key: string]: NonebotProjectMeta;
  };
}

export interface DeleteProjectResponse {
  project_id: string;
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

export interface LogHistoryResponse {
  detail: ProcessLog[];
}

export interface StoreListResponse {
  now_page: number;
  total_page: number;
  total_item: number;
  data: Plugin[] | Adapter[] | Driver[];
}

export interface InstallModuleResponse extends CreateProjectResponse {}

export interface UninstallModuleResponse extends CreateProjectResponse {}

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

export interface ModuleConfigResponse {
  detail: ModuleConfigFather[];
}

export interface DotenvListResponse {
  detail: string[];
}
