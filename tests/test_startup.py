from __future__ import annotations

import plistlib
from pathlib import Path


def test_linux_startup_toggle_uses_xdg_autostart_and_the_external_appimage(monkeypatch, tmp_path: Path) -> None:
    from leomoon_jalalitray import startup

    monkeypatch.setattr(startup.sys, "platform", "linux")
    environment = {"XDG_CONFIG_HOME": str(tmp_path / "config"), "APPIMAGE": "/opt/LeoMoon/JalaliTray.AppImage"}
    startup.set_enabled(True, home=tmp_path, environment=environment)

    path = startup.linux_autostart_path(tmp_path, environment)
    assert startup.is_enabled(tmp_path, environment)
    assert 'Exec="/opt/LeoMoon/JalaliTray.AppImage"' in path.read_text(encoding="utf-8")

    startup.set_enabled(False, home=tmp_path, environment=environment)
    assert not path.exists()


def test_macos_startup_toggle_writes_a_per_user_launch_agent(monkeypatch, tmp_path: Path) -> None:
    from leomoon_jalalitray import startup

    monkeypatch.setattr(startup.sys, "platform", "darwin")
    monkeypatch.setattr(startup.sys, "frozen", True, raising=False)
    monkeypatch.setattr(startup.sys, "executable", "/Applications/LeoMoon JalaliTray.app/Contents/MacOS/LeoMoon JalaliTray")
    startup.set_enabled(True, home=tmp_path)

    path = startup.macos_launch_agent_path(tmp_path)
    agent = plistlib.loads(path.read_bytes())
    assert agent["Label"] == "com.leomoon.JalaliTray"
    assert agent["ProgramArguments"] == [startup.sys.executable]
    assert agent["RunAtLoad"] is True


def test_start_at_login_menu_is_available_on_every_supported_platform(qapp) -> None:
    from leomoon_jalalitray import app

    window = app.mainUi()
    tray = app.SystemTrayIcon(window.windowIcon(), window)
    assert tray.startupMenu.text() == "Start at login"
    tray.hide()
    window.close()
