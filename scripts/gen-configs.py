#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成 OpenWrt-JDCloud-v2 的 20 个构建配置（5 源码 × 2 机型 × 纯净/插件）。

用法：
    python3 scripts/gen-configs.py               # 重新生成 configs/*.config

本仓库是 v1（hhliulei/OpenWrt-JDCloud，12 个固件）的 v2 仓库：
- 12 个配置（immortalwrt / libwrt / openwrt × 2 机型 × 纯净/插件）以 v1 为底，
  按 2026-11-15 实读的参考仓库做了有据可查的增补，详见 docs/V2-NOTES.md。
- PPE 路线的 8 个配置（ppe 与 ppe-immwrt 两个源码 × 2 机型 × 纯净/插件）是新增的
  第 4、5 条技术路线，IPQ60xx 未经源码作者实测，属实验性质，先编出来验证再说。

参考来源（2026-11-15 实读原文）：
- ZqinKing/wrt_release：wrt_core/deconfig/jdcloud_ipq60xx_immwrt.config、
  jdcloud_ipq60xx_libwrt.config、compile_base.config、
  fragments/nss.config、fragments/proxy.config、fragments/docker_deps.config、
  compilecfg/jdcloud_ipq60xx_immwrt.ini、jdcloud_ipq60xx_libwrt.ini
- laipeng668/openwrt-ci-roc：configs/JDCloud.config、configs/General.config
- JuliusBairaktaris/openwrt-ppe-nss（分支 ppe-nss）：seeds/qualcommax-nss-wifi.seed、
  target/linux/qualcommax/image/ipq60xx.mk（已核对 jdcloud_re-cs-02/_07 均在）
- VIKINGYFY/immortalwrt（分支 owrt）：README（满血 PPE，多平台通用）
- King-Of-Knights/openwrt-6.x：README（nss-setup/ 与 scripts/apply-feed-patches.sh，
  仅作思路参考，未用作配置来源）

铁律（2026-11-15 的 #3/#4 失败教训）：
- 机型必须用 Target Profile choice 符号 CONFIG_TARGET_qualcommax_ipq60xx_DEVICE_<机型>=y，
  绝不能用 CONFIG_TARGET_DEVICE_qualcommax_ipq60xx_DEVICE_<机型>=y（MULTI_PROFILE 菜单布尔项，
  不开 MULTI_PROFILE 时 defconfig 会悄悄丢掉，choice 默认选中首个机型 8devices_mango-dvk）。
