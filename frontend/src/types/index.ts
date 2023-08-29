interface ModuleConfigSimpleInfo {
  title: string;
  description: string;
  name: string;
}

interface ModuleConfigChild extends ModuleConfigSimpleInfo {
  default: any;
  item_type: string;
  enum: string[] | number[];
  configured: any;
  latest_change?: string;
  exclusiveMinimum?: number;
  minimum?: number;
  exclusiveMaximum?: number;
  maximum?: number;
}

export interface ModuleConfigFather extends ModuleConfigSimpleInfo {
  properties: ModuleConfigChild[];
}

export interface Config {
  title: string;
  description: string;
  name: string;
  setAction: (...params: any[]) => void;
  getAction: (...params: any[]) => any;
  properties: ModuleConfigFather[];
}
