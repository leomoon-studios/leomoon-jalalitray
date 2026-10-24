"""Per-user start-at-login integration for supported desktop platforms."""

from __future__ import annotations

import os
import plistlib
import subprocess
import sys
from pathlib import Path


APPLICATION_NAME = "LeoMoon JalaliTray"
APPLICATION_ID = "com.leomoon.JalaliTray"
WINDOWS_RUN_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"


def command_arguments(executable: str | None = None, environment: dict[str, str] | None = None) -> list[str]:
    """Return a persistent command for the installed or development application."""
    executable = executable or sys.executable
    environment = environment or os.environ
    if sys.platform.startswith("linux"):
        return [environment.get("APPIMAGE", executable)]
    if getattr(sys, "frozen", False):
        return [executable]
    return [executable, "-m", "leomoon_jalalitray"]


def linux_autostart_path(home: Path | None = None, environment: dict[str, str] | None = None) -> Path:
    home = home or Path.home()
    environment = environment or os.environ
    config_home = Path(environment.get("XDG_CONFIG_HOME", home / ".config"))
    return config_home / "autostart" / f"{APPLICATION_ID}.desktop"


def macos_launch_agent_path(home: Path | None = None) -> Path:
    return (home or Path.home()) / "Library" / "LaunchAgents" / f"{APPLICATION_ID}.plist"


def is_enabled(home: Path | None = None, environment: dict[str, str] | None = None) -> bool:
    if sys.platform.startswith("win"):
        import winreg

        try:
            winreg.QueryValueEx(winreg.OpenKey(winreg.HKEY_CURRENT_USER, WINDOWS_RUN_KEY, 0, winreg.KEY_READ), APPLICATION_NAME)
            return True
        except FileNotFoundError:
            return False
    if sys.platform == "darwin":
        return macos_launch_agent_path(home).is_file()
    if sys.platform.startswith("linux"):
        return linux_autostart_path(home, environment).is_file()
    return False


def set_enabled(enabled: bool, home: Path | None = None, environment: dict[str, str] | None = None) -> None:
    arguments = command_arguments(environment=environment)
    if sys.platform.startswith("win"):
        import winreg

        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, WINDOWS_RUN_KEY, 0, winreg.KEY_ALL_ACCESS)
        if enabled:
            winreg.SetValueEx(key, APPLICATION_NAME, 0, winreg.REG_SZ, f'"{arguments[0]}"')
        else:
            try:
                winreg.DeleteValue(key, APPLICATION_NAME)
            except FileNotFoundError:
                pass
        return
    if sys.platform == "darwin":
        path = macos_launch_agent_path(home)
        if enabled:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(plistlib.dumps({"Label": APPLICATION_ID, "ProgramArguments": arguments, "RunAtLoad": True}))
        else:
            subprocess.run(["launchctl", "bootout", f"gui/{os.getuid()}", str(path)], check=False, capture_output=True)
            path.unlink(missing_ok=True)
        return
    if sys.platform.startswith("linux"):
        path = linux_autostart_path(home, environment)
        if enabled:
            path.parent.mkdir(parents=True, exist_ok=True)
            quoted = " ".join(f'"{item.replace("\\", "\\\\").replace(chr(34), "\\\"")}"' for item in arguments)
            path.write_text(f"[Desktop Entry]\nType=Application\nName={APPLICATION_NAME}\nExec={quoted}\nTerminal=false\nX-GNOME-Autostart-enabled=true\n", encoding="utf-8")
        else:
            path.unlink(missing_ok=True)