- 绝不能写 CONFIG_TARGET_PER_DEVICE_ROOTFS=y（同样只在 MULTI_PROFILE 菜单里才可见）。
"""

from __future__ import annotations

import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "configs"

SOURCES = {
    "immortalwrt": {
        "repo": "https://github.com/laipeng668/immortalwrt.git",
        "branch": "openwrt-25.12",
        "label": "ImmortalWrt",
    },
    "libwrt": {
        "repo": "https://github.com/LiBwrt/openwrt-6.x.git",
        "branch": "25.12-nss",
        "label": "LiBwrt openwrt-6.x（NSS）",
    },
    "openwrt": {
        "repo": "https://github.com/openwrt/openwrt.git",
        # 官方 openwrt-25.12 分支里没有 jdcloud 机型，jdcloud 支持 2026-01 才合进 main。
        "branch": "main",
        "label": "官方 OpenWrt",
    },
    "ppe": {
        "repo": "https://github.com/JuliusBairaktaris/openwrt-ppe-nss.git",
        "branch": "ppe-nss",
        # 实验路线：以太走上游 qca_ppe/qca_edma，WiFi 走 NSS（nss-wifi-drv + ath11k），
        # 内核 6.18。作者实测机是小米 AX3600（IPQ807x），IPQ60xx 未经实测。
        "label": "PPE+NSS（实验）",
    },
    "ppe-immwrt": {
        "repo": "https://github.com/VIKINGYFY/immortalwrt.git",
        "branch": "owrt",
        # 实验路线：ImmortalWrt 版 PPE。README 明言 owrt 分支“多平台通用，
        # MTK、QCA、QCB 带有满血 PPE 驱动”，源码取自 JuliusBairaktaris/openwrt-ppe-nss
        # 等项目。注意：ZqinKing 的 jdcloud immwrt 用的是 VIKINGYFY 的 main 分支，
        # 这里用的是 README 点名的 PPE 分支 owrt，首次构建时需核对分支内容。
        "label": "PPE+NSS ImmortalWrt 版（实验）",
    },
}

DEVICES = {
    "jdcloud_re-cs-02": {"label": "雅典娜 RE-CS-02", "wifi": True},
    "jdcloud_re-cs-07": {"label": "太乙 RE-CS-07", "wifi": False},
}

FLAVOURS = ("pure", "plus")

# 两条 PPE 路线共用同一套 PPE/NSS-WiFi 开关（VIKINGYFY 的 PPE 代码即取自 JuliusBairaktaris）。
PPE_SOURCES = ("ppe", "ppe-immwrt")


def base_config(source: str, device: str) -> list[str]:
    """纯净版共用部分（v2：v1 底 + 参考仓库增补）。"""
    lines = [
        "# v2 纯净版基础：完整网络功能 + LuCI + 常用管理插件，保证稳定，不过度精简。",
        "CONFIG_TARGET_qualcommax=y",
        "CONFIG_TARGET_qualcommax_ipq60xx=y",
        # 机型必须用 Target Profile choice 符号（见文件头铁律）。
        f"CONFIG_TARGET_qualcommax_ipq60xx_DEVICE_{device}=y",
        "CONFIG_TARGET_ROOTFS_SQUASHFS=y",
        "CONFIG_DEVEL=y",
        "CONFIG_CCACHE=y",
        "# 中文界面（LuCI 语言包，简体中文）",
        "CONFIG_LUCI_LANG_zh_Hans=y",
        "CONFIG_PACKAGE_luci=y",
        "CONFIG_PACKAGE_luci-theme-argon=y",
        "CONFIG_PACKAGE_luci-app-argon-config=y",
        "CONFIG_PACKAGE_luci-i18n-base-zh-cn=y",
        "CONFIG_PACKAGE_luci-i18n-firewall-zh-cn=y",
        "CONFIG_PACKAGE_luci-i18n-package-manager-zh-cn=y",
        "CONFIG_PACKAGE_luci-app-firewall=y",
        "CONFIG_PACKAGE_luci-app-package-manager=y",
        "CONFIG_PACKAGE_luci-app-arpbind=y",
        "CONFIG_PACKAGE_luci-app-autoreboot=y",
        "CONFIG_PACKAGE_luci-app-cpufreq=y",
        "CONFIG_PACKAGE_luci-app-samba4=y",
        "CONFIG_PACKAGE_luci-app-uhttpd=y",
        "# 默认设置包（roc General.config / ZqinKing compile_base.config 均显式写明）",
        "CONFIG_PACKAGE_default-settings=y",
        "CONFIG_PACKAGE_default-settings-chn=y",
        "# 完整版 dnsmasq（插件版的 OpenClash / AdGuard Home 需要）",
        "CONFIG_PACKAGE_dnsmasq-full=y",
        "# CONFIG_PACKAGE_dnsmasq is not set",
        "CONFIG_PACKAGE_curl=y",
        "CONFIG_PACKAGE_ca-bundle=y",
        "CONFIG_PACKAGE_ca-certificates=y",
        "CONFIG_PACKAGE_bash=y",
        "CONFIG_PACKAGE_coreutils=y",
        "CONFIG_PACKAGE_htop=y",
        "CONFIG_PACKAGE_btop=y",
        "CONFIG_PACKAGE_tmux=y",
        "CONFIG_PACKAGE_dmesg=y",
        "CONFIG_PACKAGE_nano-full=y",
        "CONFIG_PACKAGE_unzip=y",
        "CONFIG_PACKAGE_xz=y",
        "CONFIG_PACKAGE_openssh-sftp-server=y",
        "CONFIG_PACKAGE_zoneinfo-asia=y",
        "CONFIG_PACKAGE_zram-swap=y",
        "CONFIG_PACKAGE_kmod-lib-lz4=y",
        "# zram 内核后端（roc General.config）",
        "CONFIG_KERNEL_ZRAM_BACKEND_LZ4=y",
        "CONFIG_KERNEL_ZRAM_BACKEND_LZO=y",
        "CONFIG_KERNEL_ZRAM_DEF_COMP_LZ4=y",
        "CONFIG_PACKAGE_block-mount=y",
        "CONFIG_PACKAGE_kmod-usb-storage=y",
        "CONFIG_PACKAGE_kmod-usb-storage-extras=y",
        "CONFIG_PACKAGE_kmod-usb-storage-uas=y",
        "CONFIG_PACKAGE_kmod-usb2=y",
        "CONFIG_PACKAGE_kmod-usb3=y",
        "CONFIG_PACKAGE_kmod-fs-ext4=y",
        "CONFIG_PACKAGE_kmod-fs-vfat=y",
        "CONFIG_PACKAGE_kmod-fs-exfat=y",
        "CONFIG_PACKAGE_ntfs3-mount=y",
        "CONFIG_PACKAGE_e2fsprogs=y",
        "CONFIG_PACKAGE_f2fs-tools=y",
        "CONFIG_PACKAGE_autocore=y",
        "CONFIG_PACKAGE_coremark=y",
        "# 磁盘/分区工具（roc General.config / ZqinKing deconfig）",
        "CONFIG_PACKAGE_fdisk=y",
        "CONFIG_PACKAGE_cfdisk=y",
        "CONFIG_PACKAGE_sgdisk=y",
        "CONFIG_PACKAGE_hdparm=y",
        "CONFIG_PACKAGE_smartmontools-drivedb=y",
        "CONFIG_PACKAGE_fstrim=y",
        "CONFIG_PACKAGE_tune2fs=y",
        "CONFIG_PACKAGE_usbutils=y",
        "# 诊断/网络工具（ZqinKing compile_base.config）",
        "CONFIG_PACKAGE_tcpdump=y",
        "CONFIG_PACKAGE_qrencode=y",
        "CONFIG_PACKAGE_openssl-util=y",
        "CONFIG_PACKAGE_libopenssl-legacy=y",
        "CONFIG_PACKAGE_luci-lib-ipkg=y",
        "CONFIG_PACKAGE_kmod-netlink-diag=y",
        "CONFIG_PACKAGE_kmod-inet-diag=y",
        "CONFIG_PACKAGE_kmod-tls=y",
        "# 链路聚合协议与 nftables 兼容层（ZqinKing compile_base.config）",
        "CONFIG_PACKAGE_proto-bonding=y",
        "CONFIG_PACKAGE_iptables-nft=y",
        "CONFIG_PACKAGE_ip6tables-nft=y",
        "# WireGuard 协议支持（roc General.config / ZqinKing compile_base.config）",
        "CONFIG_PACKAGE_luci-proto-wireguard=y",
        "# eMMC 健康监测（ZqinKing jdcloud deconfig；官方 OpenWrt 下若 feeds 里没有此包，",
        "# make defconfig 会自动丢掉这一行，不影响构建）",
        "CONFIG_PACKAGE_luci-app-emmc-health=y",
    ]
    if DEVICES[device]["wifi"]:
        lines += [
            "# 雅典娜三频 WiFi",
            "CONFIG_PACKAGE_kmod-ath11k-pci=y",
        ]
        if source == "ppe-immwrt":
            # 该 fork 的机型定义（VIKINGYFY/immortalwrt owrt 分支
            # target/linux/qualcommax/image/ipq60xx.mk，Device/jdcloud_re-cs-02）
            # 自带 ath11k-firmware-qcn9074-ddwrt；再写标准版两个包会往同一位置
            # 写固件文件、镜像打包时冲突（run #1、run #3 的两个雅典娜任务都死
            # 在这一步，exit 2），所以这里明确不写标准版，只留 fork 默认的 ddwrt 版。
            lines += ["# CONFIG_PACKAGE_ath11k-firmware-qcn9074 is not set"]
        else:
            lines += ["CONFIG_PACKAGE_ath11k-firmware-qcn9074=y"]
        lines += [
            "CONFIG_PACKAGE_ipq-wifi-jdcloud_re-cs-02=y",
            "CONFIG_PACKAGE_hostapd-common=y",
            "# 雅典娜顶部点阵屏（与 v1 相同：构建时需由 diy-part2 同类步骤从 NONGFAH 拉取）",
            "CONFIG_PACKAGE_luci-app-athena-led=y",
            "CONFIG_PACKAGE_luci-i18n-athena-led-zh-cn=y",
        ]
        if source in PPE_SOURCES:
            lines += [
                "# PPE 路线用 wpad-openssl（JuliusBairaktaris seed），不用 wpad-basic-mbedtls",
                "CONFIG_PACKAGE_wpad-openssl=y",
                "# CONFIG_PACKAGE_wpad-basic-mbedtls is not set",
            ]
        else:
            lines += ["CONFIG_PACKAGE_wpad-basic-mbedtls=y"]
    else:
        lines += [
            "# 太乙是有线路由：上游 Device 定义本身已排除 ath11k / wpad，这里再明确关掉（NoWiFi）",
            "# CONFIG_PACKAGE_kmod-ath11k is not set",
            "# CONFIG_PACKAGE_kmod-ath11k-ahb is not set",
            "# CONFIG_PACKAGE_kmod-ath11k-pci is not set",
            "# CONFIG_PACKAGE_ath11k-firmware-ipq6018 is not set",
            "# CONFIG_PACKAGE_ath11k-firmware-qcn9074 is not set",
            "# CONFIG_PACKAGE_ipq-wifi-jdcloud_re-cs-07 is not set",
            "# CONFIG_PACKAGE_wpad-basic-mbedtls is not set",
            "# CONFIG_PACKAGE_wpad-openssl is not set",
            "# CONFIG_PACKAGE_hostapd-common is not set",
        ]
    if source == "libwrt":
        lines += [
            "# LiBwrt NSS 11.4（v1 底）+ ZqinKing nss.config 片段（jdcloud_ipq60xx 专用）",
            "CONFIG_NSS_FIRMWARE_VERSION_11_4=y",
            "# CONFIG_NSS_FIRMWARE_VERSION_12_5 is not set",
            "CONFIG_ATH11K_MEM_PROFILE_512M=y" if DEVICES[device]["wifi"] else "",
            "CONFIG_PACKAGE_kmod-qca-nss-drv=y",
            "CONFIG_PACKAGE_kmod-qca-nss-ecm=y",
            "CONFIG_IPQ_MEM_PROFILE_256=y",
            "CONFIG_NSS_MEM_PROFILE_HIGH=y",
            "CONFIG_PACKAGE_sqm-scripts-nss=y",
            "CONFIG_PACKAGE_kmod-qca-mcs=y",
            "CONFIG_KERNEL_SKB_RECYCLER=y",
            "CONFIG_KERNEL_SKB_RECYCLER_MULTI_CPU=y",
            "CONFIG_PACKAGE_kmod-qca-nss-drv-igs=y",
            "CONFIG_PACKAGE_kmod-qca-nss-drv-l2tpv2=y",
            "CONFIG_PACKAGE_kmod-qca-nss-drv-lag-mgr=y",
            "CONFIG_PACKAGE_kmod-qca-nss-drv-pppoe=y",
            "CONFIG_PACKAGE_kmod-qca-nss-drv-pptp=y",
        ]
        if DEVICES[device]["wifi"]:
            lines += [
                "CONFIG_ATH11K_NSS_SUPPORT=y",
                "CONFIG_ATH11K_NSS_MESH_SUPPORT=y",
                "CONFIG_NSS_DRV_WIFI_MESH_ENABLE=y",
                "CONFIG_PACKAGE_MAC80211_MESH=y",
            ]
    elif source == "immortalwrt":
        lines += [
            "# ImmortalWrt：用测试内核（CONFIG_TESTING_KERNEL，当前为 6.18）+ NSS 12.5",
            "# （与 roc JDCloud.config 一致：TESTING_KERNEL / ATH11K_MEM_PROFILE_512M / 12_5）",
            "CONFIG_TESTING_KERNEL=y",
            "CONFIG_NSS_FIRMWARE_VERSION_12_5=y",
            "# CONFIG_NSS_FIRMWARE_VERSION_11_4 is not set",
            "# NSS 通用性能开关（ZqinKing nss.config 片段；不含 11.4 专属的 drv 扩展包）",
            "CONFIG_IPQ_MEM_PROFILE_256=y",
            "CONFIG_NSS_MEM_PROFILE_HIGH=y",
            "CONFIG_PACKAGE_kmod-qca-mcs=y",
            "CONFIG_KERNEL_SKB_RECYCLER=y",
            "CONFIG_KERNEL_SKB_RECYCLER_MULTI_CPU=y",
        ]
        if DEVICES[device]["wifi"]:
            lines += [
                "# IPQ60xx 的 NSS 12.5 不提供 WiFi offload，走正常 ath11k",
                "# CONFIG_ATH11K_NSS_SUPPORT is not set",
                "# CONFIG_ATH11K_NSS_MESH_SUPPORT is not set",
                "CONFIG_ATH11K_MEM_PROFILE_512M=y",
            ]
    elif source in PPE_SOURCES:
        ppe_note = (
            "JuliusBairaktaris/openwrt-ppe-nss，分支 ppe-nss，内核 6.18"
            if source == "ppe"
            else "VIKINGYFY/immortalwrt，分支 owrt（ImmortalWrt 底，PPE 代码取自 JuliusBairaktaris）"
        )
        lines += [
            f"# PPE 路线（{ppe_note}）：",
            "# 以太走上游 qca_ppe / qca_edma（PPE 硬件流表，由该 fork 的 target 代码提供，",
            "# 不是 Kconfig 开关）；WiFi 走 NSS（nss-wifi-drv + ath11k，见 seed 文件）。",
            "# 注意：该作者实测机是小米 AX3600（IPQ807x），IPQ60xx 未经实测，本路线属实验性质。",
        ]
        if DEVICES[device]["wifi"]:
            lines += [
                "# NSS WiFi（seed 文件核心两行；仅雅典娜有 WiFi，太乙不用）",
                "CONFIG_PACKAGE_kmod-nss-wifi-drv=y",
                "CONFIG_ATH11K_NSS_WIFI=y",
                "CONFIG_ATH11K_MEM_PROFILE_512M=y",
            ]
        else:
            lines += [
                "# 太乙无 WiFi：不写 kmod-nss-wifi-drv / ATH11K_NSS_WIFI；",
                "# PPE 以太加速仍由该 fork 的 target 代码提供。",
            ]
    else:  # openwrt
        lines += [
            "# 官方 OpenWrt：上游不含 NSS 闭源加速，走原生 ath11k + flow offload",
            "# （本段不写任何 NSS 开关）",
        ]
    # 去掉上面条件表达式产生的空行
    return [line for line in lines if line != ""]


def plus_config(source: str) -> list[str]:
    """插件版在纯净版基础上追加的部分（v2：v1 底 + 参考仓库增补 + Docker 依赖补齐）。"""
    lines = [
        "# ---- 插件版追加（在纯净版基础上） ----",
        "# 容器：Docker / Dockerman",
        "CONFIG_PACKAGE_dockerd=y",
        "CONFIG_PACKAGE_docker=y",
        "CONFIG_PACKAGE_docker-compose=y",
        "CONFIG_PACKAGE_luci-app-dockerman=y",
        "CONFIG_PACKAGE_luci-lib-docker=y",
        "CONFIG_PACKAGE_ttyd=y",
        "CONFIG_PACKAGE_luci-app-ttyd=y",
        "CONFIG_PACKAGE_kmod-veth=y",
        "CONFIG_PACKAGE_kmod-br-netfilter=y",
        "# Docker 运行时依赖（ZqinKing fragments/docker_deps.config，nftables 后端，Docker v29）",
        "CONFIG_PACKAGE_fuse-overlayfs=y",
        "CONFIG_PACKAGE_kmod-crypto-acompress=y",
        "CONFIG_PACKAGE_kmod-crypto-blake2b=y",
        "CONFIG_PACKAGE_kmod-crypto-xxhash=y",
        "CONFIG_PACKAGE_kmod-fs-btrfs=y",
        "CONFIG_PACKAGE_kmod-lib-lzo=y",
        "CONFIG_PACKAGE_kmod-lib-raid6=y",
        "CONFIG_PACKAGE_kmod-lib-xor=y",
        "CONFIG_PACKAGE_kmod-lib-xxhash=y",
        "CONFIG_PACKAGE_kmod-lib-zlib-deflate=y",
        "CONFIG_PACKAGE_kmod-lib-zlib-inflate=y",
        "CONFIG_PACKAGE_kmod-lib-zstd=y",
        "CONFIG_PACKAGE_kmod-ipt-nat=y",
        "CONFIG_PACKAGE_kmod-ipt-nat6=y",
        "CONFIG_PACKAGE_kmod-ipt-physdev=y",
        "CONFIG_PACKAGE_kmod-nf-ipvs=y",
        "CONFIG_PACKAGE_kmod-nf-nat6=y",
        "CONFIG_PACKAGE_kmod-dummy=y",
        "CONFIG_PACKAGE_iptables-mod-extra=y",
        "CONFIG_PACKAGE_nftables=y",
        "CONFIG_PACKAGE_kmod-nft-nat=y",
        "CONFIG_PACKAGE_kmod-nft-netdev=y",
        "# 透明代理：OpenClash（主）+ PassWall2",
        "CONFIG_PACKAGE_luci-app-openclash=y",
        "CONFIG_PACKAGE_luci-app-passwall2=y",
        "CONFIG_PACKAGE_ipset=y",
        "CONFIG_PACKAGE_ip-full=y",
        "CONFIG_PACKAGE_kmod-nft-tproxy=y",
        "CONFIG_PACKAGE_kmod-nft-queue=y",
        "CONFIG_PACKAGE_kmod-tun=y",
        "# DNS：AdGuard Home + SmartDNS + MosDNS",
        "CONFIG_PACKAGE_adguardhome=y",
        "CONFIG_PACKAGE_luci-app-adguardhome=y",
        "CONFIG_PACKAGE_smartdns=y",
        "CONFIG_PACKAGE_luci-app-smartdns=y",
        "CONFIG_PACKAGE_mosdns=y",
        "CONFIG_PACKAGE_luci-app-mosdns=y",
        "# 常用管理：DDNS / UPnP / 磁盘管理 / 网络唤醒 / 看门狗 / 文件管理",
        "CONFIG_PACKAGE_luci-app-ddns=y",
        "CONFIG_PACKAGE_ddns-scripts=y",
        "CONFIG_PACKAGE_ddns-scripts-cloudflare=y",
        "CONFIG_PACKAGE_luci-app-upnp=y",
        "CONFIG_PACKAGE_luci-app-diskman=y",
        "CONFIG_PACKAGE_luci-app-hd-idle=y",
        "CONFIG_PACKAGE_luci-app-wol=y",
        "CONFIG_PACKAGE_luci-app-watchcat=y",
        "CONFIG_PACKAGE_luci-app-quickfile=y",
        "CONFIG_PACKAGE_luci-app-sqm=y",
        "# 下载与远程：Aria2 / OpenList2 / FRP / ACME（roc JDCloud.config / General.config）",
        "CONFIG_PACKAGE_ariang=y",
        "CONFIG_PACKAGE_luci-app-aria2=y",
        "CONFIG_ARIA2_OPENSSL=y",
        "# CONFIG_ARIA2_GNUTLS is not set",
        "# CONFIG_ARIA2_NOSSL is not set",
        "# CONFIG_ARIA2_LIBXML2 is not set",
        "CONFIG_ARIA2_EXPAT=y",
        "# CONFIG_ARIA2_NOXML is not set",
        "CONFIG_ARIA2_BITTORRENT=y",
        "CONFIG_ARIA2_METALINK=y",
        "CONFIG_ARIA2_SFTP=y",
        "CONFIG_ARIA2_ASYNC_DNS=y",
        "# CONFIG_ARIA2_COOKIE is not set",
        "CONFIG_ARIA2_WEBSOCKET=y",
        "CONFIG_PACKAGE_luci-app-openlist2=y",
        "CONFIG_PACKAGE_luci-app-frps=y",
        "CONFIG_PACKAGE_luci-app-frpc=y",
        "CONFIG_PACKAGE_luci-app-acme=y",
        "CONFIG_PACKAGE_acme-acmesh-dnsapi=y",
        "# 组网与分流：EasyTier / Lucky / PBR / netwiz（ZqinKing compile_base.config）",
        "CONFIG_PACKAGE_easytier=y",
        "CONFIG_PACKAGE_luci-app-easytier=y",
        "CONFIG_EASYTIER_INCLUDE_WEBCONSOLE=n",
        "CONFIG_PACKAGE_luci-app-lucky=y",
        "CONFIG_PACKAGE_luci-app-pbr=y",
        "CONFIG_PACKAGE_luci-app-netwiz=y",
        "CONFIG_PACKAGE_luci-i18n-netwiz-zh-cn=y",
        "# Web 服务与日志（roc JDCloud.config）",
        "CONFIG_PACKAGE_nginx-full=y",
        "CONFIG_PACKAGE_logrotate=y",
        "# KMS 激活服务（roc General.config / ZqinKing deconfig）",
        "CONFIG_PACKAGE_luci-app-vlmcsd=y",
    ]
    if source in ("immortalwrt", "libwrt"):
        lines += [
            "# 应用商店（仅 ImmortalWrt / LiBwrt 有 istore feed；官方 OpenWrt 与 PPE 路线没有）",
            "CONFIG_PACKAGE_luci-app-store=y",
            "CONFIG_PACKAGE_luci-lib-taskd=y",
            "CONFIG_PACKAGE_taskd=y",
        ]
    else:
        lines += [
            "# 注意：官方 OpenWrt 与 PPE 路线没有 istore feed，不写 luci-app-store。",
        ]
    if source in PPE_SOURCES:
        lines += [
            "# ---- PPE 路线追加（JuliusBairaktaris seed 文件的 Optional 部分，插件版才加） ----",
            "# PPE 塑形 SQM（qca-ppe-qos 依赖该 fork 的 feed 补丁；若首次构建丢包或报错，",
            "# 先看 Config-*.txt，再决定是否去掉 qca-ppe-qos 这一行）",
            "CONFIG_PACKAGE_sqm-scripts=y",
            "CONFIG_PACKAGE_luci-app-sqm=y",
            "CONFIG_PACKAGE_qca-ppe-qos=y",
            "# luci-app-qca-ppe-qos 需要该作者的 luci fork，默认 feeds 下 defconfig 会丢掉，",
            "# 这里明确不写，免得误以为已启用。",
            "# CONFIG_PACKAGE_luci-app-qca-ppe-qos is not set",
            "# tc 与调度模块（PPE offload 由此驱动：flower 分类、prio/mqprio/ets/red/gred、",
            "# police、pedit、vlan 动作）",
            "CONFIG_PACKAGE_tc-tiny=y",
            "CONFIG_PACKAGE_kmod-sched-flower=y",
            "CONFIG_PACKAGE_kmod-sched-prio=y",
            "CONFIG_PACKAGE_kmod-sched-act-police=y",
            "CONFIG_PACKAGE_kmod-sched-act-pedit=y",
            "CONFIG_PACKAGE_kmod-sched-act-vlan=y",
            "CONFIG_PACKAGE_kmod-sched-mqprio=y",
            "CONFIG_PACKAGE_kmod-sched-ets=y",
            "CONFIG_PACKAGE_kmod-sched-red=y",
            "CONFIG_PACKAGE_kmod-sched-gred=y",
            "# DCB（DSCP 到优先级的映射）与组播路由（seed 文件）",
            "CONFIG_PACKAGE_dcb=y",
            "CONFIG_PACKAGE_devlink=y",
            "CONFIG_PACKAGE_ethtool-full=y",
            "CONFIG_KERNEL_DCB=y",
            "CONFIG_KERNEL_IP_MROUTE=y",
            "CONFIG_KERNEL_IPV6_MROUTE=y",
        ]
    return lines


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for source, sinfo in SOURCES.items():
        for device, dinfo in DEVICES.items():
            for flavour in FLAVOURS:
                lines = [
                    f"# OpenWrt-JDCloud v2：{sinfo['label']} / {dinfo['label']} / "
                    + ("纯净版" if flavour == "pure" else "插件版"),
                    f"# 源码：{sinfo['repo']}（分支 {sinfo['branch']}）",
                    "# 内核：不写死版本，用该分支的默认内核",
                    "# 默认：LAN 192.168.10.1，主机名 ll，root/root，Argon 主题，中文",
                    "# 软件源：不裁剪，构建时用 feeds update/install -a 拉取全部 feed",
                ]
                if source in PPE_SOURCES:
                    lines += [
                        "# ⚠ 实验路线：PPE 在 IPQ60xx 上未经该源码作者实测（作者实测机为小米 AX3600 / IPQ807x），",
                        "# 编出来后必须先在雅典娜/太乙上实测（有线速率、WiFi、PPE 是否生效）再决定是否采用。",
                    ]
                lines += [""]
                lines += base_config(source, device)
                if flavour == "plus":
                    lines += [""] + plus_config(source)
                name = f"{source}-{device}-{flavour}.config"
                (OUT / name).write_text("\n".join(lines) + "\n", encoding="utf-8")
                print(f"wrote configs/{name}")


if __name__ == "__main__":
    main()
