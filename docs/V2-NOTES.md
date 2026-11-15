# OpenWrt-JDCloud-v2 配置说明（v2 配置集）

> 状态：本仓库（OpenWrt-JDCloud-v2）的 `configs/` 就是这份 v2 配置集，
> 已接入 `.github/workflows/build.yml`（20 个任务矩阵）。v1 仓库（12 个固件）不受影响。

生成器：`scripts/gen-configs.py`（重新跑一遍应无变化，幂等）。

## 文件一览（20 个）

| 源码 | 仓库 / 分支 | 机型 × 版本 | 文件前缀 |
| --- | --- | --- | --- |
| ImmortalWrt | `laipeng668/immortalwrt.git` / `openwrt-25.12` | RE-CS-02 / RE-CS-07 × pure / plus | `immortalwrt-*.config`（4 个） |
| LiBwrt | `LiBwrt/openwrt-6.x.git` / `25.12-nss` | 同上 | `libwrt-*.config`（4 个） |
| 官方 OpenWrt | `openwrt/openwrt.git` / `main` | 同上 | `openwrt-*.config`（4 个） |
| PPE+NSS（实验） | `JuliusBairaktaris/openwrt-ppe-nss.git` / `ppe-nss` | 同上 | `ppe-*.config`（4 个） |
| PPE+NSS ImmortalWrt 版（实验） | `VIKINGYFY/immortalwrt.git` / `owrt` | 同上 | `ppe-immwrt-*.config`（4 个） |

默认设置与 v1 完全一致：LAN 192.168.10.1、主机名 ll、root/root、Argon 主题、简体中文、
软件源不裁剪（构建时 feeds 全量拉取）。纯净版 = 稳定、不精简；插件版 = 纯净版 + 主流插件。

## v2 相对 v1 改了什么（每条都有出处）

### 所有 12 个 v2 配置共有的增补

| 改动 | 出处 |
| --- | --- |
| `CONFIG_PACKAGE_default-settings=y`、`CONFIG_PACKAGE_default-settings-chn=y`（显式写明） | roc `configs/General.config`；ZqinKing `compile_base.config` |
| zram 内核后端：`CONFIG_KERNEL_ZRAM_BACKEND_LZ4=y`、`CONFIG_KERNEL_ZRAM_BACKEND_LZO=y`、`CONFIG_KERNEL_ZRAM_DEF_COMP_LZ4=y` | roc `General.config` |
| 磁盘/分区工具：`fdisk`、`cfdisk`、`sgdisk`、`hdparm`、`smartmontools-drivedb`、`fstrim`、`tune2fs` | roc `General.config`；ZqinKing deconfig |
| 文件系统/存储：`kmod-fs-exfat`、`ntfs3-mount`、`kmod-usb-storage-extras`、`kmod-usb-storage-uas`、`kmod-usb2`、`usbutils` | ZqinKing jdcloud deconfig |
| 终端/诊断工具：`tmux`、`dmesg`、`btop`、`coremark`、`tcpdump`、`qrencode`、`openssl-util`、`libopenssl-legacy`、`luci-lib-ipkg` | roc `General.config`；ZqinKing `compile_base.config` |
| `nano` → `nano-full` | roc `General.config` |
| 内核诊断模块：`kmod-netlink-diag`、`kmod-inet-diag`、`kmod-tls` | ZqinKing deconfig |
| 链路聚合与 nft 兼容层：`proto-bonding`、`iptables-nft`、`ip6tables-nft` | ZqinKing `compile_base.config` |
| `luci-proto-wireguard=y`（WireGuard 协议支持） | roc `General.config`；ZqinKing `compile_base.config` |
| `luci-app-emmc-health=y`（eMMC 健康监测；官方 OpenWrt 下若 feeds 里没有，defconfig 会自动丢掉，不影响构建） | ZqinKing jdcloud deconfig |

### ImmortalWrt（NSS 12.5）

- 底子不变：`CONFIG_TESTING_KERNEL=y`、`CONFIG_NSS_FIRMWARE_VERSION_12_5=y`、
  `CONFIG_ATH11K_MEM_PROFILE_512M=y`（与 roc `JDCloud.config` 一致）。
- 新增 NSS 通用性能开关（ZqinKing `fragments/nss.config`，不含 11.4 专属的 drv 扩展包）：
  `CONFIG_IPQ_MEM_PROFILE_256=y`、`CONFIG_NSS_MEM_PROFILE_HIGH=y`、
  `CONFIG_PACKAGE_kmod-qca-mcs=y`、`CONFIG_KERNEL_SKB_RECYCLER=y`、
  `CONFIG_KERNEL_SKB_RECYCLER_MULTI_CPU=y`。
