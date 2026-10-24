from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = PROJECT_ROOT / ".github" / "workflows"


def test_linux_workflow_builds_both_appimages_with_pinned_actions() -> None:
    workflow = (WORKFLOWS / "linux.yml").read_text(encoding="utf-8")

    assert "ubuntu-24.04-arm" in workflow
    assert '"x86_64","arm64"' in workflow
    assert "APPIMAGETOOL_SHA256" in workflow
    assert "actions/checkout@fbc6f3992d24b796d5a048ff273f7fcc4a7b6c09" in workflow
    assert "actions/upload-artifact@b7c566a772e6b6bfb58ed0dc250532a479d7789f" in workflow
    assert "leomoon-jalalitray-linux-${{ matrix.release_arch }}-release-${{ github.sha }}" in workflow


def test_windows_workflow_builds_both_installers_and_cleans_certificates() -> None:
    workflow = (WORKFLOWS / "windows.yml").read_text(encoding="utf-8")

    assert "windows-11-vs2026-arm" in workflow
    assert '"x64","arm64"' in workflow
    assert "verify-windows-build.ps1" in workflow
    assert "smoke-windows-installer.ps1" in workflow
    assert "if: always()" in workflow
    assert "leomoon-jalalitray-signing.pfx" in workflow
    assert "leomoon-jalalitray-windows-${{ matrix.release_arch }}-release-${{ github.sha }}" in workflow


def test_macos_workflow_builds_only_one_arm64_dmg_and_cleans_keychain() -> None:
    workflow = (WORKFLOWS / "macos.yml").read_text(encoding="utf-8")

    assert "runs-on: macos-15" in workflow
    assert "macos-15-intel" not in workflow
    assert "merge-macos-universal.sh" not in workflow
    assert "package-macos.sh" in workflow
    assert "smoke-macos-dmg.sh" in workflow
    assert "security delete-keychain" in workflow
    assert "if: always()" in workflow
