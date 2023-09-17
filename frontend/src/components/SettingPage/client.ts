import { API } from "@/api";
import { BaseConfig } from "@/config";
import type { Config } from "@/types";
import { appStore as store } from "@/store/global";
import { webuiConfig } from "@/config";
import { settingStore } from "@/store/setting";
import { appStore } from "@/store/global";
import { ToastWrapper } from "@/utils/notification";
import { AxiosError } from "axios";

const api = new API();
export const notice = new ToastWrapper("NoneBot Setting");

class ProjectMetaConfig extends BaseConfig {
  constructor() {
    super("Project Meta", "实例相关设置", "project");
  }

  async genConfig(projectID: string): Promise<Config> {
    let resp: any;

    await api
      .getProjectMetaConfig(projectID)
      .then((response) => {
        resp = response.detail;
        return Promise.resolve();
      })
      .catch((error: AxiosError) => {
        throw error;
      });

    const setAction = async (k: string, v: any, keyType: string) => {
      await api
        .configSet(
          store().choiceProject.project_id,
          this.name,
          store().enabledEnv,
          keyType,
          k,
          v,
        )
        .then(() => {
          return Promise.resolve();
        })
        .catch((error: AxiosError) => {
          let reason: string;
          if (error.response) {
            reason = (error.response.data as { detail: string })?.detail;
          } else {
            reason = error.message;
          }
          notice.error(`更新实例 meta 设置失败：${reason}`);
        });

      await api
        .getProjectDetail(appStore().choiceProject.project_id)
        .then((resp) => {
          appStore().choiceProject = resp;
          return Promise.resolve();
        })
        .catch((error: AxiosError) => {
          let reason: string;
          if (error.response) {
            reason = (error.response.data as { detail: string })?.detail;
          } else {
            reason = error.message;
          }
          notice.error(`获取实例 meta 信息失败：${reason}`);
        });

      await getProjectMetaConfig();
    };

    const getAction = () => {};

    const result: Config = {
      title: this.title,
      description: this.description,
      name: this.name,
      setAction: setAction,
      getAction: getAction,
      properties: resp,
    };
    return result;
  }
}

class NonebotConfig extends BaseConfig {
  constructor() {
    super("Nonebot", "Nonebot 本体相关设置", "nonebot");
  }

  async genConfig(projectID: string): Promise<Config> {
    let resp: any;

    await api
      .getNonebotConfig(projectID)
      .then((response) => {
        resp = response.detail;
        return Promise.resolve();
      })
      .catch((error: AxiosError) => {
        throw error;
      });

    const setAction = async (k: string, v: any, keyType: string) => {
      await api
        .configSet(
          store().choiceProject.project_id,
          this.name,
          store().enabledEnv,
          keyType,
          k,
          v,
        )
        .then(() => {
          return Promise.resolve();
        })
        .catch((error: AxiosError) => {
          let reason: string;
          if (error.response) {
            reason = (error.response.data as { detail: string })?.detail;
          } else {
            reason = error.message;
          }
          notice.error(`更新 NoneBot 设置失败：${reason}`);
        });

      await getNonebotConfig();
    };

    const getAction = () => {};

    const result: Config = {
      title: this.title,
      description: this.description,
      name: this.name,
      setAction: setAction,
      getAction: getAction,
      properties: resp,
    };
    return result;
  }
}

class PluginConfig extends BaseConfig {
  constructor() {
    super("Nonebot Plugin", "Nonebot Plugin 相关设置。", "nonebot_plugin");
  }

  async genConfig(projectID: string): Promise<Config> {
    let resp: any;

    await api
      .getProjectPluginConfigList(projectID)
      .then((response) => {
        resp = response.detail;
        return Promise.resolve();
      })
      .catch((error: AxiosError) => {
        throw error;
      });

    const setAction = async (k: string, v: any, keyType: string) => {
      await api
        .configSet(
          store().choiceProject.project_id,
          this.name,
          store().enabledEnv,
          keyType,
          k,
          v,
        )
        .then(() => {
          return Promise.resolve();
        })
        .catch((error: AxiosError) => {
          let reason: string;
          if (error.response) {
            reason = (error.response.data as { detail: string })?.detail;
          } else {
            reason = error.message;
          }
          notice.error(`更新 NoneBot 插件设置失败：${reason}`);
        });

      await getNonebotPluginConfig();
    };

    const getAction = () => {};

    const result: Config = {
      title: this.title,
      description: this.description,
      name: this.name,
      setAction: setAction,
      getAction: getAction,
      properties: resp,
    };
    return result;
  }
}

const projectMetaConfig = new ProjectMetaConfig();
const nonebotConfig = new NonebotConfig();
const pluginConfig = new PluginConfig();

export const getWebUIConfig = () => {
  try {
    settingStore().webuiConfigList = webuiConfig.genConfig();
  } catch (error: any) {
    notice.error(`获取 WebUI 设置失败：${error}`);
  }
};

export const getProjectMetaConfig = async () => {
  try {
    settingStore().projectMetaConfigList = await projectMetaConfig.genConfig(
      appStore().choiceProject.project_id,
    );
  } catch (error: any) {
    let reason: string;
    if (error.response) {
      reason = (error.response.data as { detail: string })?.detail;
    } else {
      reason = error.message;
    }
    notice.error(`获取实例 meta 设置失败：${reason}`);
  }
};

export const getNonebotConfig = async () => {
  try {
    settingStore().nonebotConfigList = await nonebotConfig.genConfig(
      appStore().choiceProject.project_id,
    );
  } catch (error: any) {
    let reason: string;
    if (error.response) {
      reason = (error.response.data as { detail: string })?.detail;
    } else {
      reason = error.message;
    }
    notice.error(`获取 NoneBot 设置失败：${reason}`);
  }
};

export const getNonebotPluginConfig = async () => {
  try {
    settingStore().pluginConfigList = await pluginConfig.genConfig(
      appStore().choiceProject.project_id,
    );
  } catch (error: any) {
    let reason: string;
    if (error.response) {
      reason = (error.response.data as { detail: string })?.detail;
    } else {
      reason = error.message;
    }
    notice.error(`获取 NoneBot 插件设置失败：${reason}`);
  }
};

export const getConfig = async () => {
  getWebUIConfig();
  await getProjectMetaConfig();
  await getNonebotConfig();
  await getNonebotPluginConfig();
};
