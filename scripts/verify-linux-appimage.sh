#!/usr/bin/env bash
set -euo pipefail

if (( $# != 3 )); then
    echo "Usage: $0 APPIMAGE VERSION x86_64|arm64" >&2
    exit 2
fi

appimage="$(realpath "$1")"
version="$2"
architecture="$3"
[[ "$architecture" == x86_64 || "$architecture" == arm64 ]] || { echo "Unsupported architecture: $architecture" >&2; exit 2; }
[[ "$(basename "$appimage")" == "leomoon-jalalitray-$version-linux-$architecture.AppImage" ]] || { echo "AppImage filename does not match release metadata" >&2; exit 1; }
[[ -x "$appimage" ]] || { echo "AppImage is not executable" >&2; exit 1; }

work_dir="$(mktemp -d)"
trap 'rm -rf "$work_dir"' EXIT
(
    cd "$work_dir"
    APPIMAGE_EXTRACT_AND_RUN=1 "$appimage" --appimage-extract >/dev/null
)
app_dir="$work_dir/squashfs-root"
required_paths=(
    "AppRun"
    "usr/bin/leomoon-jalalitray"
    "usr/lib/leomoon-jalalitray/LeoMoon JalaliTray"
    "usr/share/applications/com.leomoon.JalaliTray.desktop"
    "usr/share/icons/hicolor/256x256/apps/com.leomoon.JalaliTray.png"
    "usr/share/doc/leomoon-jalalitray/THIRD_PARTY_NOTICES.md"
)
for relative_path in "${required_paths[@]}"; do
    [[ -s "$app_dir/$relative_path" || -x "$app_dir/$relative_path" ]] || { echo "AppImage is missing required file: $relative_path" >&2; exit 1; }
done
grep -qx 'Exec=leomoon-jalalitray' "$app_dir/usr/share/applications/com.leomoon.JalaliTray.desktop"
grep -qx 'Icon=com.leomoon.JalaliTray' "$app_dir/usr/share/applications/com.leomoon.JalaliTray.desktop"
grep -qx 'Categories=Utility;' "$app_dir/usr/share/applications/com.leomoon.JalaliTray.desktop"

expected_architecture="x86-64"
if [[ "$architecture" == arm64 ]]; then expected_architecture="ARM aarch64"; fi
while IFS= read -r binary; do
    file "$binary" | grep -q "$expected_architecture" || { echo "Unexpected architecture: $binary" >&2; exit 1; }
done < <(find "$app_dir/usr/lib/leomoon-jalalitray" -type f \( -name '*.so' -o -name '*.so.*' -o -name 'LeoMoon JalaliTray' \) -print)

echo "Verified self-contained AppImage $appimage"
