#!/usr/bin/env bash
set -euo pipefail

if (( $# != 1 )); then
    echo "Usage: $0 APPIMAGE" >&2
    exit 2
fi

appimage="$(realpath "$1")"
[[ -x "$appimage" ]] || { echo "AppImage is not executable: $appimage" >&2; exit 1; }
work_dir="$(mktemp -d)"
trap 'rm -rf "$work_dir"' EXIT
env -i HOME="$work_dir/home" PATH=/usr/bin:/bin TMPDIR="$work_dir" APPIMAGE_EXTRACT_AND_RUN=1 \
    QT_QPA_PLATFORM=offscreen QT_QPA_PLATFORMTHEME='' QT_STYLE_OVERRIDE=Fusion \
    python3 "$(dirname "${BASH_SOURCE[0]}")/smoke_bundle.py" "$appimage"
env -i HOME="$work_dir/home" PATH=/usr/bin:/bin TMPDIR="$work_dir" APPIMAGE_EXTRACT_AND_RUN=1 \
    QT_QPA_PLATFORM=offscreen QT_QPA_PLATFORMTHEME='' QT_STYLE_OVERRIDE=Fusion \
    "$appimage" --smoke-test

echo "Linux AppImage launch and conversion check passed"
