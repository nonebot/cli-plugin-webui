import axios, { AxiosResponse } from "axios";

import { isDebug } from "@/utils";
import {
  FileListResponse,
  IsAvailableResponse,
  LoginResponse,
  CreateProjectResponse,
  CreateProjectData,
  NonebotProjectListResponse,
  DeleteProjectResponse,
  ProcessInfo,
  StoreListResponse,
  InstallModuleResponse,
  SimpleInfo,
  ModuleConfigResponse,
  DotenvListResponse,
  LogHistoryResponse,
  NonebotProjectMeta,
} from "./models";

export class API {
  private generateBaseURL(): string {
    if (isDebug()) {
      const host = localStorage.getItem("host");
      const port = localStorage.getItem("port");
      return `//${host}:${port}/api`;
    }
    return "/api";
  }

  private async baseGetRequest<T>(endpoint: string, params = {}): Promise<T> {
    const url = this.generateBaseURL() + endpoint;
    try {
      const resp: AxiosResponse<T> = await axios.get(url, {
        params: { ...params },
      });
      return resp.data;
    } catch (error: any) {
      return Promise.reject(error);
    }
  }

  private async basePostRequest<T>(endpoint: string, data = {}): Promise<T> {
    const url = this.generateBaseURL() + endpoint;
    try {
      const resp: AxiosResponse<T> = await axios.post(url, (data = data));
      return resp.data;
    } catch (error: any) {
      return Promise.reject(error);
    }
  }

  private async baseDeleteRequest<T>(endpoint: string, params = {}): Promise<T> {
    const url = this.generateBaseURL() + endpoint;
    try {
      const resp: AxiosResponse<T> = await axios.delete(url, {
        params: { ...params },
      });
      return resp.data;
    } catch (error: any) {
      return Promise.reject(error);
    }
  }

  async doLogin(token: string): Promise<LoginResponse> {
    const mark = new Date().toString();
    const requestData = {
      login_data: {
        token: token,
        mark: mark,
      },
    };
    return await this.basePostRequest<LoginResponse>("/auth/login", requestData);
  }

  async isAvailable(): Promise<IsAvailableResponse> {
    return await this.baseGetRequest<IsAvailableResponse>("/auth/is_available");
  }

  async getFileList(path: string): Promise<FileListResponse> {
    const requestData = {
      path: path,
    };
    return await this.baseGetRequest<FileListResponse>("/file/list", requestData);
  }

  async createFile(
    fileName: string,
    isFolder: boolean,
    path: string,
  ): Promise<FileListResponse> {
    const requestData = {
      file_data: {
        name: fileName,
        is_dir: isFolder ? 1 : 0,
        path: path,
      },
    };
    return await this.basePostRequest<FileListResponse>("/file/create", requestData);
  }

  async deleteFile(
    fileName: string,
    isFolder: boolean,
    path: string,
  ): Promise<FileListResponse> {
    const requestData = {
      file_data: {
        name: fileName,
        is_dir: isFolder ? 1 : 0,
        path: path,
      },
    };
    return await this.baseDeleteRequest<FileListResponse>("/file/delete", requestData);
  }

  async createProject(data: CreateProjectData): Promise<CreateProjectResponse> {
    const requestData = {
      project_data: data,
    };
    return await this.basePostRequest<CreateProjectResponse>(
      "/project/create",
      requestData,
    );
  }

  async getProjectList(): Promise<NonebotProjectListResponse> {
    return await this.baseGetRequest<NonebotProjectListResponse>("/project/list");
  }

  async deleteProject(projectID: string): Promise<DeleteProjectResponse> {
    const requestData = {
      project_id: projectID,
    };
    return await this.baseDeleteRequest<DeleteProjectResponse>(
      "/project/delete",
      requestData,
    );
  }

  async runProject(projectID: string): Promise<void> {
    const requestData = {
      project_id: projectID,
    };
    return await this.basePostRequest<void>("/project/run", requestData);
  }

  async stopProject(projectID: string): Promise<void> {
    const requestData = {
      project_id: projectID,
    };
    return await this.basePostRequest<void>("/project/stop", requestData);
  }

  async writeStdin(projectID: string, content: string): Promise<void> {
    const requestData = {
      project_id: projectID,
      content: content,
    };
    return await this.basePostRequest<void>("/project/write", requestData);
  }

  async getProjectProcessStatus(projectID: string): Promise<ProcessInfo> {
    const requestData = {
      project_id: projectID,
    };
    return await this.baseGetRequest("/project/status", requestData);
  }

  async getProcessLogHistory(
    logKey: string,
    logCount: number,
  ): Promise<LogHistoryResponse> {
    const requestData = {
      log_key: logKey,
      log_count: logCount,
    };
    return await this.baseGetRequest<LogHistoryResponse>(
      "/log/logs/history",
      requestData,
    );
  }

