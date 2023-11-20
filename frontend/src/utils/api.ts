import axios from "axios";
import type {
  AxiosError,
  AxiosInstance,
  AxiosResponse,
  InternalAxiosRequestConfig,
} from "axios";

import { getURL } from ".";

export abstract class CustomAPI {
  protected request: AxiosInstance = axios.create();
  public abstract basePoint: string;

  constructor() {
    const basePointHandler = {
      set: (target: CustomAPI, key: string, value: string) => {
        if (key === "basePoint") {
          value = value.startsWith("/") ? value : "/" + value;
          value = value.endsWith("/") ? value.slice(0, -1) : value;

          this.request = axios.create({
            baseURL: getURL(value),
          });

          this.request.interceptors.request.use(
            async (config: InternalAxiosRequestConfig) => {
              return await this.beforeRequest(config);
            },
            async (error: AxiosError) => {
              return await this.beforeRequestError(error);
            },
          );

          this.request.interceptors.response.use(
            async (response: AxiosResponse) => {
              return await this.afterRequest(response);
            },
            async (error: AxiosError) => {
              return await this.afterRequestError(error);
            },
          );
        }
        target.basePoint = value;
        return true;
      },
    };

    return new Proxy(this, basePointHandler);
  }

  protected async beforeRequest(
    config: InternalAxiosRequestConfig,
  ): Promise<InternalAxiosRequestConfig> {
    return config;
  }

  protected async beforeRequestError(error: AxiosError): Promise<any> {}

  protected async afterRequest(response: AxiosResponse): Promise<AxiosResponse> {
    return response;
  }

  protected async afterRequestError(error: AxiosError): Promise<any> {}
}
