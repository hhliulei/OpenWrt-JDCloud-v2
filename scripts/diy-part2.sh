#!/usr/bin/env bash
# diy-part2.sh —— 在 feeds update 之后、feeds install 之前做定制。
# 用法（在仓库根目录，源码在 $OPENWRT_DIR，.config 已复制进去）：
#     OPENWRT_DIR=openwrt bash scripts/diy-part2.sh <source> <device> <flavour>
#
# 做的事情（顺序有讲究，和 laipeng668/openwrt-ci-roc 的 Roc-script 一致）：
#  1. 把 Argon 主题 / Argon 配置插件 clone 到 feeds/luci 下面
#     （jerrykuku 的仓库不在默认 feed 里，必须这样补；只在 .config 选了它时才做）
#  2. 雅典娜：把点阵屏插件 clone 到 package/luci-app-athena-led
#  3. 把仓库的 files/ 覆盖层复制进源码树
#  4. 改默认 LAN 地址 192.168.10.1、主机名 ll（改 config_generate）
#  5. 生成 root 密码哈希并写进 files 里那份 99-ll-defaults
#     —— 哈希用 openssl passwd -1 root 在构建期现场生成，
#        仓库里只存占位符 __ROOT_PASSWORD_HASH__，不存明文密码，也不提交哈希。

set -Eeuo pipefail

SOURCE="${1:?用法：diy-part2.sh <source> <device> <flavour>}"
DEVICE="${2:?用法：diy-part2.sh <source> <device> <flavour>}"
FLAVOUR="${3:?用法：diy-part2.sh <source> <device> <flavour>}"
OPENWRT_DIR="${OPENWRT_DIR:-openwrt}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG_FILE="$REPO_ROOT/configs/${SOURCE}-${DEVICE}-${FLAVOUR}.config"

[ -d "$OPENWRT_DIR" ] || { echo "找不到源码目录 $OPENWRT_DIR" >&2; exit 1; }
[ -f "$CONFIG_FILE" ] || { echo "找不到配置文件 $CONFIG_FILE" >&2; exit 1; }

config_enabled() { grep -qx "CONFIG_PACKAGE_$1=y" "$CONFIG_FILE"; }

clone_repo() { # clone_repo <url> <branch> <dest>
    local url="$1" branch="$2" dest="$3"
    rm -rf "$dest"
    git clone --depth 1 --single-branch --branch "$branch" "$url" "$dest"
}

# 1. Argon 主题（所有 20 个版本都用 Argon）
if config_enabled luci-theme-argon; then
    clone_repo https://github.com/jerrykuku/luci-theme-argon.git master \
        "$OPENWRT_DIR/feeds/luci/themes/luci-theme-argon"
fi
if config_enabled luci-app-argon-config; then
    clone_repo https://github.com/jerrykuku/luci-app-argon-config.git master \
        "$OPENWRT_DIR/feeds/luci/applications/luci-app-argon-config"
fi

# 2. 雅典娜点阵屏（太乙没有这块屏，不拉）
if [ "$DEVICE" = "jdcloud_re-cs-02" ]; then
    clone_repo https://github.com/NONGFAH/luci-app-athena-led.git main \
        "$OPENWRT_DIR/package/luci-app-athena-led" \
        || clone_repo https://github.com/NONGFAH/luci-app-athena-led.git master \
            "$OPENWRT_DIR/package/luci-app-athena-led"
fi

# 3. files/ 覆盖层（uci-defaults 等）
if [ -d "$REPO_ROOT/files" ]; then
    mkdir -p "$OPENWRT_DIR/files"
    cp -a "$REPO_ROOT/files/." "$OPENWRT_DIR/files/"
fi

# 4. 默认 LAN 地址与主机名
CFG_GEN="$OPENWRT_DIR/package/base-files/files/bin/config_generate"
sed -i 's/192\.168\.1\.1/192.168.10.1/g' "$CFG_GEN"
sed -i "s/hostname='[^']*'/hostname='ll'/g" "$CFG_GEN"
grep -q "192.168.10.1" "$CFG_GEN" || { echo "config_generate 改 LAN 地址失败" >&2; exit 1; }
grep -q "hostname='ll'" "$CFG_GEN" || { echo "config_generate 改主机名失败" >&2; exit 1; }

# 5. root 密码哈希（构建期现场生成，只写进构建树的 uci-defaults，不提交）
command -v openssl >/dev/null || { echo "找不到 openssl，无法生成密码哈希" >&2; exit 1; }
DEFAULTS="$OPENWRT_DIR/files/etc/uci-defaults/99-ll-defaults"
[ -f "$DEFAULTS" ] || { echo "找不到 $DEFAULTS" >&2; exit 1; }
PASS_HASH="$(openssl passwd -1 root)"
[ -n "$PASS_HASH" ] || { echo "生成密码哈希失败" >&2; exit 1; }
# 用 | 做分隔符，避免哈希里的 / 干扰 sed
sed -i "s|__ROOT_PASSWORD_HASH__|$PASS_HASH|g" "$DEFAULTS"
grep -q "__ROOT_PASSWORD_HASH__" "$DEFAULTS" && { echo "密码占位符替换失败" >&2; exit 1; }

echo "diy-part2 完成：$SOURCE / $DEVICE / $FLAVOUR（LAN 192.168.10.1，主机名 ll）"
