# 源码与分支说明（SOURCES.md）

本仓库不 fork 上游源码：每次构建由 workflow 按下表实时克隆上游仓库，
内核用各分支的默认版本，不写死版本号。分支与内核版本是 2026-11-15
实测核对过的（`git ls-remote` + 稀疏克隆读 `target/linux/qualcommax/Makefile`）。

## 源码对照表

| 源码（本仓库代号） | 上游仓库 | 分支 | 内核（该分支默认） | NSS / PPE | WiFi |
| --- | --- | --- | --- | --- | --- |
| ImmortalWrt（`immortalwrt`） | `laipeng668/immortalwrt.git` | `openwrt-25.12` | 6.12，构建时开 `CONFIG_TESTING_KERNEL` 用测试内核（当前为 6.18） | NSS 12.5 | 雅典娜：正常 ath11k（12.5 不提供 WiFi offload）；太乙：无 |
| LiBwrt（`libwrt`） | `LiBwrt/openwrt-6.x.git` | `25.12-nss`（该仓库唯一分支） | 6.12 | NSS 11.4 | 雅典娜：`ATH11K_NSS_SUPPORT` 开（WiFi offload）；太乙：无 |
| 官方 OpenWrt（`openwrt`） | `openwrt/openwrt.git` | `main`（快照） | 跟 main 的默认内核（当前 6.18） | 无（上游不含 NSS 闭源加速） | 雅典娜：正常 ath11k；太乙：无 |
| PPE+NSS（`ppe`，实验） | `JuliusBairaktaris/openwrt-ppe-nss.git` | `ppe-nss` | 6.18 | PPE（上游 qca_ppe / qca_edma 硬件流表）+ NSS WiFi（nss-wifi-drv + ath11k），不用 ECM、不走厂商 NSS 驱动 | 雅典娜：`ATH11K_NSS_WIFI` 开（NSS WiFi offload）；太乙：无 |
| PPE ImmortalWrt 版（`ppe-immwrt`，实验） | `VIKINGYFY/immortalwrt.git` | `owrt` | 该分支默认 | PPE（满血，代码取自 JuliusBairaktaris 等项目）+ NSS WiFi | 雅典娜：NSS WiFi offload；太乙：无 |

说明：
- ImmortalWrt 用 `laipeng668/immortalwrt` 这个 fork 而不用官方 `immortalwrt/immortalwrt`，
  因为 Wall-WRT / laipeng668/openwrt-ci-roc 都是用它做雅典娜适配（含 NSS 12.5 与
  Athena 相关补丁）；官方 ImmortalWrt 同样有 `openwrt-25.12` 分支，可随时换回。
- LiBwrt 的 `25.12-nss` 是 `LiBwrt/openwrt-6.x` 的唯一分支，`laipeng668/openwrt-6.x`
  是同一份代码的镜像（2026-11-15 核对过 HEAD 一致）。
- 官方 OpenWrt 只能用 `main` 分支：`openwrt-25.12` 分支的
  `target/linux/qualcommax/image/ipq60xx.mk` 里根本没有 jdcloud 这两个机型
  （2026-11-15 核对，25.12.3 发布镜像里也没有 jdcloud 固件）；
  jdcloud 支持 2026-01 才合进 main。main 是快照分支，内核与软件包都跟最新，
  这是官方那 4 个固件唯一可行的分支。

## 机型对照表

| 机型 | 设备名（.config / 上游 Device） | SoC | WiFi | 备注 |
| --- | --- | --- | --- | --- |
| 雅典娜 | `jdcloud_re-cs-02` | IPQ6010 | 三频 WiFi 6：2.4G + 5G-1 + 5G-2，ath11k + QCN9074 固件 + `ipq-wifi-jdcloud_re-cs-02` 校准数据 | 顶部点阵屏用 `luci-app-athena-led`（diy-part2.sh 从 NONGFAH 拉取） |
| 太乙 | `jdcloud_re-cs-07` | IPQ6010 | 无（NoWiFi） | 上游 Device 定义本身就排除了 ath11k / wpad；本仓库配置里再明确关掉 |

