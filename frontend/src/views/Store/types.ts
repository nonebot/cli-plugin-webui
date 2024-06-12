export interface PypiInfo {
  info: Info
  last_serial: number
  releases: Releases
  urls: Url[]
  vulnerabilities: any[]
}

interface Info {
  author: string
  author_email: string
  bugtrack_url: any
  classifiers: string[]
  description: string
  description_content_type: string
  docs_url: any
  download_url: string
  downloads: Downloads
  dynamic: any
  home_page: string
  keywords: string
  license: string
  maintainer: string
  maintainer_email: string
  name: string
  package_url: string
  platform: any
  project_url: string
  project_urls: ProjectUrls
  provides_extra: any
  release_url: string
  requires_dist: string[]
  requires_python: string
  summary: string
  version: string
  yanked: boolean
  yanked_reason: any
}

interface Downloads {
  last_day: number
  last_month: number
  last_week: number
}

interface ProjectUrls {
  Documentation: string
  Homepage: string
  Repository: string
}

interface Releases {
  [key: string]: ReleaseInfo[]
}

interface ReleaseInfo {
  comment_text: string
  digests: Digests
  downloads: number
  filename: string
  has_sig: boolean
  md5_digest: string
  packagetype: string
  python_version: string
  requires_python: string
  size: number
  upload_time: string
  upload_time_iso_8601: string
  url: string
  yanked: boolean
  yanked_reason: any
}

interface Digests {
  blake2b_256: string
  md5: string
  sha256: string
}

interface Url {
  comment_text: string
  digests: Digests
  downloads: number
  filename: string
  has_sig: boolean
  md5_digest: string
  packagetype: string
  python_version: string
  requires_python: string
  size: number
  upload_time: string
  upload_time_iso_8601: string
  url: string
  yanked: boolean
  yanked_reason: any
}
