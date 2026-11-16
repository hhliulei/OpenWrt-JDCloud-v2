# 🚀 OpenWrt-JDCloud-v2 — 京东云雅典娜 / 太乙云编译固件（v2）

OpenWrt / ImmortalWrt / JDCloud RE-CS-02 / JDCloud RE-CS-07 / IPQ6010 / PPE / 云编译
> 基于 ImmortalWrt / LiBwrt / 官方 OpenWrt + 两条 PPE 实验路线的定制固件，适配京东云雅典娜 RE-CS-02（AX6600）与太乙 RE-CS-07（ER1），GitHub Actions 全自动云编译

[![Stars](https://img.shields.io/github/stars/hhliulei/OpenWrt-JDCloud-v2?style=flat&logo=github&label=Stars)](https://github.com/hhliulei/OpenWrt-JDCloud-v2/stargazers)
[![Downloads](https://img.shields.io/github/downloads/hhliulei/OpenWrt-JDCloud-v2/total?logo=github&label=%E4%B8%8B%E8%BD%BD%E9%87%8F)](https://github.com/hhliulei/OpenWrt-JDCloud-v2/releases)
[![Build](https://img.shields.io/github/actions/workflow/status/hhliulei/OpenWrt-JDCloud-v2/build.yml?label=%E7%BC%96%E8%AF%91)](https://github.com/hhliulei/OpenWrt-JDCloud-v2/actions)
[![Release Date](https://img.shields.io/github/release-date/hhliulei/OpenWrt-JDCloud-v2?label=%E6%9C%80%E6%96%B0%E5%8F%91%E5%B8%83)](https://github.com/hhliulei/OpenWrt-JDCloud-v2/releases)

[👉 进入项目主页](https://github.com/hhliulei/OpenWrt-JDCloud-v2)

> 本仓库是 v1（[OpenWrt-JDCloud](https://github.com/hhliulei/OpenWrt-JDCloud)，12 个固件）的
> v2：12 个配置按参考仓库做了有据可查的增补，并新增两条 PPE 路线（8 个固件）。
> 改动清单与出处见 [docs/V2-NOTES.md](docs/V2-NOTES.md)。

> ⚠️ **PPE 路线属实验性质**：`ppe` 与 `ppe-immwrt` 两条路线的 PPE 在 IPQ60xx 上
> 未经源码作者实测（作者实测机为小米 AX3600 / IPQ807x），编出来后请先实测
> （有线速率、WiFi、PPE 是否生效）再决定是否日常使用。首次构建（run #1）里
> 4 个 PPE 固件失败，原因见「构建状态」一节。

---

## ⭐ 项目特点

- 🔥 **云编译构建** — 基于 GitHub Actions 完全自动化编译，五个源码、两个机型、纯净版与插件版，一共 20 个固件
- 📦 **双机型支持** — 雅典娜 RE-CS-02（三频 WiFi 6 + 顶部点阵屏）与太乙 RE-CS-07（有线路由）同仓构建，固件不混用
- 🐧 **最新内核** — 各源码用其分支默认内核（ImmortalWrt 测试内核当前 6.18、LiBwrt 6.12、官方 main 当前 6.18、PPE 路线 6.18），不写死版本号
- ⚡ **硬件加速** — LiBwrt NSS 11.4（含雅典娜 WiFi offload）、ImmortalWrt NSS 12.5，官方 OpenWrt 走原生 flow offload；PPE 路线另有 Qualcomm PPE 开源硬件加速 + NSS WiFi（实验）
- 💡 **点阵屏控制** — 内置雅典娜 LED 点阵屏管理界面（athena-led）
- 🚀 **开箱即用** — 默认 LAN 192.168.10.1、主机名 ll、登录 root / root、Argon 主题、中文界面；插件版预装 OpenClash / PassWall2 / Docker / AdGuard Home / MosDNS / Aria2 等
- 🧩 **软件源完整** — 构建时不裁剪任何 feed，纯净版刷完也能在 LuCI「软件包」里按需装任意插件
- 🔄 **源码同步** — 每天 02:00 UTC（北京时间 10:00）自动拉取上游最新代码构建，每个固件只保留最新 2 个 Release；定时构建成功后，仓库根目录的 `upstream-lock.txt` 会自动更新为本次构建实际用的各源提交号

---

## 📥 快速开始

### 下载固件

| 版本 | 下载入口 | 适合场景 |
|------|----------|----------|
| 🍃 `PURE` 纯净版 | 🎯 **[👉 下载最新 PURE 固件](https://github.com/hhliulei/OpenWrt-JDCloud-v2/releases?q=PURE&expanded=true)** | 轻量稳定，日常推荐，插件按需自装 |
| 🚀 `PLUS` 插件版 | 🎯 **[👉 下载最新 PLUS 固件](https://github.com/hhliulei/OpenWrt-JDCloud-v2/releases?q=PLUS&expanded=true)** | OpenClash / PassWall2 / Docker / AdGuard Home 开箱即用 |

> 💡 打开后列表**最上方**即为该版本最新固件；也可浏览 [全部 Releases](https://github.com/hhliulei/OpenWrt-JDCloud-v2/releases)。

---

## 📋 固件说明

| 说明 | 详情 |
|------|------|
| **编译时间** | 显示的时间为编译开始时间，用于对应上游源码版本 |
| **版本划分** | 默认同时构建 `PURE` 纯净版与 `PLUS` 插件版 |
| **基础功能** | 纯净版保持轻量配置，包含完整网络功能栈，不过度精简 |
| **扩展插件** | 插件版额外集成 OpenClash、PassWall2、Docker / Dockerman、AdGuard Home、SmartDNS、MosDNS、DDNS、ttyd 终端、UPnP 等常用组件，也可通过自定义配置 `.config` 文件增加插件 |
| **硬件平台** | 基于 QUALCOMMAX（IPQ6010）架构 |
| **性能优化** | 针对 IPQ6010 平台进行网络性能调优；LiBwrt / ImmortalWrt 启用 NSS 加速，PPE 路线启用 PPE 硬件流表（实验） |

### 固件版本

| 版本 | 适合人群 | 预置内容 |
|------|----------|----------|
| `PURE` 纯净版 | 希望系统轻量、稳定，按需自行安装插件的用户 | 完整网络功能 + LuCI + 常用管理插件（防火墙、软件包管理、ARP 绑定、自动重启、Samba4、uHTTPd、CPU 调频等），另有 v2 增补的 zram、磁盘与诊断工具、WireGuard 协议支持、eMMC 健康监测 |
| `PLUS` 插件版 | 希望刷完即用常见扩展服务的用户 | 在纯净版基础上增加 OpenClash、PassWall2、Docker / Dockerman、AdGuard Home、SmartDNS、MosDNS、DDNS、ttyd 终端、UPnP、磁盘管理、网络唤醒、看门狗、硬盘休眠、Aria2、OpenList2、FRP、ACME、EasyTier、Lucky、PBR、SQM、iStore（仅 ImmortalWrt / LiBwrt 预装）等实用插件；PPE 路线另加 PPE 塑形 SQM（qca-ppe-qos）与 tc 调度模块；每个 Release 说明末尾的「插件信息」一节列出了本次构建实际编入的全部插件 |

> 💡 Releases 中的文件名会包含 `pure` 或 `plus`，请按需求下载对应版本。

### 文件命名与附件说明

**每个版本单独放一个 Release**：20 个固件（5 源码 × 2 机型 × 纯净/插件）各有
自己独立的 Release，不打包成一个大包；找固件时按 tag 前缀搜机型、源码或版本
即可，不用翻大包（参考 VIKINGYFY/OpenWRT-CI 的 Tags 做法）。

Release 的 tag 形如 `jdcloud_re-cs-02-immortalwrt-openwrt-25.12-pure-26.11.16-10.00.00`，
即 `<机型>-<源码>-<分支>-<版本>-<编译时间>`：机型在前，接着是源码、分支、
纯净版 / 插件版，最后是编译时间（精确到秒）。例如：

| tag | 对应固件 |
|-----|----------|
| `jdcloud_re-cs-02-immortalwrt-openwrt-25.12-pure-26.11.16-10.00.00` | 雅典娜 + ImmortalWrt（openwrt-25.12）+ 纯净版 |
| `jdcloud_re-cs-07-libwrt-25.12-nss-plus-26.11.16-10.00.00` | 太乙 + LiBwrt（25.12-nss）+ 插件版 |
| `jdcloud_re-cs-02-ppe-ppe-nss-plus-26.11.16-10.00.00` | 雅典娜 + PPE+NSS（ppe-nss，实验）+ 插件版 |
| `jdcloud_re-cs-02-ppe-immwrt-owrt-plus-26.11.16-10.00.00` | 雅典娜 + PPE ImmortalWrt 版（owrt，实验）+ 插件版 |

> 💡 2026-11-16 之前发布的 Release 用的是旧格式
> `ppe-jdcloud_re-cs-02-pure-26.11.16-1830`（`<源码>-<机型>-<版本>-<编译时间>`），
> 已有的旧 Release 不动；新格式只影响之后新发布的 Release，清理旧 Release 时
> 新旧两种格式一起按创建时间排、每个固件只保留最新 2 个。

每个 Release 包含以下文件：

| 文件 | 说明 |
|------|------|
| `*squashfs-sysupgrade-*.bin` | 固件本体；已是 OpenWrt / ImmortalWrt 时升级用 |
| `*squashfs-factory-*.bin` | 首次从原厂固件刷入用（只有 LiBwrt 的 Release 有） |
| `*initramfs-uImage.itb` | 内存启动镜像，用于首次刷机 / 救砖流程 |
| `*.manifest` | 固件包含的软件包清单 |
| `Config-*.txt` | 本次编译使用的完整 `.config`，便于复现构建或二次定制 |
| `Packages-*.txt` | 本次编译选中的软件包清单 |
| `sha256sums.txt` | 固件校验文件，刷机前请先校验下载完整性 |
| `upstream-lock.txt` | 本次构建实际用的源码提交号与追加 feed 列表 |

---

## 🧱 源码 / 分支 / 内核 / NSS / WiFi 对照表

| 源码 | 上游仓库 | 分支 | 内核 | NSS / PPE | WiFi |
| --- | --- | --- | --- | --- | --- |
| ImmortalWrt | `laipeng668/immortalwrt.git` | `openwrt-25.12` | 测试内核（当前 6.18） | NSS 12.5 | 雅典娜：正常 ath11k；太乙：无 |
| LiBwrt | `LiBwrt/openwrt-6.x.git` | `25.12-nss` | 6.12 | NSS 11.4 | 雅典娜：WiFi offload 开；太乙：无 |
| 官方 OpenWrt | `openwrt/openwrt.git` | `main`（快照，25.12 分支无 jdcloud 机型） | 跟 main 默认内核（当前 6.18） | 无（上游不含 NSS） | 雅典娜：正常 ath11k；太乙：无 |
| PPE+NSS（实验） | `JuliusBairaktaris/openwrt-ppe-nss.git` | `ppe-nss` | 6.18 | PPE（qca_ppe / qca_edma 硬件流表）+ NSS WiFi | 雅典娜：NSS WiFi offload；太乙：无 |
| PPE ImmortalWrt 版（实验） | `VIKINGYFY/immortalwrt.git` | `owrt` | 该分支默认 | PPE（满血）+ NSS WiFi | 雅典娜：NSS WiFi offload；太乙：无 |

内核不写死版本号：用各分支的默认内核，构建时以 Release 里附的
`upstream-lock.txt` 与 `Config-*.txt` 为准。详细说明与假设清单见 [SOURCES.md](SOURCES.md)。

## 固件矩阵（20 个）

| 源码 | 雅典娜 RE-CS-02 | 太乙 RE-CS-07 |
| --- | --- | --- |
| ImmortalWrt | 纯净版 / 插件版 | 纯净版 / 插件版 |
| LiBwrt openwrt-6.x | 纯净版 / 插件版 | 纯净版 / 插件版 |
| 官方 OpenWrt | 纯净版 / 插件版 | 纯净版 / 插件版 |
| PPE+NSS（实验） | 纯净版 / 插件版 | 纯净版 / 插件版 |
| PPE ImmortalWrt 版（实验） | 纯净版 / 插件版 | 纯净版 / 插件版 |

- 雅典娜：京东云无线宝 AX6600，三频 WiFi 6 + 顶部点阵屏，`jdcloud_re-cs-02`，1GB 内存。
- 太乙：京东云 ER1 有线路由，无 WiFi（NoWiFi），`jdcloud_re-cs-07`，2GB 内存。
- 平台都是 `qualcommax/ipq60xx`，SoC Qualcomm IPQ6010。

## 默认值

| 项目 | 默认值 |
| --- | --- |
| LAN | 192.168.10.1/24 |
| 主机名 | ll |
| 登录用户名 | root |
| 登录密码 | root |
| 主题 | Argon |
| 语言 | 中文 |
| 时区 | Asia/Shanghai |
| WiFi（仅雅典娜） | ll / ll-5G / ll-5G-2，密码 12345678 |

> ⚠️ 首次使用后请在 LuCI 里改掉登录密码与 WiFi 密码。

### WiFi 推荐设置（雅典娜三频）

雅典娜为三频机型，共三个 WiFi：2.4G（2×2，574Mbps）、5.2GHz 游戏频段 5G-1（4×4，4804Mbps）、5.8GHz 影音频段 5G-2（2×2，1201Mbps），信道和带宽按各自频段分别设置：

| WiFi | 信道 | 带宽 | 说明 |
|------|------|------|------|
| 2.4G（2×2） | `11` | `20MHz` | 抗干扰优先，拥挤环境下 20MHz 更稳 |
| 5G-1 游戏频段（4×4） | `44` | `160MHz` | 4×4 满血跑 160MHz 可达 4804Mbps；若无法开启或断流，回退 `80MHz` |
| 5G-2 影音频段（2×2） | `149` | `80MHz` | `149` 起在 US 下功率上限最高，非 DFS 无雷达断流 |

三个 WiFi 通用的设置：

| 项 | 推荐值 | 说明 |
|----|--------|------|
| 地区 | `US` | 可用信道多、功率上限高，推荐信道在 US 下均为非 DFS |
| 发射功率 | `24 dBm` | US 法规内的高功率档 |
| 加密 | `WPA2-PSK`，算法 `CCMP` | 兼容性最稳组合，老设备无障碍接入 |

## 🧩 插件矩阵

插件清单从仓库 `configs/` 下的 20 个 `.config` 真实提取（`CONFIG_PACKAGE_*=y`），
构建时 `make defconfig` 可能丢掉个别在该源码里不存在的包，
**最终以各 Release 里附的 `Config-*.txt` / `Packages-*.txt` 为准**。

| 分类 | 插件 | 来源 | 菜单位置 | 状态 |
| --- | --- | --- | --- | --- |
| 容器 | Docker（dockerd / docker / docker-compose） | 官方 / ImmortalWrt feed | 服务 → Docker | 仅 PLUS |
| 容器 | Dockerman（luci-app-dockerman） | 官方 / ImmortalWrt feed | 服务 → Docker | 仅 PLUS |
| 代理 | OpenClash | vernesong/OpenClash feed | 服务 → OpenClash | 仅 PLUS |
| 代理 | PassWall2 | OpenWrt-Passwall/openwrt-passwall2 feed | 服务 → PassWall2 | 仅 PLUS |
| DNS | AdGuard Home（luci-app-adguardhome） | 官方 / ImmortalWrt feed | 服务 → AdGuard Home | 仅 PLUS |
| DNS | SmartDNS（luci-app-smartdns） | 官方 / ImmortalWrt feed | 服务 → SmartDNS | 仅 PLUS |
| DNS | MosDNS（luci-app-mosdns） | 官方 / ImmortalWrt feed | 服务 → MosDNS | 仅 PLUS |
| 网络 | DDNS（luci-app-ddns + ddns-scripts） | 官方 / ImmortalWrt feed | 服务 → 动态 DNS | 仅 PLUS |
| 网络 | UPnP（luci-app-upnp） | 官方 / ImmortalWrt feed | 服务 → UPnP | 仅 PLUS |
| 网络 | SQM（luci-app-sqm） | 官方 / ImmortalWrt feed | 网络 → SQM | 仅 PLUS |
| 管理 | ttyd 终端（luci-app-ttyd） | 官方 / ImmortalWrt feed | 服务 → 终端 | 仅 PLUS |
| 管理 | 磁盘管理（luci-app-diskman） | 官方 / ImmortalWrt feed | 系统 → 磁盘管理 | 仅 PLUS |
| 管理 | 网络唤醒（luci-app-wol） | 官方 / ImmortalWrt feed | 服务 → 网络唤醒 | 仅 PLUS |
| 管理 | 看门狗（luci-app-watchcat） | 官方 / ImmortalWrt feed | 服务 → 看门狗 | 仅 PLUS |
| 管理 | 硬盘休眠（luci-app-hd-idle） | 官方 / ImmortalWrt feed | 系统 → 硬盘休眠 | 仅 PLUS |
| 管理 | 文件管理（luci-app-quickfile） | 官方 / ImmortalWrt feed | 服务 → 文件管理 | 仅 PLUS |
| 管理 | KMS（luci-app-vlmcsd） | 官方 / ImmortalWrt feed | 服务 → KMS | 仅 PLUS |
| 下载 | Aria2 + Ariang（luci-app-aria2） | 官方 / ImmortalWrt feed | 服务 → Aria2 | 仅 PLUS |
| 下载 | OpenList2（luci-app-openlist2） | 官方 / ImmortalWrt feed | 服务 → OpenList2 | 仅 PLUS |
| 远程 | FRP（luci-app-frpc / luci-app-frps） | 官方 / ImmortalWrt feed | 服务 → FRP | 仅 PLUS |
| 远程 | ACME 证书（luci-app-acme） | 官方 / ImmortalWrt feed | 服务 → ACME | 仅 PLUS |
| 组网 | EasyTier（luci-app-easytier） | 官方 / ImmortalWrt feed | 服务 → EasyTier | 仅 PLUS |
| 组网 | Lucky（luci-app-lucky） | 官方 / ImmortalWrt feed | 服务 → Lucky | 仅 PLUS |
| 分流 | PBR 策略路由（luci-app-pbr） | 官方 / ImmortalWrt feed | 网络 → PBR | 仅 PLUS |
| 分流 | netwiz（luci-app-netwiz） | 官方 / ImmortalWrt feed | 网络 → netwiz | 仅 PLUS |
| PPE | PPE 塑形 SQM（qca-ppe-qos + sqm-scripts + tc-tiny + kmod-sched-*） | PPE fork 自带 | 网络 → SQM | 仅 PLUS，且仅 PPE 路线 |
| 商店 | iStore（luci-app-store） | linkease/istore feed | 服务 → 应用商店 | 仅 PLUS，且仅 ImmortalWrt / LiBwrt 预装 |
| 基础 | 防火墙（luci-app-firewall） | 官方 / ImmortalWrt feed | 网络 → 防火墙 | PURE 与 PLUS 都有 |
| 基础 | 软件包管理（luci-app-package-manager） | 官方 / ImmortalWrt feed | 系统 → 软件包 | PURE 与 PLUS 都有 |
| 基础 | ARP 绑定（luci-app-arpbind） | 官方 / ImmortalWrt feed | 网络 → ARP 绑定 | PURE 与 PLUS 都有 |
| 基础 | 自动重启（luci-app-autoreboot） | 官方 / ImmortalWrt feed | 系统 → 自动重启 | PURE 与 PLUS 都有 |
| 基础 | CPU 调频（luci-app-cpufreq） | 官方 / ImmortalWrt feed | 系统 → CPU 调频 | PURE 与 PLUS 都有 |
| 基础 | Samba4 文件共享（luci-app-samba4） | 官方 / ImmortalWrt feed | 服务 → 网络共享 | PURE 与 PLUS 都有 |
| 基础 | uHTTPd 设置页（luci-app-uhttpd） | 官方 / ImmortalWrt feed | 系统 → uHTTPd | PURE 与 PLUS 都有 |
| 基础 | zram、exfat / ntfs3、USB 存储、tmux / btop / tcpdump、WireGuard 协议、eMMC 健康监测 | 官方 / ImmortalWrt feed | 命令行 / 后台，无菜单 | PURE 与 PLUS 都有 |
| 雅典娜 | 点阵屏（luci-app-athena-led） | NONGFAH/luci-app-athena-led | 系统 → 点阵屏 | PURE 与 PLUS 都有，仅雅典娜 |
| 主题 | Argon + Argon 配置（luci-theme-argon / luci-app-argon-config） | jerrykuku/luci-theme-argon | 系统 → 主题 | PURE 与 PLUS 都有 |
| 加速 | LiBwrt NSS（kmod-qca-nss-drv / kmod-qca-nss-ecm / sqm-scripts-nss + 扩展驱动） | LiBwrt 25.12-nss 自带 | 后台，无菜单 | PURE 与 PLUS 都有，仅 LiBwrt |
| 加速 | PPE NSS WiFi（kmod-nss-wifi-drv + wpad-openssl） | PPE fork 自带 | 后台，无菜单 | PURE 与 PLUS 都有，仅 PPE 路线（雅典娜） |

- **iStore 注意**：`luci-app-store` 只在 ImmortalWrt / LiBwrt 的 plus 配置里选中，
  只有这两条路线的插件版固件预装 iStore。`ppe-immwrt` 虽然也加了 istore feed
  （`scripts/diy-part1.sh` 里 `immortalwrt|libwrt|ppe-immwrt` 都加），
  但生成器没有给它写 `luci-app-store` 这一行，固件里不含 iStore，
  刷完以后可以自己从 istore feed 安装；官方 OpenWrt 与 `ppe` 既无 feed
  也不写这一行。之前文档里“ImmortalWrt 系都含 iStore”的说法不准确，已按
  实际情况改过来了。
- **PPE 的 SQM**：`luci-app-sqm` 在 5 个源码的 plus 版里都有；`qca-ppe-qos`、
  `sqm-scripts`、`tc-tiny` 与 `kmod-sched-*` 只在 PPE 路线的 plus 版里。
  PPE plus 配置里 `luci-app-sqm=y` 写了两次（生成器里基础段与 PPE 追加段各写了一次），
  无害，构建时只算一次。
- **未编入的**：PassWall v1（未采用，只编 PassWall2）；`luci-app-qca-ppe-qos`
  （需要 PPE 作者的 luci fork，默认 feeds 下 `make defconfig` 会丢掉，配置里明确不写）；
  `ath11k-firmware-qcn9074-ddwrt`（与默认的 `ath11k-firmware-qcn9074` 文件冲突，
  见「待实机验证」）。

### PLUS 版使用提示

- **AdGuard Home 首次启用**：出厂默认关闭。启用服务后访问 `http://路由器IP:3000` 完成安装向导，向导中 **DNS 监听端口请填 `5553`**（`53` 已被系统 dnsmasq 占用，填 53 会报错）；完成后在 LuCI「网络 → DHCP/DNS」的「DNS 转发」中填入 `127.0.0.1#5553` 并勾选「忽略解析文件」，广告过滤即对全局生效。
- **代理插件二选一**：OpenClash 与 PassWall2 工作机制相同（接管 DNS + 透明代理规则），同时启用会互相抢占，轻则其中一个失效、分流错乱，重则断网，请只启用其中一个，切换前先停用当前插件。
- **Docker 存储去向**：Docker 数据默认写入系统分区，容易撑爆。建议先用磁盘管理把 eMMC 空闲空间或外接 U 盘挂载为独立分区，再在 Docker 设置中把存储路径指向该分区。雅典娜只有 1GB 内存，跑 Docker 很吃紧，优先在太乙（2GB）上用 Docker。
- **PPE 路线的 SQM**：PPE 插件版里的 `qca-ppe-qos` 依赖该 fork 的 feed 补丁才能用；若 SQM 页面报错或丢包，先看 Release 里附的 `Config-*.txt`，再决定是否去掉这一行。

---

## 🛠️ 刷机指南

> [!IMPORTANT]
> ### 刷机前必读
> - **目标分区红线**：插件版体积明显大于纯净版，升级前请核实目标系统分区（`rootfs`）空间足够；原厂 60MB 左右的小分区绝对不能直接刷插件版。
> - **Docker 数据保护**：`sysupgrade` 默认会重置内部 Flash 的 overlay 分区，**保留配置不等于保留整个 overlay**！若 Docker 数据位于内部 overlay，升级前必须完整导出到电脑；若位于独立分区，升级后必须先核验挂载再启动 Docker。
> - **换加速架构要清理旧配置**：若从 NSS 固件换到 PPE 固件（或反过来），升级后需检查并清理失效的加速专用防火墙配置节，配置过度杂乱时建议导出备份后选择不保留配置升级（`sysupgrade -n 固件文件名.bin`）。

> ⚠️ **重要提示：** 以下操作涉及 U-Boot 和分区修改，**请务必先备份重要数据**，谨慎操作！

### 详细教程

- 📖 **[刷机与升级说明 →](docs/FLASHING.md)**（开 SSH / 备份分区 / initramfs + sysupgrade 首刷 / 升级 / 救砖全流程）

### 刷机前必读

1. **备份所有数据**
   - 备份原厂固件与原厂后台配置，留好恢复的路。
   - **备份 ART 分区**：ART（eMMC 分区表里一般是 p15）存着每台机器唯一的 MAC、序列号和 WiFi 校准数据。丢了机器还能用，但不再是出厂那个身份，WiFi 也可能不正常。
   - **别碰 SBL1**：一级引导（p1），刷坏只能上编程器救。
   - **改内存才碰 CDT**：CDT（p10/p11）是内存识别配置，不改内存就不要动，错配不会报错，但运行会随机崩。
2. **验证文件完整性**

   每个 Release 附带 `sha256sums.txt` 校验文件，将其与固件下载到同一目录后执行：

   ```bash
   # Linux / macOS
   sha256sum -c sha256sums.txt
   ```

   ```powershell
   # Windows：计算固件哈希，与 sha256sums.txt 中对应行比对
   certutil -hashfile 固件文件名.bin SHA256
   ```

3. **核对机型**：确认文件名里的机型是 `jdcloud_re-cs-02` 还是 `jdcloud_re-cs-07`，**两个机型的固件不能混刷**。

### 刷机步骤

1. **首次从原厂固件刷入**：选文件名带 `factory` 的文件（只有 LiBwrt 的 Release 有），或按教程走 initramfs + sysupgrade 流程；**不要拿 sysupgrade 当 factory 用**。
2. **已是 OpenWrt / ImmortalWrt 要升级**：选文件名带 `sysupgrade` 的文件；在 LuCI「系统 → 备份 / 升级」里上传，同源码同机型升级可保留配置，换源码或换机型建议不保留配置。
3. **救砖**：能进 U-Boot 就用 TFTP 重新拉 `initramfs-uImage.itb` 启动再 sysupgrade；U-Boot 也坏了用 USB 9008 线刷恢复（需要 9008 工具与原厂还原固件）。

### 常见风险及预防

| 风险 | 症状 | 预防方法 |
|------|------|----------|
| **ART 分区丢失** | MAC / 序列号变化，WiFi 不正常 | 刷机前先备份 ART 分区（p15） |
| **U-Boot 错误** | 设备无法启动 | 使用不死 U-Boot，备份原件 |
| **SBL1 损坏** | 设备无法启动，只能编程器救 | 绝对别碰 SBL1（p1） |
| **分区错误** | 系统无法识别 / 空间不足 | 确认 GPT 分区表正确，插件版先核实 rootfs 空间 |
| **机型刷错** | 无法启动或功能异常 | 核对文件名里的机型，RE-CS-02 与 RE-CS-07 不混刷 |
| **断电** | 刷机中断 | 用 UPS 或稳定电源 |
| **固件损坏** | 开机无响应 | 验证 SHA256 后再刷入 |

### 刷机后核对 NSS / PPE（LiBwrt / ImmortalWrt / PPE）

```bash
dmesg | grep -iE 'nss|ath11k|ppe'
```

配置只证明选项被选中，实际 offload 生效仍需实测。

---

## 📦 产物与 Release 说明格式

每个固件单独一个 Release（见上节 tag 命名规则），每个 Release 的说明按固定模板写：

1. **基本信息** — 版本（PURE / PLUS）、源码与分支、源码提交、编译时间；PPE 路线会标“实验路线”
2. **外部插件来源** — 构建时追加的 feed（openclash / passwall2 / pw_packages / istore / nss）
3. **设备与平台** — 机型、硬件平台 qualcommax/ipq60xx、CPU Qualcomm IPQ6010
4. **固件特性** — 该源码的内核与加速方式
5. **默认登录信息** — 管理地址、主机名、用户名、密码、WiFi 名称与密码（仅雅典娜）
6. **WiFi 推荐设置** — 雅典娜三频信道 / 带宽 / 地区 / 功率 / 加密（仅雅典娜）
7. **下载与刷机说明** — factory 与 sysupgrade 的选用、附件说明
8. **风险提示** — 备份 ART、SBL1 别动、不要拿 sysupgrade 当 factory 用、机型不混刷
9. **插件信息** — 本次构建实际编入的 LuCI 插件与主要组件清单（从构建后的 `.config` 提取），以及内核版本；完整清单见 `Packages-*.txt`，完整配置见 `Config-*.txt`

内核版本是构建时从源码里读出来的，不是写死的。

---

## 🧱 构建机制（PURE / PLUS 如何隔离）

- 两个版本由同一套 `configs/` 区分：纯净版与插件版各有一份 `.config`，插件版在纯净版基础上追加插件选项；**纯净版产物不受插件版任何改动影响**。
- 配置由 `scripts/gen-configs.py` 生成，`validate` 任务会先校验 `configs/` 与生成器输出一致，不一致拒绝构建；改配置先改生成器，再重新生成。
- 构建不裁剪任何 feed：`./scripts/feeds update -a` / `./scripts/feeds install -a`，固件自带的软件仓库是全的。
- 每天 02:00 UTC（北京时间 10:00）自动拉取上游最新代码构建：每次构建都是
  `git clone --depth=1` 拉各源码分支的最新提交，所以“每天跟上游”本身就是
  现有行为，不需要额外操作。
- **上游锁定记录同步回写**：定时构建成功后，`sync-lock` 任务会收集 20 个构建任务
  各自实际用的 `SOURCE_HASH`，写回仓库根目录的 `upstream-lock.txt` 并提交
  （提交信息带 `[skip ci]`；且该文件不在 push 触发的 `paths` 列表里，不会触发
  新的构建，不会死循环）。这样仓库里始终记录着最近一次定时构建对应的上游提交，
  想复现某天的固件时直接按这个提交号 checkout 上游即可。手动触发或 push 触发
  的构建不写回，只同步定时构建的结果。
- 并发控制：`build-v2` 并发组（与 v1 仓库的 `build-main` 互不干扰），`cancel-in-progress: false`，排队的构建会依次执行，不会互相打断。

### 构建状态

- 2026-11-16 凌晨 run #1：**20 个任务里 16 个成功、4 个失败，16 个固件已发布**
  （ImmortalWrt 4 + LiBwrt 4 + 官方 OpenWrt 4 + ppe/re-cs-02 2 + ppe-immwrt/re-cs-07 2，
  共 138 个附件；最新 tag 为旧格式的 `ppe-jdcloud_re-cs-02-pure-26.11.16-00.21` 一类）。
- **4 个失败，全是 PPE 路线**：
  1. `ppe` / 太乙 RE-CS-07 纯净版 + 插件版：在「克隆源码」失败（exit 128）——
     下载缓存先恢复出 `openwrt/dl` 目录，`git clone` 报目录已存在；修复已在本地
     仓库的 `build.yml` 里（克隆前先把 `dl` 移走、克隆完放回），待上传到 GitHub 后重编验证。
  2. `ppe-immwrt` / 雅典娜 RE-CS-02 纯净版 + 插件版：在「编译固件」失败（exit 2）——
     `ath11k-firmware-qcn9074` 与 `ath11k-firmware-qcn9074-ddwrt` 文件冲突，
     两个包都想往同一个位置写固件文件；修法是在 RE-CS-02 的 ppe-immwrt 配置里
     二选一（或看该 fork 默认拉的是哪一个），**这次只记下来，等确认修法再改**。
- 2026-11-16 10:00 CST 的定时构建（run #2）尚未核对。

### 版本与验证建议

- `PURE`：推荐作为日常稳定版，保持轻量配置。
- `PLUS`：插件版会额外集成 OpenClash、PassWall2、Docker / Dockerman、AdGuard Home、DDNS、ttyd、UPnP 等，固件体积和运行资源占用都会明显高于纯净版。
- 手动测试时可在 Actions 里单选源码 / 机型 / 版本触发构建；建议插件版发布前先在 Actions 里确认构建日志无报错。
- PPE 路线先只跑纯净版验证，确认能启动、能上网、PPE 生效后再跑插件版。

---

## 📂 项目结构

```text
OpenWrt-JDCloud-v2/
├── .github/workflows/build.yml   # 20 个固件的云编译流程（矩阵 + Release）
├── configs/                      # 20 个 .config，每源码 × 每机型 × 纯净/插件
├── scripts/
│   ├── gen-configs.py            # 生成 configs/ 的脚本（改配置先改这里）
│   ├── diy-part1.sh              # 追加插件 feed（feeds 更新前）
│   └── diy-part2.sh              # Argon / 点阵屏 / 默认值 / 密码哈希（feeds 更新后）
├── files/etc/uci-defaults/99-ll-defaults   # 首次开机默认设置
├── docs/
│   ├── FLASHING.md               # 刷机与升级说明
│   └── V2-NOTES.md               # v2 改动清单、出处与 PPE 风险
├── SOURCES.md                    # 源码、分支、内核、NSS / PPE、假设清单
├── upstream-lock.txt             # 上游锁定记录（定时构建自动同步回写）
├── build.sh                      # 本地编译入口
└── README.md
```

---

## 🔗 上游源码与依赖

| 源码 | 仓库地址 | 说明 |
|------|----------|------|
| **ImmortalWrt** | [laipeng668/immortalwrt](https://github.com/laipeng668/immortalwrt.git) | 本仓库用的 ImmortalWrt fork（含 NSS 12.5 与雅典娜适配） |
| **LiBwrt** | [LiBwrt/openwrt-6.x](https://github.com/LiBwrt/openwrt-6.x.git) | LiBwrt openwrt-6.x，`25.12-nss` 分支 |
| **官方 OpenWrt** | [openwrt/openwrt](https://github.com/openwrt/openwrt.git) | 官方 OpenWrt，用 `main` 分支（25.12 分支无 jdcloud 机型） |
| **PPE+NSS**（实验） | [JuliusBairaktaris/openwrt-ppe-nss](https://github.com/JuliusBairaktaris/openwrt-ppe-nss.git) | 官方 main 底 + PPE，`ppe-nss` 分支 |
| **PPE ImmortalWrt 版**（实验） | [VIKINGYFY/immortalwrt](https://github.com/VIKINGYFY/immortalwrt.git) | ImmortalWrt 底 + PPE，`owrt` 分支 |

插件 feed 与直拉的包见 [SOURCES.md](SOURCES.md)：OpenClash（vernesong/OpenClash）、PassWall2（OpenWrt-Passwall/openwrt-passwall2）、iStore（linkease/istore）、Argon 主题（jerrykuku/luci-theme-argon）、雅典娜点阵屏（NONGFAH/luci-app-athena-led）、NSS 固件 feed（JuliusBairaktaris/nss-packages，仅 ppe）。

---

## 🚀 自定义编译

### 修改编译配置

改配置先改 `scripts/gen-configs.py`，再重新生成 `configs/`：

```bash
python3 scripts/gen-configs.py
```

直接改 `configs/` 下的 `.config` 会被 `validate` 任务打回。

### 触发编译

- **手动全量编译**：Actions → `构建 OpenWrt-JDCloud-v2 固件` → Run workflow，默认全编 20 个，也可单选源码 / 机型 / 版本。
- **自动触发**：改 `configs/`、`scripts/`、`files/` 或 workflow 后 push，以及每天 02:00 UTC 定时，都会触发构建。
- **本地编译**：`bash build.sh <源码> <机型> <版本>`，例如 `bash build.sh immortalwrt jdcloud_re-cs-02 pure`。首次全编约 1-2 小时，磁盘至少留 30GB。

---

## 📊 固件特性对比

| 特性 | 原厂固件 | 本项目固件 |
|------|---------|----------|
| **OpenWrt 版本** | 不支持 | ✅ Linux 6.12 / 6.18（按源码分支）/ firewall4 |
| **硬件加速** | 原厂闭源方案 | ✅ LiBwrt NSS 11.4 / ImmortalWrt NSS 12.5；官方走原生 flow offload；PPE 路线走 PPE 硬件流表 + NSS WiFi（实验） |
| **自定义插件** | ❌ 不支持 | ✅ 完全支持（Docker / PassWall2 / OpenClash 开箱即用，软件源完整） |
| **定期更新** | ❌ 不定期 | ✅ 每天 02:00 UTC 自动跟进上游 |
| **开源透明** | ❌ 闭源 | ✅ 全开源公开 |

---

## 🔍 待实机验证

- **PPE 在 IPQ60xx 上未经实测**：两条 PPE 路线的作者实测机都是小米 AX3600（IPQ807x），README 明说 IPQ60xx 未经测试；8 个 PPE 固件编出来后，必须先实测（有线速率、WiFi、PPE 是否生效）再决定是否日常使用。
- **ath11k 固件包冲突（ppe-immwrt / 雅典娜，待修）**：run #1 里 ppe-immwrt 的两个雅典娜固件在编译时失败，`ath11k-firmware-qcn9074` 与 `ath11k-firmware-qcn9074-ddwrt` 文件冲突。配置里只写了前者（`CONFIG_PACKAGE_ath11k-firmware-qcn9074=y`），后者是该 fork 构建时另外拉进来的；修法是在 RE-CS-02 的 ppe-immwrt 配置里二选一，**等确认修法再改，本次不改配置**。
- **克隆缓存问题（已修，待上传验证）**：run #1 里 ppe 的两个太乙固件在克隆源码时失败，原因是下载缓存先恢复出 `openwrt/dl` 目录；修复已在本地 `build.yml` 里（克隆前移走 `dl`、克隆完放回），等上传到 GitHub 后重编验证。
- **NSS 是否生效**：LiBwrt 的 `kmod-qca-nss-drv` / `kmod-qca-nss-ecm` 包名若被上游改名，`make defconfig` 会静默丢掉，NSS 可能不生效；请以 Release 里附的 `Config-*.txt` 为准核对，并用 `dmesg | grep -i nss` 实测。
- **ImmortalWrt 测试内核**：`CONFIG_TESTING_KERNEL`（当前 6.18）会随上游更新变化；想要最稳的 6.12 可删掉该行。
- **athena-led**：diy-part2.sh 先按 `main` 拉、失败再按 `master` 拉；若上游改了默认分支名，构建会在这一步报错。
- **sqm-scripts-nss 冲突**：roc 的配置把它设为 `n`，ZqinKing 的 nss 片段设为 `y`，v2 按 ZqinKing 取了 `y`（只在 LiBwrt 里）；首次构建若 SQM 报错，先看 `Config-*.txt` 再决定是否改回 `n`。
- **qca-ppe-qos 依赖 feed 补丁**：PPE 插件版里的 `qca-ppe-qos` 依赖该 fork 的 feed 补丁；若首次构建在这一行丢包或报错，先看 `Config-*.txt`，再决定是否去掉这一行。
- **VIKINGYFY `owrt` 分支**：之前担心该分支可能没有 jdcloud 机型；run #1 里 ppe-immwrt 的两个太乙固件构建成功、雅典娜固件只死在固件包冲突上，说明 `owrt` 分支里两个机型都在，分支选择没问题。
- **WiFi 实测**：雅典娜三频 WiFi 的信道 / 带宽 / 功率组合、5G-1 的 160MHz 是否稳定，需实机核对；PPE 路线的 NSS WiFi 是否生效也需实测。

---

## ⚠️ 免责声明

刷机有风险，操作需谨慎。

本项目固件仅供学习与研究使用，请确认设备型号匹配并提前备份数据。
因刷机造成的设备损坏或数据丢失，作者不承担任何责任。

---

## 许可证

GPL-2.0（见 [LICENSE](LICENSE)）。上游 OpenWrt / ImmortalWrt 源码与各插件
遵循各自的许可证，本仓库的构建脚本与配置按 GPL-2.0 提供。

> 文档风格参考了 [Wearwall/Wall-WRT](https://github.com/Wearwall/Wall-WRT) 与
> [ones20250/Openwrt-AX6600](https://github.com/ones20250/Openwrt-AX6600)，
> 但源码、机型与默认值都是按本仓库的要求重新搭的，不是它们的 fork。
> v2 相对 v1 的增补与出处见 [docs/V2-NOTES.md](docs/V2-NOTES.md)。
