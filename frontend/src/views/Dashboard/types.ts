import type { LoadingOptions } from '@/types'
import type { ComputedRef } from 'vue'

type PlatformProfile = {
  name: string
  struct: string
  platform_type: string
}

type Cpu = {
  name: string
  count: number
  max_freq: string
  current_freq: string
  percent: number
  process: number
}

type Mem = {
  total: number
  available: number
  percent: number
  used: number
  free: number
}

type Disk = {
  total: number
  used: number
  free: number
  speed: number[]
}

type Net = {
  sent_total: number
  recv_total: number
  package_sent: number
  package_recv: number
  speed: number[]
}

type SystemInfo = {
  platform: PlatformProfile
  cpu: Cpu
  mem: Mem
  disk: Disk
  net: Net
}

type ProcessPerformance = {
  cpu: number
  mem: number
}

type ProcessInfo = {
  status_code?: number
  total_logs: number
  is_running: boolean
  performance?: ProcessPerformance
}

export type StatusInfo = {
  system: SystemInfo
  process?: ProcessInfo
}

type NumberOrStringArray = (string | number)[]

export type ChartItem = {
  title: string
  subtitle: ComputedRef<string>
  isLoading?: ComputedRef<boolean>
  loadingOptions?: LoadingOptions
  timeData: NumberOrStringArray
  data: {
    name?: string
    data: NumberOrStringArray
  }[]
}
