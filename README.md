# OpenWrt-JDCloud-v2 — 京东云雅典娜 / 太乙云编译（v2）

京东云雅典娜 RE-CS-02（AX6600）与太乙 RE-CS-07（ER1）的 OpenWrt / ImmortalWrt 云编译固件。
GitHub Actions 全自动编译，五个源码、两个机型、纯净版与插件版，一共 20 个固件。

> 仓库地址：`https://github.com/hhliulei/OpenWrt-JDCloud-v2`
> 本仓库是 v1（[OpenWrt-JDCloud](https://github.com/hhliulei/OpenWrt-JDCloud)，12 个固件）的
> v2：12 个配置按参考仓库做了有据可查的增补，并新增两条 PPE 路线（8 个固件）。
> 改动清单与出处见 [docs/V2-NOTES.md](docs/V2-NOTES.md)。
> 文档风格参考了 Wearwall/Wall-WRT 与 ones20250/Openwrt-AX6600，
> 但源码、机型与默认值都是按本仓库的要求重新搭的，不是它们的 fork。

> ⚠️ **PPE 路线属实验性质**：`ppe` 与 `ppe-immwrt` 两条路线的 PPE 在 IPQ60xx 上
> 未经源码作者实测（作者实测机为小米 AX3600 / IPQ807x），编出来后请先实测
> （有线速率、WiFi、PPE 是否生效）再决定是否日常使用。

## 源码 / 分支 / 内核 / NSS / WiFi 对照表

| 源码 | 上游仓库 | 分支 | 内核 | NSS / PPE | WiFi |
| --- | --- | --- | --- | --- | --- |
| ImmortalWrt | `laipeng668/immortalwrt.git` | `openwrt-25.12` | 测试内核（当前 6.18） | NSS 12.5 | 雅典娜：正常 ath11k；太乙：无 |
| LiBwrt | `LiBwrt/openwrt-6.x.git` | `25.12-nss` | 6.12 | NSS 11.4 | 雅典娜：WiFi offload 开；太乙：无 |
| 官方 OpenWrt | `openwrt/openwrt.git` | `main`（快照，25.12 分支无 jdcloud 机型） | 跟 main 默认内核（当前 6.18） | 无（上游不含 NSS） | 雅典娜：正常 ath11k；太乙：无 |
| PPE+NSS（实验） | `JuliusBairaktaris/openwrt-ppe-nss.git` | `ppe-nss` | 6.18 | PPE（qca_ppe/edma）+ NSS WiFi | 雅典娜：NSS WiFi offload；太乙：无 |
| PPE ImmortalWrt 版（实验） | `VIKINGYFY/immortalwrt.git` | `owrt` | 该分支默认 | PPE（满血）+ NSS WiFi | 雅典娜：NSS WiFi offload；太乙：无 |

内核不写死版本号：用各分支的默认内核，构建时以 Release 里附的
`upstream-lock.txt` 为准。详细说明与假设清单见 [SOURCES.md](SOURCES.md)。

## 固件矩阵（20 个）

| 源码 | 雅典娜 RE-CS-02 | 太乙 RE-CS-07 |
| --- | --- | --- |
| ImmortalWrt | 纯净版 / 插件版 | 纯净版 / 插件版 |
| LiBwrt openwrt-6.x | 纯净版 / 插件版 | 纯净版 / 插件版 |
| 官方 OpenWrt | 纯净版 / 插件版 | 纯净版 / 插件版 |
| PPE+NSS（实验） | 纯净版 / 插件版 | 纯净版 / 插件版 |
| PPE ImmortalWrt 版（实验） | 纯净版 / 插件版 | 纯净版 / 插件版 |

- 雅典娜：京东云无线宝 AX6600，三频 WiFi 6 + 顶部点阵屏，`jdcloud_re-cs-02`。
- 太乙：京东云 ER1 有线路由，无 WiFi（NoWiFi），`jdcloud_re-cs-07`。
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

WiFi 推荐设置（雅典娜三频）：2.4G 信道 11 / 20MHz，5G-1 信道 44 / 160MHz
（起不来或断流就降到 80MHz），5G-2 信道 149 / 80MHz，地区 US，发射功率 24 dBm，
加密 WPA2-PSK。首次使用后请在 LuCI 里改掉 WiFi 密码。

## 纯净版与插件版

| 版本 | 适合人群 | 预置内容 |
| --- | --- | --- |
| PURE 纯净版 | 希望系统轻量、稳定，按需自行安装插件的用户 | 完整网络功能 + LuCI + 常用管理插件（防火墙、软件包管理、ARP 绑定、自动重启、Samba4、uHTTPd 等），不过度精简 |
| PLUS 插件版 | 希望刷完即用常见扩展服务的用户 | 在纯净版基础上增加 OpenClash、PassWall2、Docker / Dockerman、AdGuard Home、SmartDNS、MosDNS、DDNS、ttyd 终端、UPnP、磁盘管理、网络唤醒、看门狗、iStore（仅 ImmortalWrt 系）、Aria2、OpenList2、FRP、ACME、EasyTier、Lucky 等实用插件；PPE 路线另加 PPE 塑形 SQM（qca-ppe-qos）与 tc 调度模块 |

v2 相对 v1 的增补（NSS 性能开关、Docker 依赖补齐、MosDNS / Aria2 / OpenList2 /
FRP / ACME / EasyTier / Lucky 等插件、磁盘与诊断工具、zram 后端、WireGuard、
eMMC 健康监测）与每条改动的出处，见 [docs/V2-NOTES.md](docs/V2-NOTES.md)。
一个已知冲突：`sqm-scripts-nss` 在 ZqinKing 的 jdcloud 片段里是开、在 roc 里是关，
v2 按 ZqinKing 取了开，首次构建若 SQM 报错再看 `Config-*.txt` 决定是否改回关。

两个版本的区别只在预装插件：**软件仓库都是全的**。纯净版刷完以后，
想装什么插件都可以自己在 LuCI「软件包」里装，不是不给装。
Release 文件名里带 `pure` 或 `plus`，请按需求下载对应版本。

## 插件矩阵

| 分类 | 插件 | 来源 | 菜单位置 | 状态 |
| --- | --- | --- | --- | --- |
| 容器 | Docker（dockerd / docker / docker-compose） | 官方 / ImmortalWrt feed | 服务 → Docker | 仅 PLUS |
| 容器 | Dockerman（luci-app-dockerman） | 官方 / ImmortalWrt feed | 服务 → Docker | 仅 PLUS |
| 代理 | OpenClash | OpenClash feed | 服务 → OpenClash | 仅 PLUS |
| 代理 | PassWall2 | PassWall2 feed | 服务 → PassWall2 | 仅 PLUS |
| DNS | AdGuard Home | 官方 / ImmortalWrt feed | 服务 → AdGuard Home | 仅 PLUS |
| DNS | SmartDNS | 官方 / ImmortalWrt feed | 服务 → SmartDNS | 仅 PLUS |
| DNS | MosDNS | 官方 / ImmortalWrt feed | 服务 → MosDNS | 仅 PLUS |
| 网络 | DDNS | 官方 / ImmortalWrt feed | 服务 → 动态 DNS | 仅 PLUS |
| 网络 | UPnP | 官方 / ImmortalWrt feed | 服务 → UPnP | 仅 PLUS |
| 管理 | ttyd 终端 | 官方 / ImmortalWrt feed | 服务 → 终端 | 仅 PLUS |
| 管理 | 磁盘管理（diskman） | 官方 / ImmortalWrt feed | 系统 → 磁盘管理 | 仅 PLUS |
| 管理 | 网络唤醒（wol） | 官方 / ImmortalWrt feed | 服务 → 网络唤醒 | 仅 PLUS |
| 管理 | 看门狗（watchcat） | 官方 / ImmortalWrt feed | 服务 → 看门狗 | 仅 PLUS |
| 管理 | 文件管理（quickfile） | 官方 / ImmortalWrt feed | 服务 → 文件管理 | 仅 PLUS |
| 管理 | KMS（vlmcsd） | 官方 / ImmortalWrt feed | 服务 → KMS | 仅 PLUS |
| 下载 | Aria2 + Ariang | 官方 / ImmortalWrt feed | 服务 → Aria2 | 仅 PLUS |
| 下载 | OpenList2 | 官方 / ImmortalWrt feed | 服务 → OpenList2 | 仅 PLUS |
| 远程 | FRP（frps / frpc） | 官方 / ImmortalWrt feed | 服务 → FRP | 仅 PLUS |
| 远程 | ACME 证书 | 官方 / ImmortalWrt feed | 服务 → ACME | 仅 PLUS |
| 组网 | EasyTier | 官方 / ImmortalWrt feed | 服务 → EasyTier | 仅 PLUS |
| 组网 | Lucky | 官方 / ImmortalWrt feed | 服务 → Lucky | 仅 PLUS |
| 分流 | PBR 策略路由 | 官方 / ImmortalWrt feed | 网络 → PBR | 仅 PLUS |
| 分流 | netwiz | 官方 / ImmortalWrt feed | 网络 → netwiz | 仅 PLUS |
| 塑形 | SQM（luci-app-sqm） | 官方 / ImmortalWrt feed | 网络 → SQM | 仅 PLUS |
| PPE | PPE 塑形 SQM（qca-ppe-qos）+ tc 调度模块 | PPE fork 自带 | 网络 → SQM | 仅 PLUS，且仅 PPE 路线 |
| 商店 | iStore（luci-app-store） | iStore feed | 服务 → 应用商店 | 仅 PLUS，且仅 ImmortalWrt 系（immortalwrt / libwrt / ppe-immwrt） |
| 基础 | 防火墙 / 软件包管理 / ARP 绑定 / 自动重启 | 官方 / ImmortalWrt feed | 系统 / 网络 | PURE 与 PLUS 都有 |
| 基础 | Samba4 文件共享 | 官方 / ImmortalWrt feed | 服务 → 网络共享 | PURE 与 PLUS 都有 |
| 雅典娜 | 点阵屏（luci-app-athena-led） | NONGFAH/luci-app-athena-led | 系统 → 点阵屏 | PURE 与 PLUS 都有，仅雅典娜 |
| 主题 | Argon + Argon 配置 | jerrykuku/luci-theme-argon | 系统 → 主题 | PURE 与 PLUS 都有 |

## 下载固件

| 版本 | 下载入口 | 适合场景 |
| --- | --- | --- |
| 🍃 `PURE` 纯净版 | 到 Releases 页面按 tag 找对应版本 | 轻量稳定，日常推荐，插件按需自装 |
| 🚀 `PLUS` 插件版 | 到 Releases 页面按 tag 找对应版本 | OpenClash / PassWall2 / Docker / AdGuard Home 开箱即用 |

Release 的 tag 形如 `immortalwrt-jdcloud_re-cs-02-pure-26.11.15-1830`，
即 `<源码>-<机型>-<版本>-<编译时间>`。打开列表最上方即为该版本最新固件，
也可浏览全部 Releases。

每个 Release 里包含以下文件：

- `*squashfs-sysupgrade-*.bin`：已是 OpenWrt / ImmortalWrt 时升级用
- `*squashfs-factory-*.bin`：首次从原厂固件刷入用（只有 LiBwrt 的 Release 有）
- `*.manifest`：固件包含的软件包清单
- `Config-*.txt`：本次编译的完整 `.config` 配置，便于复现或二次定制
- `Packages-*.txt`：本次编译选中的软件包清单
- `sha256sums.txt`：固件校验文件，刷机前先校验下载完整性
- `upstream-lock.txt`：本次构建实际用的源码提交号与追加 feed 列表

## 刷机与升级

完整教程见 [docs/FLASHING.md](docs/FLASHING.md)。要点：

- 首次从原厂固件刷入：选文件名带 `factory` 的文件（LiBwrt），
  或按教程走 initramfs + sysupgrade 流程；不要拿 sysupgrade 当 factory 用。
- 已是 OpenWrt / ImmortalWrt 要升级：选文件名带 `sysupgrade` 的文件；
  同源码同机型升级可保留配置，换源码或换机型建议不保留配置。
- 刷机前先用 `sha256sums.txt` 校验，再确认文件名里的机型是
  `jdcloud_re-cs-02` 还是 `jdcloud_re-cs-07`，两个机型的固件不能混刷。

## Release 说明格式

每个 Release 的说明里都会写清楚：源码与分支、机型、版本（PURE / PLUS）、
内核版本、编译时间、默认登录信息、内置插件、下载与刷机说明。
内核版本是构建时从源码里读出来的，不是写死的。

## ⚠️ 风险提示

刷机存在风险，请确认：

- 已备份原厂固件
- 已备份 ART 分区（每台机器唯一的 MAC / 序列号 / WiFi 校准数据）
- 能进入 U-Boot 或 TTL 恢复
- 了解分区结构，SBL1 绝对别动，不改内存就别碰 CDT

## 自己触发编译

- 手动：在仓库 Actions 页面打开「构建 OpenWrt-JDCloud-v2 固件」，
  点 Run workflow，可单选源码 / 机型 / 版本（默认全编 20 个）。
- 自动：改 `configs/`、`scripts/`、`files/` 或 workflow 后 push，
  以及每天 02:00 UTC 定时，都会触发构建。
- 本地：`bash build.sh <源码> <机型> <版本>`，
  例如 `bash build.sh immortalwrt jdcloud_re-cs-02 pure`。
  首次全编约 1-2 小时，磁盘至少留 30GB。

## 仓库结构

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
├── upstream-lock.txt             # 上游锁定记录模板（Release 里附构建时生成的版本）
├── build.sh                      # 本地编译入口
└── README.md
```

## 许可证

GPL-2.0（见 [LICENSE](LICENSE)）。上游 OpenWrt / ImmortalWrt 源码与各插件
遵循各自的许可证，本仓库的构建脚本与配置按 GPL-2.0 提供。
