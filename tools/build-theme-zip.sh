#!/usr/bin/env sh
set -eu

REPO_DIR=$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)
SOURCE_THEME="$REPO_DIR/themes/dracula/theme.css"
OUT_DIR="$REPO_DIR/dist"
ARCHIVE="$OUT_DIR/dracula-ida-theme.zip"

command -v zip >/dev/null 2>&1 || { echo "zip is required" >&2; exit 1; }
command -v unzip >/dev/null 2>&1 || { echo "unzip is required" >&2; exit 1; }
python3 "$REPO_DIR/tools/validate_theme.py"

STAGE=$(mktemp -d /tmp/dracula-ida-theme.XXXXXX)
trap 'rm -rf -- "$STAGE"' EXIT HUP INT TERM

mkdir -p "$STAGE/dracula" "$OUT_DIR"
cp -p "$SOURCE_THEME" "$STAGE/dracula/theme.css"
rm -f -- "$ARCHIVE"

(cd "$STAGE" && zip -DqX "$ARCHIVE" dracula/theme.css)

echo "Built $ARCHIVE"
unzip -l "$ARCHIVE"
