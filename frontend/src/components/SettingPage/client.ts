import { API } from "@/api";
import { BaseConfig } from "@/config";
import type { Config } from "@/types";
import { appStore as store } from "@/store/global";
import { webuiConfig } from "@/config";
import { settingStore } from "@/store/setting";
import { appStore } from "@/store/global";

const api = new API();

class ProjectMetaConfig extends BaseConfig {
  constructor() {
    super("Project Meta", "实例相关设置", "project");
  }

  async genConfig(projectID: string): Promise<Config> {
    let resp;

    try {
      resp = await api.getProjectMetaConfig(projectID);
    } catch (error: any) {
      console.log(`获取 project meta 失败：${error}`);
      throw error;
    }

    const setAction = async (k: string, v: any, keyType: string) => {
      try {
        await api.configSet(
          store().choiceProject.project_id,
          this.name,
          store().enabledEnv,
          keyType,
          k,
          v,
        );
        await api.getProjectMetaConfig(store().choiceProject.project_id);
      } catch (error: any) {}
    };

    const getAction = () => {};

    const result: Config = {
      title: this.title,
      description: this.description,
      name: this.name,
      setAction: setAction,
      getAction: getAction,
      properties: resp.detail,
    };
    return result;
  }
}

class NonebotConfig extends BaseConfig {
  constructor() {
    super("Nonebot", "Nonebot 本体相关设置", "nonebot");
  }

  async genConfig(projectID: string): Promise<Config> {
    let resp;

    try {
      resp = await api.getNonebotConfig(projectID);
    } catch (error: any) {
      console.log(`获取 nonebot config 失败：${error}`);
      throw error;
    }

    const setAction = async (k: string, v: any, keyType: string) => {
      try {
        await api.configSet(
          store().choiceProject.project_id,
          this.name,
          store().enabledEnv,
          keyType,
          k,
          v,
        );
        await api.getNonebotConfig(store().choiceProject.project_id);
      } catch (error: any) {}
    };

    const getAction = () => {};

    const result: Config = {
      title: this.title,
      description: this.description,
      name: this.name,
      setAction: setAction,
      getAction: getAction,
      properties: resp.detail,
    };
    return result;
  }
}

class PluginConfig extends BaseConfig {
  constructor() {
    super("Nonebot Plugin", "Nonebot Plugin 相关设置。", "nonebot_plugin");
  }

  async genConfig(projectID: string): Promise<Config> {
    let resp;

    try {
      resp = await api.getProjectPluginConfigList(projectID);
    } catch (error: any) {
      console.log(`获取 nb plugin config 失败：${error}`);
      throw error;
    }

    const setAction = async (k: string, v: any, keyType: string) => {
      try {
        await api.configSet(
          store().choiceProject.project_id,
          this.name,
          store().enabledEnv,
          keyType,
          k,
          v,
        );
        await getNonebotPluginConfig();
      } catch (error: any) {}
    };

    const getAction = () => {};

    const result: Config = {
      title: this.title,
      description: this.description,
      name: this.name,
      setAction: setAction,
      getAction: getAction,
      properties: resp.detail,
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
  } catch (error: any) {}
};

export const getProjectMetaConfig = async () => {
  try {
    settingStore().projectMetaConfigList = await projectMetaConfig.genConfig(
      appStore().choiceProject.project_id,
    );
  } catch (error: any) {}
};

export const getNonebotConfig = async () => {
  try {
    settingStore().nonebotConfigList = await nonebotConfig.genConfig(
      appStore().choiceProject.project_id,
    );
  } catch (error: any) {}
};

export const getNonebotPluginConfig = async () => {
  try {
    settingStore().pluginConfigList = await pluginConfig.genConfig(
      appStore().choiceProject.project_id,
    );
  } catch (error: any) {}
};

export const getConfig = async () => {
  getWebUIConfig();
  await getProjectMetaConfig();
  await getNonebotConfig();
  await getNonebotPluginConfig();
};
