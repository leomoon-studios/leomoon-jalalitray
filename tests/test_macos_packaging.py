from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INFO_PLIST = PROJECT_ROOT / "packaging" / "macos" / "Info.plist.in"
PACKAGE_SCRIPT = PROJECT_ROOT / "scripts" / "package-macos.sh"
VERIFY_SCRIPT = PROJECT_ROOT / "scripts" / "verify-macos-package.sh"
SMOKE_SCRIPT = PROJECT_ROOT / "scripts" / "smoke-macos-dmg.sh"


def test_macos_bundle_metadata_is_native_arm64_only() -> None:
    info_plist = INFO_PLIST.read_text(encoding="utf-8")
    verifier = VERIFY_SCRIPT.read_text(encoding="utf-8")

    assert "LeoMoon JalaliTray" in info_plist
    assert "com.leomoon.JalaliTray" in info_plist
    assert "LSMinimumSystemVersion</key><string>12.0" in info_plist
    assert "Application is not ARM64-only" in verifier
    assert '"$architectures" == arm64' in verifier


def test_macos_packaging_uses_a_single_native_dmg_with_optional_signing_and_notarization() -> None:
    package_script = PACKAGE_SCRIPT.read_text(encoding="utf-8")

    assert '"$architecture" == arm64' in package_script
    assert "JALALITRAY_MACOS_CODESIGN_IDENTITY" in package_script
    assert "JALALITRAY_MACOS_NOTARY_PROFILE" in package_script
    assert "xcrun stapler staple" in package_script
    assert "leomoon-jalalitray-$version-macos-$architecture.dmg" in package_script
    assert "lipo -create" not in package_script


def test_macos_dmg_smoke_script_mounts_copies_and_runs_packaged_conversion_check() -> None:
    smoke_script = SMOKE_SCRIPT.read_text(encoding="utf-8")

    assert "hdiutil attach" in smoke_script
    assert "cp -a" in smoke_script
    assert "--smoke-test" in smoke_script
    assert "spctl --assess" in smoke_script