两个机型在 ImmortalWrt / LiBwrt / 官方 main 的 `target/linux/qualcommax/image/ipq60xx.mk` 里都有
`define Device/jdcloud_re-cs-02` / `define Device/jdcloud_re-cs-07`，
`KERNEL_SIZE := 6144k`，`FitImage` 格式；LiBwrt 里还多一个 `EmmcImage`，
所以 LiBwrt 的构建会额外产出 `factory.bin`。注意：官方 `openwrt-25.12` 分支里没有这两个机型，
所以官方源码用 `main` 分支（见上表）。PPE 路线也已核对：JuliusBairaktaris 的 `ppe-nss` 分支
`ipq60xx.mk` 里 `jdcloud_re-cs-02`（第 201 行）、`jdcloud_re-cs-07`（第 224 行）都在，
定义与官方 main 一致；VIKINGYFY 的 `owrt` 分支是否包含这两个机型，首次构建时需核对
（ZqinKing 的 jdcloud immwrt 用的是 VIKINGYFY 的 `main` 分支，不是 `owrt`）。

## 追加的插件 feed（scripts/diy-part1.sh）

| feed | 地址 | 用途 |
| --- | --- | --- |
| `openclash` | `vernesong/OpenClash.git` | OpenClash |
| `passwall2` | `Openwrt-Passwall/openwrt-passwall2.git` | PassWall2 |
| `pw_packages` | `Openwrt-Passwall/openwrt-passwall-packages.git` | PassWall2 依赖包 |
| `istore` | `linkease/istore.git` | iStore 应用商店（只加 ImmortalWrt 系：immortalwrt / libwrt / ppe-immwrt，官方 OpenWrt 与 ppe 不加） |
| `nss` | `JuliusBairaktaris/nss-packages.git;ppe-nss` | NSS 固件（只加 ppe 源码；该 feed 里只取 `nss-firmware` 一个包，kmod-nss-wifi-drv 需要它） |

另外两个不在 feed 里的包由 diy-part2.sh 直接 clone：
- Argon 主题与配置插件：`jerrykuku/luci-theme-argon`、`jerrykuku/luci-app-argon-config`
  （master 分支，放到 `feeds/luci/themes|applications` 下面）。
- 雅典娜点阵屏：`NONGFAH/luci-app-athena-led`（放到 `package/` 下面，只在雅典娜构建时拉）。

## 软件源为什么是“全的”

workflow 里跑的是 `./scripts/feeds update -a` / `./scripts/feeds install -a`，
不裁剪任何默认 feed，也不删追加的 feed。固件自带的软件仓库（`/etc/opkg/distfeeds.conf`
或 apk 仓库配置）因此包含全部 feed，刷完以后任何插件都能自己装。
纯净版只是“没预装”扩展插件，不是“装不上”。

## 假设与不确定点（首次构建前请核对）

1. **机型符号（2026-11-15 已踩坑并修复）**：机型必须用 Target Profile choice 的符号
   `CONFIG_TARGET_qualcommax_ipq60xx_DEVICE_jdcloud_re-cs-02=y`（没有 `TARGET_DEVICE_` 这一段）。
   之前写的是 `CONFIG_TARGET_DEVICE_qualcommax_ipq60xx_DEVICE_...=y`，那是多机型
   （`MULTI_PROFILE`）菜单里的布尔项；不开 `MULTI_PROFILE` 时它在 Kconfig 里不可见，
   `make defconfig` 会悄悄丢掉这一行，choice 就默认选中首个机型（`8devices_mango-dvk`），
   导致 2026-11-15 的 #3/#4 全部在 defconfig 校验失败。本仓库已在本地用
   ImmortalWrt（`openwrt-25.12`）和官方 OpenWrt（`main`）的源码实测验证：改对符号后
   defconfig 保留机型行，`CONFIG_TARGET_PROFILE="DEVICE_jdcloud_re-cs-02"`。
   另注意 `CONFIG_TARGET_PER_DEVICE_ROOTFS=y` 同样只在 `MULTI_PROFILE` 菜单里才可见，
   单机型构建不需要它，配置里已去掉。
