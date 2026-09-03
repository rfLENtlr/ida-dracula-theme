#!/usr/bin/env sh
set -eu

REPO_DIR=$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)
SOURCE_THEME="$REPO_DIR/themes/dracula/theme.css"
ACTION=install

usage()
{
    echo "Usage: $0 [--uninstall] [IDA user directory]" >&2
    exit 2
}

if [ "${1:-}" = "--uninstall" ]; then
    ACTION=uninstall
    shift
fi

[ "$#" -le 1 ] || usage

if [ "$#" -eq 1 ]; then
    TARGET_ROOT=$1
elif [ -n "${IDA_USER_DIR:-}" ]; then
    TARGET_ROOT=$IDA_USER_DIR
elif [ -n "${IDAUSR:-}" ]; then
    # IDAUSR may be a colon-separated search path. Themes are installed into
    # its first writable/user-owned entry, which is also where IDA writes.
    TARGET_ROOT=${IDAUSR%%:*}
else
    TARGET_ROOT=${HOME:?HOME is not set}/.idapro
fi

[ -n "$TARGET_ROOT" ] || { echo "IDA user directory is empty" >&2; exit 2; }

THEME_DIR="$TARGET_ROOT/themes/dracula"
THEME_FILE="$THEME_DIR/theme.css"
BACKUP_FILE="$THEME_DIR/theme.css.pre-dracula-ida-theme"

if [ "$ACTION" = uninstall ]; then
    if [ -f "$BACKUP_FILE" ]; then
        mv -f -- "$BACKUP_FILE" "$THEME_FILE"
        echo "Restored the previous theme: $THEME_FILE"
    elif [ -f "$THEME_FILE" ]; then
        rm -f -- "$THEME_FILE"
        echo "Removed: $THEME_FILE"
    else
        echo "Dracula theme is not installed at: $THEME_FILE"
    fi
    echo "Any user.css overrides were preserved. Restart IDA to refresh themes."
    exit 0
fi

[ -f "$SOURCE_THEME" ] || { echo "Missing source theme: $SOURCE_THEME" >&2; exit 1; }
mkdir -p -- "$THEME_DIR"

if [ -f "$THEME_FILE" ] && ! cmp -s -- "$SOURCE_THEME" "$THEME_FILE" && [ ! -e "$BACKUP_FILE" ]; then
    cp -p -- "$THEME_FILE" "$BACKUP_FILE"
    echo "Backed up the previous theme to: $BACKUP_FILE"
fi

cp -- "$SOURCE_THEME" "$THEME_FILE"
chmod 0644 "$THEME_FILE"

echo "Installed Dracula theme: $THEME_FILE"
echo "Restart IDA, then choose Options -> Colors... -> Current theme -> dracula"