- 12.5 仍不提供 WiFi offload：`ATH11K_NSS_SUPPORT` / `ATH11K_NSS_MESH_SUPPORT` 继续明确关掉。

### LiBwrt（NSS 11.4）

- 底子不变：`CONFIG_NSS_FIRMWARE_VERSION_11_4=y`、`kmod-qca-nss-drv`、`kmod-qca-nss-ecm`、
  雅典娜开 `ATH11K_NSS_SUPPORT` / `ATH11K_NSS_MESH_SUPPORT`。
- 新增 ZqinKing `fragments/nss.config` 片段（该片段明确用于 jdcloud_ipq60xx 设备）：
  `CONFIG_IPQ_MEM_PROFILE_256=y`、`CONFIG_NSS_MEM_PROFILE_HIGH=y`、
  `CONFIG_PACKAGE_sqm-scripts-nss=y`、`CONFIG_PACKAGE_kmod-qca-mcs=y`、
  `CONFIG_KERNEL_SKB_RECYCLER=y`、`CONFIG_KERNEL_SKB_RECYCLER_MULTI_CPU=y`、
  `CONFIG_PACKAGE_kmod-qca-nss-drv-igs=y`、`kmod-qca-nss-drv-l2tpv2=y`、
  `kmod-qca-nss-drv-lag-mgr=y`、`kmod-qca-nss-drv-pppoe=y`、`kmod-qca-nss-drv-pptp=y`，
  以及雅典娜的 `CONFIG_NSS_DRV_WIFI_MESH_ENABLE=y`、`CONFIG_PACKAGE_MAC80211_MESH=y`。
- 注意一个参考冲突：roc `General.config` 把 `CONFIG_PACKAGE_sqm-scripts-nss` 显式设为 `n`，
  而 ZqinKing 的 nss 片段设为 `y`。v2 按 ZqinKing（jdcloud 专用片段）取 `y`；
  首次构建若 SQM 相关报错，先查 `Config-*.txt` 再决定是否改回 `n`。
- `kmod-ath11k-pci` 保持 `=y`（ZqinKing 片段写的是 `=m`，差异已记录，v1 的 `=y` 不变）。

### 官方 OpenWrt

- 仍用 `main` 分支（`openwrt-25.12` 里没有 jdcloud 机型），无 NSS 开关。
- 只享受上文“所有配置共有”的增补。

### 插件版（plus）共有的增补

| 改动 | 出处 |
| --- | --- |
| Docker 运行时依赖补齐（nftables 后端，Docker v29）：`fuse-overlayfs`、`kmod-fs-btrfs`、`kmod-crypto-acompress/blake2b/xxhash`、`kmod-lib-lzo/raid6/xor/xxhash/zlib-deflate/zlib-inflate/zstd`、`kmod-ipt-nat/nat6/physdev`、`kmod-nf-ipvs`、`kmod-nf-nat6`、`kmod-dummy`、`iptables-mod-extra`、`nftables`、`kmod-nft-nat`、`kmod-nft-netdev` | ZqinKing `fragments/docker_deps.config` |
| DNS 再加 MosDNS：`mosdns`、`luci-app-mosdns` | ZqinKing `compile_base.config` |
| `luci-app-sqm=y`（SQM 界面） | ZqinKing deconfig |
| 文件管理与 KMS：`luci-app-quickfile`、`luci-app-vlmcsd` | ZqinKing deconfig；roc `General.config` |
| 下载与远程：`ariang`、`luci-app-aria2`（含 `CONFIG_ARIA2_OPENSSL/EXPAT/BITTORRENT/METALINK/SFTP/ASYNC_DNS/WEBSOCKET=y`）、`luci-app-openlist2`、`luci-app-frps`、`luci-app-frpc`、`luci-app-acme`、`acme-acmesh-dnsapi` | roc `JDCloud.config` / `General.config` |
| 组网与分流：`easytier`、`luci-app-easytier`（`CONFIG_EASYTIER_INCLUDE_WEBCONSOLE=n`）、`luci-app-lucky`、`luci-app-pbr`、`luci-app-netwiz` + `luci-i18n-netwiz-zh-cn` | ZqinKing `compile_base.config` |
| Web 与日志：`nginx-full`、`logrotate` | roc `JDCloud.config` |
| DDNS 再加 Cloudflare：`ddns-scripts-cloudflare` | roc `General.config` |
| iStore 只保留在 ImmortalWrt / LiBwrt 的 plus 里；官方 OpenWrt 与 PPE 路线没有 istore feed，v2 里直接不写 `luci-app-store`（v1 是写了靠 defconfig 丢，v2 改为明示不写） | 与 v1 注释一致，做法更干净 |

