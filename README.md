<!-- markdownlint-disable MD033 MD041 -->
<p align="center">
  <a href="https://cli.nonebot.dev/"><img src="https://cli.nonebot.dev/logo.png" width="200" height="200" alt="nonebot"></a>
</p>

<div align="center">

# NB CLI Plugin WebUI

_✨ NoneBot2 命令行工具 前端可视化页面（WebUI） 插件 ✨_

</div>

<p align="center">
  <a href="https://raw.githubusercontent.com/nonebot/nb-cli-plugin-webui/master/LICENSE">
    <img src="https://img.shields.io/github/license/nonebot/cli-plugin-webui" alt="license">
  </a>
  <a href="https://pypi.python.org/pypi/nb-cli-plugin-webui">
    <img src="https://img.shields.io/pypi/v/nb-cli-plugin-webui" alt="pypi">
  </a>
  <img src="https://img.shields.io/badge/python-3.8+-blue" alt="python">
  <a href="https://results.pre-commit.ci/latest/github/nonebot/nb-cli-plugin-webui/master">
    <img src="https://results.pre-commit.ci/badge/github/nonebot/cli-plugin-webui/master.svg" alt="pre-commit" />
  </a>
  <br />
  <a href="https://jq.qq.com/?_wv=1027&k=5OFifDh">
    <img src="https://img.shields.io/badge/QQ%E7%BE%A4-768887710-orange?style=flat-square" alt="QQ Chat Group">
  </a>
  <a href="https://qun.qq.com/qqweb/qunpro/share?_wv=3&_wwv=128&appChannel=share&inviteCode=7b4a3&appChannel=share&businessType=9&from=246610&biz=ka">
    <img src="https://img.shields.io/badge/QQ%E9%A2%91%E9%81%93-NoneBot-5492ff?style=flat-square" alt="QQ Channel">
  </a>
  <a href="https://t.me/botuniverse">
    <img src="https://img.shields.io/badge/telegram-botuniverse-blue?style=flat-square" alt="Telegram Channel">
  </a>
  <a href="https://discord.gg/VKtE6Gdc4h">
    <img src="https://discordapp.com/api/guilds/847819937858584596/widget.png?style=shield" alt="Discord Server">
  </a>
</p>

## 功能

- 可视化的 nb cli 操作
  - 创建新的 NoneBot 实例
  - 添加已有的 NoneBot 实例
  - 拓展（插件、适配器、驱动器）管理（安装、卸载）
- 可同时管理多个 NoneBot 实例
- 为启动的 NoneBot 实例提供状态展示、性能查询
- 可视化的 NoneBot 实例配置

## 使用

### 安装

**需要 [nb-cli](https://github.com/nonebot/nb-cli/)**

使用 nb-cli 安装

```shell
nb self install nb-cli-plugin-webui
```

使用 Docker 运行

```shell
docker pull nonebot/cil-plugin-webui:latest
```

Docker 镜像可以选择以下版本:

- `latest`, `latest-slim`: 最新的稳定版本 (Release)
- `latest-${python 版本}`, `latest-slim-${python 版本}`: 指定 Python 版本的最新版本
- `sha-${commit sha:0:7}-${python 版本}`, `sha-${commit sha:0:7}-${python 版本}-slim`: 指定 commit 的版本
- `${branch}-${python 版本}`, `${branch}-${python 版本}-slim`: 指定分支的最新版本

### 命令行使用

```shell
nb ui --help
```

Docker 镜像使用

```shell
docker run -it --rm -p 8080:8080 -v ./:/app nonebot/cli-plugin-webui:latest --help
```

可选附加 env 参数:

- HOST: 指定监听地址，默认为 `0.0.0.0`
- PORT: 指定监听端口，默认为 `8080`

## 开发

待补充......

## 补充

nb-cli WebUI 目前正处于快速迭代中，欢迎各位提交在使用过程中发现的 BUG 和建议。
