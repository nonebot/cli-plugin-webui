import type { ProcessInfo } from "@/api/schemas";

interface PlatformProfile {
  name: string;
  struct: string;
  platform_type: string;
}

interface Cpu {
  name: string;
  count: number;
  max_freq: string;
  current_freq: string;
  percent: number;
  process: number;
}

interface Mem {
  total: number;
  available: number;
  percent: number;
  used: number;
  free: number;
}

interface Disk {
  total: number;
  used: number;
  free: number;
  speed: number[];
}

interface Net {
  sent_total: number;
  recv_total: number;
  package_sent: number;
  package_recv: number;
  speed: number[];
}

interface SystemInfo {
  platform: PlatformProfile;
  cpu: Cpu;
  mem: Mem;
  disk: Disk;
  net: Net;
}

export interface StatusInfo {
  system: SystemInfo;
  process?: ProcessInfo;
}