## PPE 路线（8 个配置，实验性质）

两条 PPE 路线共用同一套开关，区别只在源码底子：

| | `ppe` | `ppe-immwrt` |
| --- | --- | --- |
| 源码 | `JuliusBairaktaris/openwrt-ppe-nss.git` / `ppe-nss` | `VIKINGYFY/immortalwrt.git` / `owrt` |
| 底子 | 官方 OpenWrt main | ImmortalWrt（README 点名 owrt 分支带满血 PPE） |
| 内核 | 6.18（该分支默认） | 该分支默认（未写死） |

技术路线（JuliusBairaktaris `seeds/qualcommax-nss-wifi.seed`）：
- 以太走上游 `qca_ppe` / `qca_edma`（PPE 硬件流表）。**这不是 Kconfig 开关**，由该 fork 的
  target 代码提供；配置文件里没有也不需要为此写一行。
- WiFi 走 NSS：`CONFIG_PACKAGE_kmod-nss-wifi-drv=y`、`CONFIG_ATH11K_NSS_WIFI=y`，
  雅典娜用 `CONFIG_PACKAGE_wpad-openssl=y`（明确关掉 `wpad-basic-mbedtls`），
  太乙无 WiFi，不写这两行（与上游 RE-CS-07 的 Device 定义一致）。
- 插件版追加 seed 文件的 Optional 部分：`sqm-scripts`、`luci-app-sqm`、`qca-ppe-qos`、
  `tc-tiny`、`kmod-sched-flower/prio/act-police/act-pedit/act-vlan/mqprio/ets/red/gred`、
  `dcb`、`devlink`、`ethtool-full`、`CONFIG_KERNEL_DCB=y`、`CONFIG_KERNEL_IP_MROUTE=y`、
  `CONFIG_KERNEL_IPV6_MROUTE=y`。
- `luci-app-qca-ppe-qos` **明确不写**：seed 文件原话是它需要该作者的 luci fork，
  默认 feeds 下 defconfig 会丢掉。
- 雅典娜的 `luci-app-athena-led` 照写（与 v1 相同，将来接入构建时需由 diy-part2 同类步骤拉取）。

**未验证的风险（首次构建前必读）：**
1. JuliusBairaktaris 的作者实测机是小米 AX3600（IPQ807x），**IPQ60xx 未经实测**；VIKINGYFY
   的 PPE 也未点名在京东云上测过。8 个 PPE 配置编出来后，必须先实测（有线速率、WiFi、
   PPE 是否生效）再决定是否采用。
2. 该作者的 `ipq60xx.mk` 已核对：`jdcloud_re-cs-02`（第 201 行）、`jdcloud_re-cs-07`
   （第 224 行）都在，定义与官方 main 一致（FitImage，DTS config@cp03-c3/c4），
   所以机型符号本身没问题；风险在 PPE/NSS-WiFi 这条加速链路上。
3. `qca-ppe-qos` 依赖该 fork 的 feed 补丁（seed 注释：PPE QoS 需要“sqm-scripts from the
   builder's feed patch”）。若首次构建在这一行丢包或报错，先看 `Config-*.txt`，
   再决定是否去掉 `qca-ppe-qos` 这一行。
4. VIKINGYFY 这边有个分支出入：ZqinKing 的 jdcloud immwrt 用的是 VIKINGYFY 的 `main` 分支，
   而这里用的是 README 点名的 PPE 分支 `owrt`。首次构建时需核对 `owrt` 分支是否包含
   jdcloud 机型与 PPE 代码。
5. PPE 路线没有 istore feed，不写 `luci-app-store`（与官方 OpenWrt 同理）。

## 刻意没采纳的参考内容

