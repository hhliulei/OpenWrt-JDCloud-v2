# 刷机与升级说明（FLASHING.md）

适用机型：雅典娜 JDCloud RE-CS-02、太乙 JDCloud RE-CS-07。
平台：qualcommax / ipq60xx，SoC Qualcomm IPQ6010。

## 先看：两个文件别用错

每个 Release 里一个机型一般有这两个固件文件（LiBwrt 还多一个 `factory.bin`）：

| 文件 | 什么时候用 |
| --- | --- |
| `*squashfs-factory-*.bin` | 首次从原厂固件刷入时用（只在 LiBwrt 的 Release 里有） |
| `*squashfs-sysupgrade-*.bin` | 已经是 OpenWrt / ImmortalWrt，要升级时用 |
| `*initramfs-uImage.itb` | 内存启动镜像，用于首次刷机 / 救砖流程（见下） |

**不要拿 sysupgrade 当 factory 用**，也不要拿雅典娜的固件刷太乙、反过来也不行。
刷之前先核对文件名里的机型（`jdcloud_re-cs-02` 还是 `jdcloud_re-cs-07`），
再用 Release 里附的 `sha256sums.txt` 校验下载完整性：

```sh
sha256sum -c sha256sums.txt
```

## 动手前必做：备份

1. **备份原厂固件**：刷第三方固件前先把原厂固件、原厂后台的配置导出来，留好恢复的路。
2. **备份 ART 分区**：ART（eMMC 分区表里一般是 p15）存着每台机器唯一的
   MAC、序列号和 WiFi 校准数据。丢了机器还能用，但不再是出厂那个身份，
   WiFi 也可能不正常。先备份，再动手。
3. **别碰 SBL1**：一级引导（p1），刷坏只能上编程器救。
4. **改内存才碰 CDT**：CDT（p10/p11）是内存识别配置，不改内存就不要动，
   错配不会报错，但运行会随机崩。

## 首次刷机（原厂 → OpenWrt，通用流程）

原厂固件一般要先开 telnet / SSH，再刷第三方 U-Boot、改 GPT 分区表，
然后用内存启动镜像进 OpenWrt，最后用 sysupgrade 写盘。
不同原厂版本开 telnet 的方法不一样，请按当时最新的教程操作，
下面是通用步骤，具体命令以教程为准：

1. 开 telnet / SSH，确认能进原厂系统。
2. 备份 ART 与原厂固件。
3. 刷第三方 U-Boot（亚瑟 / 雅典娜通用款），刷 GPT 分区表（双分区结构）。
4. 用 TFTP 把 `initramfs-uImage.itb` 传上去，从内存启动 OpenWrt。
5. 进 OpenWrt 后台（默认 192.168.10.1），用 sysupgrade 上传
   `*squashfs-sysupgrade-*.bin`，**不要勾选“保留配置”**（原厂配置不通用）。
6. 等待重启，重新进后台，确认机型、WiFi（雅典娜）、LAN 口都正常。

LiBwrt 的 Release 里有 `factory.bin` 时，第 4-5 步可以简化为直接刷 factory，
但仍建议先走一遍 initramfs 验证机器没问题。

## 升级（已是 OpenWrt / ImmortalWrt）

- 在 LuCI「系统 → 备份 / 升级」里上传 `*squashfs-sysupgrade-*.bin`。
- 同一个仓库、同一个机型的版本之间升级，可以勾选“保留配置”；
  换源码（比如 ImmortalWrt 换到 LiBwrt）或换机型时，建议不保留配置，
  刷完重新设置。
- 升级前先确认 Release 的 tag：源码、机型、纯净版 / 插件版要和当前一致，
  tag 形如 `immortalwrt-jdcloud_re-cs-02-pure-26.11.15-1830`。

## 救砖

- 能进 U-Boot：用 TFTP 重新拉 `initramfs-uImage.itb` 启动，再 sysupgrade。
- 能进 TTL：按 U-Boot 提示中断启动，走 TFTP 流程。
- U-Boot 也坏了：USB 9008 线刷恢复（需要 9008 工具与原厂还原固件，
  参考 ones20250/Openwrt-AX6600 仓库里的「刷机救砖全家桶」思路）。
- 救砖前先确认手头有原厂还原固件和正确的 GPT 分区文件，型号别拿错。

## 首次开机

- 管理地址：`192.168.10.1`，用户名 `root`，密码 `root`。
- 主机名：`ll`，主题 Argon，语言中文，时区 Asia/Shanghai。
- 雅典娜 WiFi：`ll`（2.4G）/ `ll-5G`（5G-1）/ `ll-5G-2`（5G-2），
  密码都是 `12345678`，首次使用后请在 LuCI 里改掉。
- 太乙没有 WiFi，是有线路由，用网线连 LAN 口进后台。
- 插件版首次进 OpenClash / AdGuard Home 前，先确认 WAN 口能上网，
  代理与 DNS 插件需要自己导入订阅 / 配置，本仓库不预置任何订阅。

## 分区与扩容（雅典娜 / 太乙都是 eMMC 机型）

- 原厂 eMMC 分区是 A/B 双槽设计，第三方固件刷完根分区默认不大；
  插件版预装了磁盘管理相关插件，可以在 LuCI 里看 eMMC 剩余空间，
  需要扩容时用分区扩容工具（partexp 类）操作，操作前先备份数据。
- Docker 的数据目录建议放到 eMMC 剩余空间或外接 U 盘，不要挤根分区。

## 常见问题

- **刷完进不了 192.168.10.1**：先确认电脑网线插在 LAN 口、电脑是自动获取 IP；
  再确认刷的固件机型对不对；最后用 TTL / U-Boot 看启动日志。
- **WiFi 搜不到（雅典娜）**：确认刷的是雅典娜固件不是太乙的；
  5G-1 用 160MHz，部分终端不支持会连不上，可在 LuCI 里把 5G-1 降到 80MHz。
- **插件版 Docker 起不来**：雅典娜只有 1GB 内存，Docker + OpenClash + AdGuard Home
  一起跑很吃紧，先在 LuCI 里看内存占用，优先在太乙（2GB）上用 Docker。
- **软件源装不上插件**：先在 LuCI「软件包」里点更新软件包列表；
  本仓库的固件软件源是全的，列表更新失败一般是网络问题，不是源被裁了。
