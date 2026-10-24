from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DESKTOP_FILE = PROJECT_ROOT / "packaging" / "linux" / "com.leomoon.JalaliTray.desktop"
PACKAGE_SCRIPT = PROJECT_ROOT / "scripts" / "package-linux.sh"
VERIFY_SCRIPT = PROJECT_ROOT / "scripts" / "verify-linux-appimage.sh"
SMOKE_SCRIPT = PROJECT_ROOT / "scripts" / "smoke-linux-appimage.sh"


def test_linux_desktop_entry_uses_stable_application_metadata() -> None:
    desktop_file = DESKTOP_FILE.read_text(encoding="utf-8")

    assert "Exec=leomoon-jalalitray" in desktop_file
    assert "Icon=com.leomoon.JalaliTray" in desktop_file
    assert "Categories=Utility;" in desktop_file


def test_linux_packaging_requires_pinned_tooling_and_writes_release_artifacts() -> None:
    package_script = PACKAGE_SCRIPT.read_text(encoding="utf-8")

    assert "--appimagetool-sha256" in package_script
    assert "--runtime-sha256" in package_script
    assert "Refusing to replace unsafe artifact directory" in package_script
    assert "release-manifest.json" in package_script
    assert "SHA256SUMS" in package_script
    assert 'architecture" == arm64' in package_script
    assert 'tool_architecture="aarch64"' in package_script


def test_linux_appimage_verifier_checks_layout_architecture_and_tray_smoke_launch() -> None:
    verifier = VERIFY_SCRIPT.read_text(encoding="utf-8")
    smoke_script = SMOKE_SCRIPT.read_text(encoding="utf-8")

    assert "com.leomoon.JalaliTray.desktop" in verifier
    assert "LeoMoon JalaliTray" in verifier
    assert "Unexpected architecture" in verifier
    assert "APPIMAGE_EXTRACT_AND_RUN=1" in smoke_script
    assert "QT_QPA_PLATFORM=offscreen" in smoke_script
    assert "--smoke-test" in smoke_script
