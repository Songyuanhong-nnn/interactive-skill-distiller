#!/usr/bin/env bash
# 安装 interactive-skill-distiller 到 WorkBuddy skills 目录
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NAME="interactive-skill-distiller"
DEST="${1:-$HOME/.workbuddy/skills}"

# 安全校验：拒绝明显危险的目标路径
case "$DEST" in
  ""|"/"|"."|".."|"$HOME"|"$HOME/")
    echo "[!] 目标路径不安全或为空：$DEST" >&2
    echo "    请传入一个具体的 skills 目录，或省略使用默认值" >&2
    exit 2 ;;
esac

mkdir -p "$DEST"

if [ -e "$DEST/$NAME" ]; then
  BACKUP="$DEST/$NAME.bak.$(date +%Y%m%d%H%M%S)"
  mv "$DEST/$NAME" "$BACKUP"
  echo "[i] 旧版本已备份 -> $BACKUP"
fi

cp -R "$SRC" "$DEST/$NAME"
rm -f "$DEST/$NAME/install.sh" "$DEST/$NAME/install.ps1"

echo "[+] 已安装 -> $DEST/$NAME"
echo "    重启会话或重新索引后生效"