2. **NSS 驱动包名**：LiBwrt 配置里写了 `kmod-qca-nss-drv` / `kmod-qca-nss-ecm`。
   如果该分支里包名有变，`make defconfig` 会静默丢掉这一行，NSS 加速可能不生效，
   请以首次构建的 `Config-*.txt` 为准核对（Release 里自带）。
3. **ImmortalWrt 测试内核**：`CONFIG_TESTING_KERNEL=y` 会让 ImmortalWrt 用测试内核
   （当前 6.18）。测试内核可能随上游更新而变化；如果想要最稳的 6.12，
   把 `configs/immortalwrt-*.config` 里的 `CONFIG_TESTING_KERNEL=y` 删掉。
4. **athena-led 默认分支**：diy-part2.sh 先按 `main` 拉，失败再按 `master` 拉；
   如果 NONGFAH 的仓库改了默认分支名，两次都会失败，构建会在这一步报错，
   按报错信息改分支名即可。
5. **iStore 与官方 OpenWrt / PPE**：`luci-app-store` 只在 ImmortalWrt 系
   （immortalwrt / libwrt / ppe-immwrt）的 plus 版里生效；官方 OpenWrt 与 ppe
   的 plus 版没有 istore feed，配置里直接不写这一行。
6. **Docker 与雅典娜 1GB 内存**：雅典娜出厂只有 1GB 内存，跑 Docker 很吃紧，
   建议优先在太乙（2GB）上用 Docker，或给雅典娜扩内存后再用。
7. **factory.bin**：LiBwrt 的 Device 定义带 `EmmcImage`，会产出 `factory.bin`；
   ImmortalWrt / 官方 OpenWrt 的 Device 定义目前只有 `FitImage`，
   首次刷机请按 docs/FLASHING.md 用 initramfs + sysupgrade 的流程，
   不要拿 sysupgrade 当 factory 用。
8. **PPE 路线未经 IPQ60xx 实测**：JuliusBairaktaris 的作者实测机是小米 AX3600
   （IPQ807x），README 明说“IPQ60xx is not tested at all”；VIKINGYFY 的 PPE
   也未点名在京东云上测过。8 个 PPE 配置编出来后，必须先实测（有线速率、WiFi、
   PPE 是否生效）再决定是否采用，Release 说明里已标“实验路线”。
9. **VIKINGYFY 分支出入**：ZqinKing 的 jdcloud immwrt 用的是 VIKINGYFY 的 `main` 分支，
   而本仓库 `ppe-immwrt` 用的是 README 点名的 PPE 分支 `owrt`。首次构建时需核对
   `owrt` 分支是否包含 jdcloud 机型与 PPE 代码；若缺机型，改回 `main` 分支或换源码。
10. **qca-ppe-qos 依赖 feed 补丁**：PPE 插件版里的 `qca-ppe-qos` 依赖该 fork 的
    feed 补丁（seed 注释：PPE QoS 需要“sqm-scripts from the builder's feed patch”）。
    若首次构建在这一行丢包或报错，先看 `Config-*.txt`，再决定是否去掉这一行。
    `luci-app-qca-ppe-qos` 需要作者的 luci fork，默认 feeds 下 defconfig 会丢掉，
    配置里已明确不写。
11. **sqm-scripts-nss 冲突**：roc 的 `General.config` 把它设为 `n`，ZqinKing 的
    nss 片段（jdcloud_ipq60xx 专用）设为 `y`。v2 按 ZqinKing 取 `y`；首次构建若
    SQM 相关报错，先查 `Config-*.txt` 再决定是否改回 `n`。