| 内容 | 来源 | 不采纳的原因 |
| --- | --- | --- |
| `CONFIG_USE_APK=n`（关掉 apk，用 opkg） | ZqinKing `compile_base.config` | v1 默认用 apk；iStore 等插件按 apk 走，改包管理器牵连太大 |
| `CONFIG_TARGET_ROOTFS_INITRAMFS=n`（不产 initramfs 镜像） | ZqinKing jdcloud deconfig | 会破坏 `docs/FLASHING.md` 的首次刷机流程（initramfs + sysupgrade） |
| `ath11k-firmware-qcn9074-ddwrt`（DDWRT 版固件） | ZqinKing deconfig | 与上游 Device 定义默认选的 `ath11k-firmware-qcn9074` 冲突，v1 保持原样 |
| PassWall v1（+ Xray） | roc `General.config`；ZqinKing `proxy.config` | v1 已定 OpenClash（主）+ PassWall2，两套代理栈不混用 |
| Aurora 主题、繁体中文 `zh_Hant` | roc `General.config` | 用户定的是 Argon + 简体中文 |
| `luci-app-cupsd`（打印服务） | ZqinKing deconfig | 路由器上不需要打印服务 |
| OAF 应用过滤 | ZqinKing `compile_base.config` | ZqinKing 自己的 README 也说 OAF 默认禁用以规避网络栈影响 |
| `CONFIG_BUSYBOX_CONFIG_TELNET=y`（busybox 开 telnet） | ZqinKing `compile_base.config` | 明文协议，有安全风险，用户没要求 |
| `CONFIG_PACKAGE_automount=n`（关掉自动挂载） | ZqinKing `compile_base.config` | v1 靠设备默认选中 automount，U盘自动挂载有用，不关 |
| `luci-app-3cat`、`luci-app-vantage` | roc `General.config`；ZqinKing `compile_base.config` | 不够主流，作用不明，不引入 |
| ZqinKing / roc 的 MULTI_PROFILE 写法（一个构建产 4 个机型） | 两仓库的 deconfig / JDCloud.config | v1 是单机型 choice 符号、一次构建一个机型（2026-11-15 的教训）；v2 沿用 v1 的单机型写法，不改构建模型 |

## 参考文件（2026-11-15 实读）

- ZqinKing/wrt_release：`wrt_core/deconfig/jdcloud_ipq60xx_immwrt.config`、
  `jdcloud_ipq60xx_libwrt.config`（两份内容相同）、`compile_base.config`、
  `fragments/nss.config`、`fragments/proxy.config`、`fragments/docker_deps.config`、
  `compilecfg/jdcloud_ipq60xx_immwrt.ini`（源 VIKINGYFY/immortalwrt，分支 main，
  片段 nss,docker_deps,proxy）、`compilecfg/jdcloud_ipq60xx_libwrt.ini`
  （源 LiBwrt/openwrt-6.x，分支 25.12-nss，片段相同）。
- laipeng668/openwrt-ci-roc：`configs/JDCloud.config`、`configs/General.config`。
- JuliusBairaktaris/openwrt-ppe-nss（分支 ppe-nss）：`seeds/qualcommax-nss-wifi.seed`
  （注：该 seed 文件写的是 `CONFIG_TARGET_qualcommax_ipq807x=y`，PPE 配置本身是按
  ipq807x 写的；v2 的 PPE 配置把子目标换成 ipq60xx，开关照搬）、
  `target/linux/qualcommax/image/ipq60xx.mk`（已核对 jdcloud 两机型在列）。
- VIKINGYFY/immortalwrt（分支 owrt）：README（“owrt 为多平台通用，MTK、QCA、QCB
  带有满血 PPE 驱动”，源码取自 JuliusBairaktaris 等项目）。
- King-Of-Knights/openwrt-6.x：README（`nss-setup/` 目录与
  `scripts/apply-feed-patches.sh`——这个“构建前应用 feeds 修复补丁”的做法值得将来
  借鉴到 workflow 里，但它不是配置项，所以 v2 没用到它）。

## 构建与验证顺序（首次构建前必读）

1. 本仓库已按本说明接入构建：`build.yml` 的 matrix 已有 `ppe`、`ppe-immwrt` 两个 source
   与对应 REPO_URL / REPO_BRANCH；diy-part1 的 source 判断已同步扩展
   （ppe 加 nss feed；iStore 只加 ImmortalWrt 系；athena-led 照 v1 的做法拉取）。
2. 首次构建建议先只跑 PPE 的 4 个纯净版（`ppe` / `ppe-immwrt` × 两机型 × pure，
   手动触发时可单选 source），验证构建与刷机，通过后再跑 plus 与 v2 的 12 个。
3. v2 的 12 个配置与 v1 的差异以
   `diff <v1 仓库>/configs/<名>.config <本仓库>/configs/<名>.config` 为准。

## 待确认的问题

1. `CONFIG_IPQ_MEM_PROFILE_256=y`、`CONFIG_NSS_MEM_PROFILE_HIGH=y` 等 NSS 内存档位
   取自 ZqinKing 的 nss 片段（该片段明确用于 jdcloud_ipq60xx），但档位含义未深究，
   以首次构建的 `Config-*.txt` 与实际运行为准。
2. roc 与 ZqinKing 在 `sqm-scripts-nss` 上冲突（roc 设 `n`，ZqinKing 设 `y`），
   v2 按 ZqinKing 取 `y`，见上文 LiBwrt 一节。
3. `luci-app-emmc-health` 在官方 OpenWrt main 的 feeds 里是否存在未核对；
   若不存在，defconfig 会自动丢掉，不影响构建，但 pure 版就少了这个监测。
4. PPE 路线的 5 条未验证风险，见上文。
