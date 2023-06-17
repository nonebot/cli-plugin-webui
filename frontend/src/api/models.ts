interface LoginData {
  token: string;
  mark: string;
}

export interface LoginRequest {
  login_data: LoginData;
}

export interface LoginResponse {
  jwt_token: string;
}

export interface IsAvailableResponse {
  detail: string;
}

export interface AdaptersResponse {
  adapters: Adapter[];
}

export interface Adapter {
  name: string;
  module_name: string;
  project_link: string;
  desc: string;
}

export interface DriversResponse {
  drivers: Driver[];
}

export interface Driver {
  name: string;
  module_name: string;
  project_link: string;
  desc: string;
}

export interface FileMeta {
  name: string;
  is_dir: number;
  path: string;
}

export interface FileDetails {
  name: string;
  is_dir: number;
  path: string;
  modified_time: string;
  absolute_path: string;
}

export interface FileOperateRequest {
  file_data: FileMeta;
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
  project_name: string;
  project_dir: string;
  mirror_url: string;
  driver: Driver;
  adapter: Adapter;
}

export interface CreateProjectRequest {
  project_data: CreateProjectData;
}

export interface CreateProjectResponse {
  log_key: string;
}

interface SimpleInfo {
  name: string;
  module_name: string;
}

export interface NonebotProjectMeta {
  project_id: string;
  project_name: string;
  project_dir: string;
  mirror: string;
  adapters: SimpleInfo[];
  drivers: SimpleInfo[];
  plugins: string[];
  plugin_dirs: string[];
  builtin_plugins: string[];
}

export interface NonebotProjectListResponse {
  projects: {
    [key: string]: NonebotProjectMeta;
  };
}

export interface DeleteProjectResponse {
  project_id: string;
}
