import axios, { AxiosResponse, InternalAxiosRequestConfig } from "axios";

import { router } from "@/router";
import { globalStore } from "@/store/app";

axios.interceptors.request.use(
  async (config: InternalAxiosRequestConfig) => {
    const jwtToken = localStorage.getItem("jwtToken");
    if (jwtToken) {
      config.headers.Authorization = `Bearer ${jwtToken}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  },
);

axios.interceptors.response.use(
  async (response: AxiosResponse) => {
    return response;
  },
  (error) => {
    if (error.response && error.response.status === 403) {
      localStorage.removeItem("jwtToken");
      router.push("#auth-card");
      globalStore().isAuth = false;
    }
    return Promise.reject(error);
  },
);
