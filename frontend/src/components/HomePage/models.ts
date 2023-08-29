export interface SystemStatsData {
  system_stats: SystemStats;
}

export interface SystemStats {
  platform: Platform;
  cpu: Cpu;
  mem: Mem;
  disk: Disk;
  net: Net;
}

export interface Platform {
  name: string;
  struct: string;
  platform_type: string;
}

export interface Cpu {
  name: string;
  count: number;
  max_freq: string;
  current_freq: string;
  percent: number;
  process: number;
}

export interface Mem {
  total: number;
  available: number;
  percent: number;
  used: number;
  free: number;
}

export interface Disk {
  total: number;
  used: number;
  free: number;
  speed: number[];
}

export interface Net {
  sent_total: number;
  recv_total: number;
  package_sent: number;
  package_recv: number;
  speed: number[];
}