  async getPlugins(
    page: number,
    isSearch?: boolean,
    projectID?: string,
    showAll?: boolean,
  ): Promise<StoreListResponse> {
    const requestData = {
      page: page,
      is_search: isSearch ? 1 : 0,
      project_id: projectID,
      show_all: showAll ? 1 : 0,
    };
    return await this.baseGetRequest<StoreListResponse>(
      "/store/list/plugin",
      requestData,
    );
  }

  async getAdapters(
    page: number,
    isSearch?: boolean,
    projectID?: string,
    showAll?: boolean,
  ): Promise<StoreListResponse> {
    const requestData = {
      page: page,
      is_search: isSearch ? 1 : 0,
      project_id: projectID,
      show_all: showAll ? 1 : 0,
    };
    return await this.baseGetRequest<StoreListResponse>(
      "/store/list/adapter",
      requestData,
    );
  }

  async getDrivers(
    page: number,
    isSearch?: boolean,
    projectID?: string,
    showAll?: boolean,
  ): Promise<StoreListResponse> {
    const requestData = {
      page: page,
      is_search: isSearch ? 1 : 0,
      project_id: projectID,
      show_all: showAll ? 1 : 0,
    };
    return await this.baseGetRequest<StoreListResponse>(
      "/store/list/driver",
      requestData,
    );
  }

  async refreshStore(): Promise<void> {
    return await this.baseGetRequest<void>("/store/list/refresh");
  }

  async searchStore(
    projectID: string,
    moduleType: string,
    content: string,
  ): Promise<StoreListResponse> {
    const requestData = {
      data: {
        project_id: projectID,
        module_type: moduleType,
        content: content,
      },
    };
    return await this.basePostRequest<StoreListResponse>("/store/search", requestData);
  }

  async installModule(
    projectID: string,
    env: string,
    module: SimpleInfo,
  ): Promise<InstallModuleResponse> {
    const requestData = {
      project_id: projectID,
      env: env,
      module: module,
    };
    return await this.basePostRequest<InstallModuleResponse>(
      "/project/module/install",
      requestData,
    );
  }

  async uninstallModule(projectID: string, env: string, module: any): Promise<void> {
    const requestData = {
      project_id: projectID,
      env: env,
      module: module,
    };
    return await this.basePostRequest<void>("/project/module/uninstall", requestData);
  }

  async getProjectMetaConfig(projectID: string): Promise<ModuleConfigResponse> {
    const requestData = {
      project_id: projectID,
    };
    return await this.baseGetRequest<ModuleConfigResponse>(
      "/project/config/meta/list",
      requestData,
    );
  }

  async getNonebotConfig(projectID: string): Promise<ModuleConfigResponse> {
    const requestData = {
      project_id: projectID,
    };
    return await this.baseGetRequest<ModuleConfigResponse>(
      "/project/config/nonebot/list",
      requestData,
    );
  }

  async getProjectPluginConfigList(projectID: string): Promise<ModuleConfigResponse> {
    const requestData = {
      project_id: projectID,
    };
    return await this.baseGetRequest<ModuleConfigResponse>(
      "/project/config/plugin/list",
      requestData,
    );
  }

  async getDotenvList(projectID: string): Promise<DotenvListResponse> {
    const requestData = {
      project_id: projectID,
    };
    return await this.baseGetRequest<DotenvListResponse>(
      "/project/config/dotenv/list",
      requestData,
    );
  }

  async createDotenvFile(projectID: string, env: string): Promise<void> {
    const requestData = {
      project_id: projectID,
      env: env,
    };
    return await this.basePostRequest<void>("/project/config/dotenv/create", requestData);
  }

  async deleteDotenvFile(projectID: string, env: string): Promise<void> {
    const requestData = {
      project_id: projectID,
      env: env,
    };
    return await this.basePostRequest<void>("/project/config/dotenv/delete", requestData);
  }

  async activeDotenvFile(projectID: string, env: string): Promise<void> {
    const requestData = {
      project_id: projectID,
      env: env,
    };
    return await this.basePostRequest<void>("/project/config/dotenv/active", requestData);
  }

  async configSet(
    projectID: string,
    moduleType: string,
    env: string,
    keyType: string,
    k: string,
    v: any,
  ): Promise<void> {
    const requestData = {
      project_id: projectID,
      module_type: moduleType,
      data: {
        env: env,
        k_type: keyType,
        k: k,
        v: v,
      },
    };
    return await this.basePostRequest<void>("/project/config/set", requestData);
  }

  async getProjectDetail(projectID: string): Promise<NonebotProjectMeta> {
    const requestData = {
      project_id: projectID,
    };
    return await this.baseGetRequest("/project/detail", requestData);
  }
}
