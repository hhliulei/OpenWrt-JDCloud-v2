#!/usr/bin/env bash
# build.sh —— 本地编译（和 GitHub Actions 走同一套脚本，方便本机复现）。
# 用法：
#     bash build.sh <source> <device> <flavour>
#     bash build.sh immortalwrt jdcloud_re-cs-02 pure
#     bash build.sh ppe jdcloud_re-cs-07 plus
# source: immortalwrt | libwrt | openwrt | ppe | ppe-immwrt
# device: jdcloud_re-cs-02 | jdcloud_re-cs-07
# flavour: pure | plus
#
# 5 个源码 × 2 机型 × 2 版本 = 20 个固件。ppe / ppe-immwrt 两条 PPE 路线属实验性质。
#
# 产物在 openwrt/bin/targets/qualcommax/ipq60xx/，以及 artifacts/<source>-<device>-<flavour>/。
# 注意：首次全编在 4 核机器上约 1-2 小时，磁盘至少留 30GB 空闲。

set -Eeuo pipefail

SOURCE="${1:?用法：build.sh <source> <device> <flavour>}"
DEVICE="${2:?用法：build.sh <source> <device> <flavour>}"
FLAVOUR="${3:?用法：build.sh <source> <device> <flavour>}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OPENWRT_DIR="${OPENWRT_DIR:-$REPO_ROOT/openwrt}"
JOBS="${JOBS:-$(nproc)}"

case "$SOURCE" in
    immortalwrt) REPO_URL="https://github.com/laipeng668/immortalwrt.git"; REPO_BRANCH="openwrt-25.12" ;;
    libwrt)      REPO_URL="https://github.com/LiBwrt/openwrt-6.x.git";    REPO_BRANCH="25.12-nss" ;;
    openwrt)     REPO_URL="https://github.com/openwrt/openwrt.git";       REPO_BRANCH="main" ;;  # 25.12 分支无 jdcloud 机型
    ppe)         REPO_URL="https://github.com/JuliusBairaktaris/openwrt-ppe-nss.git"; REPO_BRANCH="ppe-nss" ;;  # 实验：PPE+NSS，IPQ60xx 未经作者实测
    ppe-immwrt)  REPO_URL="https://github.com/VIKINGYFY/immortalwrt.git"; REPO_BRANCH="owrt" ;;  # 实验：ImmortalWrt 底 PPE
    *) echo "未知 source：$SOURCE" >&2; exit 1 ;;
esac

CONFIG_FILE="$REPO_ROOT/configs/${SOURCE}-${DEVICE}-${FLAVOUR}.config"
[ -f "$CONFIG_FILE" ] || { echo "找不到配置文件 $CONFIG_FILE" >&2; exit 1; }

echo "==> 源码：$REPO_URL（$REPO_BRANCH）"
if [ -d "$OPENWRT_DIR/.git" ]; then
    echo "复用已克隆的源码：$OPENWRT_DIR"
else
    git clone --depth 1 --single-branch --branch "$REPO_BRANCH" "$REPO_URL" "$OPENWRT_DIR"
fi

echo "==> diy-part1：追加插件 feed"
OPENWRT_DIR="$OPENWRT_DIR" bash "$REPO_ROOT/scripts/diy-part1.sh" "$SOURCE" "$DEVICE" "$FLAVOUR"

echo "==> 复制 .config"
cp "$CONFIG_FILE" "$OPENWRT_DIR/.config"

cd "$OPENWRT_DIR"
echo "==> feeds update"
./scripts/feeds update -a

echo "==> diy-part2：Argon / athena-led / 默认值 / 密码哈希"
OPENWRT_DIR="$OPENWRT_DIR" bash "$REPO_ROOT/scripts/diy-part2.sh" "$SOURCE" "$DEVICE" "$FLAVOUR"

echo "==> feeds install"
./scripts/feeds install -a

echo "==> defconfig + 机型校验"
make defconfig
grep -q "CONFIG_TARGET_qualcommax_ipq60xx_DEVICE_${DEVICE}=y" .config \
    || { echo "错误：defconfig 后 .config 里没有机型 $DEVICE，可能是机型符号与上游 Kconfig 不一致（见 SOURCES.md）" >&2; exit 1; }

echo "==> 下载源码包"
make download -j"$JOBS"

echo "==> 编译（失败自动降为单线程详细日志重试一次）"
make -j"$JOBS" || make -j1 V=s

echo "==> 收集产物"
ARTIFACTS="$REPO_ROOT/artifacts/${SOURCE}-${DEVICE}-${FLAVOUR}"
mkdir -p "$ARTIFACTS"
cp bin/targets/qualcommax/ipq60xx/*"${DEVICE}"* "$ARTIFACTS/" 2>/dev/null || true
cp bin/targets/qualcommax/ipq60xx/*.manifest "$ARTIFACTS/" 2>/dev/null || true
cp .config "$ARTIFACTS/Config-${SOURCE}-${DEVICE}-${FLAVOUR}.txt"
(cd "$ARTIFACTS" && sha256sum -- * > sha256sums.txt)
echo "完成：$ARTIFACTS"
ls -la "$ARTIFACTS"
