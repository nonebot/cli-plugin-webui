import { router } from "@/router";
import type { AxiosError, InternalAxiosRequestConfig } from "axios";

import { CustomAPI } from "@/utils/api";
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

class API extends CustomAPI {
  public basePoint = "/api/v1";

  protected async beforeRequest(
    config: InternalAxiosRequestConfig,
  ): Promise<InternalAxiosRequestConfig> {
    const token = localStorage.getItem("jwtToken");
    config.headers.Authorization = `Bearer ${token}`;

    return config;
  }

  protected async beforeRequestError(error: AxiosError): Promise<AxiosError> {
    return Promise.reject(error);
  }

  protected async afterRequestError(error: AxiosError): Promise<AxiosError> {
    if (error.response && error.response.status === 403) {
      localStorage.removeItem("jwtToken");
      router.push("/login");
    }

    return Promise.reject(error);
  }

  async doLogin(token: string): Promise<GenericResponse<string>> {
    const mark = new Date().toString();
    return await this.request.post("/auth/login", {
      token: token,
      mark: mark,
    });
  }

  async getFileList(path: string): Promise<FileResponse> {
    return await this.request.get("/file/list", {
      params: {
        path: path,
      },
    });
  }

  async createFile(
    fileName: string,
    isFolder: boolean,
    path: string,
  ): Promise<FileResponse> {
    return await this.request.post("/file/create", {
      name: fileName,
      is_dir: isFolder,
      path: path,
    });
  }

  async deleteFile(path: string): Promise<FileResponse> {
    return await this.request.delete("/file/delete", {
      params: {
        path: path,
      },
    });
  }

  async installModule(
    env: string,
    module: SimpleInfo | Plugin,
    projectID: string,
  ): Promise<GenericResponse<string>> {
    const module_type = "valid" in module ? "plugin" : "module";
    const data = { module_type: module_type, ...module };
    return await this.request.post("/store/nonebot/install", data, {
      params: {
        env: env,
        project_id: projectID,
      },
    });
  }

  async uninstallModule(
    env: string,
    module: SimpleInfo | Plugin,
    projectID: string,
  ): Promise<GenericResponse<string>> {
    const module_type = "valid" in module ? "plugin" : "module";
    const data = { module_type: module_type, ...module };
    return await this.request.post("/store/nonebot/uninstall", data, {
      params: {
        env: env,
        project_id: projectID,
      },
    });
  }

  async getNoneBotModules(
    moduleType: string,
    page: number,
    projectID?: string,
    isSearch?: boolean,
    showAll?: boolean,
  ): Promise<StoreListResponse> {
    return await this.request.get("/store/nonebot/list", {
      params: {
        module_type: moduleType,
        page: page,
        project_id: projectID,
        is_search: isSearch,
        show_all: showAll,
      },
    });
  }

  async searchStore(
    projectID: string,
    moduleType: string,
    content: string,
  ): Promise<StoreListResponse> {
    return await this.request.post("/store/nonebot/search", undefined, {
      params: {
        project_id: projectID,
        module_type: moduleType,
        content: content,
      },
    });
  }

  async runProject(projectID: string): Promise<GenericResponse<string>> {
    return await this.request.post("/process/run", undefined, {
      params: {
        project_id: projectID,
      },
    });
  }

  async stopProject(projectID: string): Promise<GenericResponse<string>> {
    return await this.request.post("/process/stop", undefined, {
      params: {
        project_id: projectID,
      },
    });
  }

  async writeToProjectProcessStdin(
    content: string,
    projectID: string,
  ): Promise<GenericResponse<number>> {
    return await this.request.post("/process/write", undefined, {
      params: {
        content: content,
        project_id: projectID,
      },
    });
  }

  async getProcessLogHistory(
    logID: string,
    logCount: number,
  ): Promise<GenericResponse<ProcessLog[]>> {
    return await this.request.get("/process/log/history", {
      params: {
        log_id: logID,
        log_count: logCount,
      },
    });
  }

  async getEnvs(projectID: string): Promise<GenericResponse<string[]>> {
    return await this.request.get("/project/config/env/list", {
      params: {
        project_id: projectID,
      },
    });
  }

  async createEnv(env: string, projectID: string): Promise<GenericResponse<string>> {
    return await this.request.post("/project/config/env/create", {
      env: env,
      project_id: projectID,
    });
  }

  async deleteEnv(env: string, projectID: string): Promise<GenericResponse<string>> {
    return await this.request.delete("/project/config/env/delete", {
      params: {
        env: env,
        project_id: projectID,
      },
    });
  }

  async useEnv(env: string, projectID: string): Promise<GenericResponse<string>> {
    return await this.request.post("/project/config/env/use", undefined, {
      params: {
        env: env,
        project_id: projectID,
      },
    });
  }

  async getProjectMetaConfig(projectID: string): Promise<ModuleConfigResponse> {
    return await this.request.get("/project/config/meta/detail", {
      params: {
        project_id: projectID,
      },
    });
  }

  async getNoneBotConfig(projectID: string): Promise<ModuleConfigResponse> {
    return await this.request.get("/project/config/nonebot/detail", {
      params: {
        project_id: projectID,
      },
    });
  }

  async getProjectPluginConfigList(projectID: string): Promise<ModuleConfigResponse> {
    return await this.request.get("/project/config/nonebot/plugins/detail", {
      params: {
        project_id: projectID,
      },
    });
  }

  async configUpdate(
    moduleType: string,
    projectID: string,
    env: string,
    keyType: string,
    k: string,
    v: any,
  ): Promise<GenericResponse<string>> {
    return await this.request.post(
      "/project/config/update",
      {
        env: env,
        key_type: keyType,
        k: k,
        v: v,
      },
      {
        params: {
          module_type: moduleType,
          project_id: projectID,
        },
      },
    );
  }

  async createProject(data: CreateProjectData): Promise<GenericResponse<string>> {
    return await this.request.post("/project/create", data);
  }

  async addProject(data: AddProjectData): Promise<GenericResponse<string>> {
    return await this.request.post("/project/add", data);
  }

  async getProjectProfile(
    projectID: string,
  ): Promise<GenericResponse<NoneBotProjectMeta>> {
    return await this.request.get("/project/profile", {
      params: {
        project_id: projectID,
      },
    });
  }

  async deleteProject(projectID: string): Promise<GenericResponse<string>> {
    return await this.request.delete("/project/delete", {
      params: {
        project_id: projectID,
      },
    });
  }

  async getProjectList(): Promise<
    GenericResponse<{ [key: string]: NoneBotProjectMeta }>
  > {
    return await this.request.get("/project/list");
  }

  async checkProjectToml(projectDir: string): Promise<CheckProjectTomlResponse> {
    return await this.request.post("/project/check_toml", undefined, {
      params: {
        project_dir: projectDir,
      },
    });
  }
}

const api = new API();
api.basePoint = "/api/v1";
export default api;
