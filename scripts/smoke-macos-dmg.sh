#!/usr/bin/env bash
set -euo pipefail

[[ $# -eq 3 ]] || { echo "Usage: $0 ARTIFACT_DIRECTORY VERSION arm64" >&2; exit 2; }
artifact_dir="$(cd "$1" && pwd)"
version="$2"
architecture="$3"
repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
dmg="$artifact_dir/leomoon-jalalitray-$version-macos-$architecture.dmg"

(cd "$artifact_dir" && shasum -a 256 -c SHA256SUMS)
mount_dir="$(mktemp -d)"
copy_dir="$(mktemp -d)"
device=""
cleanup() { [[ -n "$device" ]] && hdiutil detach "$device" -quiet || true; rm -rf "$mount_dir" "$copy_dir"; }
trap cleanup EXIT
device="$(hdiutil attach -nobrowse -readonly -mountpoint "$mount_dir" "$dmg" | awk '/^\/dev\// {print $1; exit}')"
app="$mount_dir/LeoMoon JalaliTray.app"
bash "$repo_dir/scripts/verify-macos-package.sh" "$app" "$dmg" "$version" "$architecture"
cp -a "$app" "$copy_dir/"
"$copy_dir/LeoMoon JalaliTray.app/Contents/MacOS/LeoMoon JalaliTray" --smoke-test
if grep -q '"signed": true' "$artifact_dir/release-manifest.json"; then spctl --assess --type execute "$copy_dir/LeoMoon JalaliTray.app"; fi
