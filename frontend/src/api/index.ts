import axios, { AxiosResponse } from "axios";

import { isDebug } from "@/core/utils";
import {
  AdaptersResponse,
  FileOperateRequest,
  DriversResponse,
  FileListResponse,
  IsAvailableResponse,
  LoginRequest,
  LoginResponse,
  CreateProjectRequest,
  CreateProjectResponse,
  CreateProjectData,
  NonebotProjectListResponse,
  DeleteProjectResponse,
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

  async doLogin(token: string): Promise<LoginResponse> {
    const mark = new Date().toString();
    const requestData: LoginRequest = {
      login_data: {
        token: token,
        mark: mark,
      },
    };
    return await this.basePostRequest<LoginResponse>(
      "/auth/login",
      requestData,
    );
  }

  async isAvailable(): Promise<IsAvailableResponse> {
    return await this.baseGetRequest<IsAvailableResponse>("/auth/is_available");
  }

  async getAdapters(): Promise<AdaptersResponse> {
    return await this.baseGetRequest<AdaptersResponse>("/adapter/list");
  }

  async getDrivers(): Promise<DriversResponse> {
    return await this.baseGetRequest<DriversResponse>("/driver/list");
  }

  async getFileList(path: string): Promise<FileListResponse> {
    const requestData = {
      path: path,
    };
    return await this.baseGetRequest<FileListResponse>(
      "/files/list",
      requestData,
    );
  }

  async createFile(
    fileName: string,
    isFolder: boolean,
    path: string,
  ): Promise<FileListResponse> {
    const requestData: FileOperateRequest = {
      file_data: {
        name: fileName,
        is_dir: isFolder ? 1 : 0,
        path: path,
      },
    };
    return await this.basePostRequest<FileListResponse>(
      "/files/create",
      requestData,
    );
  }

  async deleteFile(
    fileName: string,
    isFolder: boolean,
    path: string,
  ): Promise<FileListResponse> {
    const requestData: FileOperateRequest = {
      file_data: {
        name: fileName,
        is_dir: isFolder ? 1 : 0,
        path: path,
      },
    };
    return await this.basePostRequest<FileListResponse>(
      "/files/delete",
      requestData,
    );
  }

  async createProject(data: CreateProjectData): Promise<CreateProjectResponse> {
    const requestData: CreateProjectRequest = {
      project_data: data,
    };
    return await this.basePostRequest<CreateProjectResponse>(
      "/project/create",
      requestData,
    );
  }

  async getProjectList(): Promise<NonebotProjectListResponse> {
    return await this.baseGetRequest<NonebotProjectListResponse>(
      "/project/list",
    );
  }

  async deleteProject(project_id: string): Promise<DeleteProjectResponse> {
    const requestData = {
      project_id: project_id,
    };
    return await this.basePostRequest<DeleteProjectResponse>(
      "/project/delete",
      requestData,
    );
  }
}
