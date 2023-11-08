import axios from "axios";

import { isDebug } from "@/utils";
import {
  FileResponse,
  GenericResponse,
  CreateProjectData,
  ProcessLog,
  StoreListResponse,
  SimpleInfo,
  Plugin,
  NoneBotProjectMeta,
  CheckProjectTomlResponse,
  AddProjectData,
  ModuleConfigResponse,
} from "@/api/schemas";

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
      const resp = await axios.get(url, {
        params: { ...params },
      });
      return resp.data;
    } catch (error: any) {
      return Promise.reject(error);
    }
  }

  private async basePostRequest<T>(endpoint: string, data = {}, params = {}): Promise<T> {
    const url = this.generateBaseURL() + endpoint;
    try {
      const resp = await axios.post(url, data, {
        params: params,
      });
      return resp.data;
    } catch (error: any) {
      return Promise.reject(error);
    }
  }

  private async baseDeleteRequest<T>(endpoint: string, params = {}): Promise<T> {
    const url = this.generateBaseURL() + endpoint;
    try {
      const resp = await axios.delete(url, {
        params: { ...params },
      });
      return resp.data;
    } catch (error: any) {
      return Promise.reject(error);
    }
  }

  async doLogin(token: string): Promise<GenericResponse<string>> {
    const mark = new Date().toString();
    return await this.basePostRequest("/auth/login", {
      token: token,
      mark: mark,
    });
  }

  async getFileList(path: string): Promise<FileResponse> {
    return await this.baseGetRequest("/file/list", {
      path: path,
    });
  }

  async createFile(
    fileName: string,
    isFolder: boolean,
    path: string,
  ): Promise<FileResponse> {
    return await this.basePostRequest("/file/create", {
      name: fileName,
      is_dir: isFolder,
      path: path,
    });
  }

  async deleteFile(path: string): Promise<FileResponse> {
    return await this.baseDeleteRequest("/file/delete", {
      path: path,
    });
  }

  async createProject(data: CreateProjectData): Promise<GenericResponse<string>> {
    return await this.basePostRequest("/project/create", data);
  }

  async addProject(data: AddProjectData): Promise<GenericResponse<string>> {
    return await this.basePostRequest("/project/add", data);
  }

  async getProjectProfile(
    projectID: string,
  ): Promise<GenericResponse<NoneBotProjectMeta>> {
    return await this.baseGetRequest("/project/profile", {
      project_id: projectID,
    });
  }

  async deleteProject(projectID: string): Promise<GenericResponse<string>> {
    return await this.baseDeleteRequest("/project/delete", {
      project_id: projectID,
    });
  }

  async getProjectList(): Promise<
    GenericResponse<{ [key: string]: NoneBotProjectMeta }>
  > {
    return await this.baseGetRequest("/project/list");
  }

  async runProject(projectID: string): Promise<GenericResponse<string>> {
    return await this.basePostRequest(
      "/process/run",
      {},
      {
        project_id: projectID,
      },
    );
  }

  async stopProject(projectID: string): Promise<GenericResponse<string>> {
    return await this.basePostRequest(
      "/process/stop",
      {},
      {
        project_id: projectID,
      },
    );
  }

  async writeToProjectProcessStdin(
    content: string,
    projectID: string,
  ): Promise<GenericResponse<number>> {
    return await this.basePostRequest(
      "/process/write",
      {},
      {
        content: content,
        project_id: projectID,
      },
    );
  }

  async getProcessLogHistory(
    logID: string,
    logCount: number,
  ): Promise<GenericResponse<ProcessLog[]>> {
    return await this.baseGetRequest("/process/log/history", {
      log_id: logID,
      log_count: logCount,
    });
  }

  async getNoneBotModules(
    moduleType: string,
    page: number,
    projectID?: string,
    isSearch?: boolean,
    showAll?: boolean,
  ): Promise<StoreListResponse> {
    return await this.baseGetRequest("/store/nonebot/list", {
      module_type: moduleType,
      page: page,
      project_id: projectID,
      is_search: isSearch,
      show_all: showAll,
    });
  }

  // TODO: need attention
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
    env: string,
    module: SimpleInfo | Plugin,
    projectID: string,
  ): Promise<GenericResponse<string>> {
    const module_type = "valid" in module ? "plugin" : "module";
    const data = { module_type: module_type, ...module };
    return await this.basePostRequest("/store/nonebot/install", data, {
      env: env,
      project_id: projectID,
    });
  }

  async uninstallModule(
    env: string,
    module: SimpleInfo | Plugin,
    projectID: string,
  ): Promise<GenericResponse<string>> {
    const module_type = "valid" in module ? "plugin" : "module";
    const data = { module_type: module_type, ...module };
    return await this.basePostRequest("/store/nonebot/uninstall", data, {
      env: env,
      project_id: projectID,
    });
  }

  async getProjectMetaConfig(projectID: string): Promise<ModuleConfigResponse> {
    return await this.baseGetRequest("/project/config/meta/detail", {
      project_id: projectID,
    });
  }

  async getNoneBotConfig(projectID: string): Promise<ModuleConfigResponse> {
    return await this.baseGetRequest("/project/config/nonebot/detail", {
      project_id: projectID,
    });
  }

  async getProjectPluginConfigList(projectID: string): Promise<ModuleConfigResponse> {
    return await this.baseGetRequest("/project/config/nonebot/plugins/detail", {
      project_id: projectID,
    });
  }

  async getEnvs(projectID: string): Promise<GenericResponse<string[]>> {
    return await this.baseGetRequest("/project/config/env/list", {
      project_id: projectID,
    });
  }

  async createEnv(env: string, projectID: string): Promise<GenericResponse<string>> {
    return await this.basePostRequest("/project/config/env/create", {
      env: env,
      project_id: projectID,
    });
  }

  async deleteEnv(env: string, projectID: string): Promise<GenericResponse<string>> {
    return await this.baseDeleteRequest("/project/config/env/delete", {
      env: env,
      project_id: projectID,
    });
  }

  async useEnv(env: string, projectID: string): Promise<GenericResponse<string>> {
    return await this.basePostRequest(
      "/project/config/env/use",
      {},
      {
        env: env,
        project_id: projectID,
      },
    );
  }

  async configUpdate(
    moduleType: string,
    projectID: string,
    env: string,
    keyType: string,
    k: string,
    v: any,
  ): Promise<GenericResponse<string>> {
    return await this.basePostRequest(
      "/project/config/update",
      {
        env: env,
        key_type: keyType,
        k: k,
        v: v,
      },
      {
        module_type: moduleType,
        project_id: projectID,
      },
    );
  }

  async checkProjectToml(projectDir: string): Promise<CheckProjectTomlResponse> {
    return await this.basePostRequest(
      "/project/check_toml",
      {},
      {
        project_dir: projectDir,
      },
    );
  }
}
