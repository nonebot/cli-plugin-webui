import { client } from './api'

export const covertTimestampToDateString = (
  timestamp: string,
  options: any = {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  }
) => {
  const fixedTimestamp = Number(timestamp) * 1000
  const date = new Date(fixedTimestamp)
  return date.toLocaleDateString(navigator.language, options)
}

export const limitContentShow = (content: string, limit: number) => {
  if (content.length <= limit) {
    return content
  }
  return content.slice(0, limit) + '...'
}

export const generateURLForWebUI = (path: string, isWebsocket = false) => {
  const base = client.getConfig().baseUrl!
  const protocol = isWebsocket ? 'ws' : 'http'
  return `${protocol}://${base}${path}`
}

export const sleep = (ms: number) => {
  return new Promise((resolve) => setTimeout(resolve, ms))
}

export const compareSemanticVersion = (v1: string, v2: string) => {
  const parseVersion = (v: string) => {
    const [main, pre] = v.split('-')
    const parts = main.split('.').map(Number)
    return { parts, pre: pre || null }
  }

  const v1Parsed = parseVersion(v1)
  const v2Parsed = parseVersion(v2)

  // 逐位比较主版本号
  const maxLength = Math.max(v1Parsed.parts.length, v2Parsed.parts.length)
  for (let i = 0; i < maxLength; i++) {
    const part1 = v1Parsed.parts[i] || 0
    const part2 = v2Parsed.parts[i] || 0

    if (part1 > part2) return 1
    if (part1 < part2) return -1
  }

  // 比较预发行版本
  if (!v1Parsed.pre && v2Parsed.pre) return 1 // v1 是正式版，v2 是预发行版
  if (v1Parsed.pre && !v2Parsed.pre) return -1 // v1 是预发行版，v2 是正式版
  if (v1Parsed.pre && v2Parsed.pre) return v1Parsed.pre.localeCompare(v2Parsed.pre) // 按字典顺序比较预发行版本

  return 0 // 完全相等
}
