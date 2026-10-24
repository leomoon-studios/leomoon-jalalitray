# LeoMoon JalaliTray

## Introduction

LeoMoon JalaliTray is a desktop system tray calendar and date converter. It shows the current Jalali and Gregorian dates, provides clipboard actions for both formats, and opens a converter for Gregorian and Jalali dates.

The application is being modernized as a cross-platform Python and Qt 6 project. It supports Windows, macOS, and Linux with a shared codebase and native release packages for each platform.

## Features

- A system tray menu showing the current Jalali and Gregorian dates.
- Gregorian to Jalali and Jalali to Gregorian date conversion, including age calculation and leap-year information.
- One-click copying of formatted Persian dates, ISO-style Jalali dates, and Gregorian dates.
- Light and dark themes that follow the operating system preference.
- Bundled Vazir fonts and day-specific tray icons.
- A cross-platform **Start at login** option managed from the tray menu.

## Usage

1. Download the package for your computer from the [GitHub releases page](https://github.com/leomoon-studios/leomoon-jalalitray/releases). Windows provides x64 and ARM64 installers, Linux provides x86_64 and ARM64 AppImages, and macOS provides an ARM64 DMG.
2. Open the application. Its calendar icon appears in the system tray.
3. Use the tray menu to copy the displayed Jalali or Gregorian date, open the date converter, change the theme, or enable **Start at login**.
4. In the converter window, select a date in either calendar. The corresponding date, weekday, leap-year information, and age are updated automatically.

## Start at login

Use the tray menu’s **Start at login** option to enable or disable automatic launch for the current user.

- Windows uses the current user’s `HKCU\Software\Microsoft\Windows\CurrentVersion\Run` entry.
- macOS creates `~/Library/LaunchAgents/com.leomoon.JalaliTray.plist`. Copy the application from the DMG to `/Applications` before enabling this option.
- Linux creates `$XDG_CONFIG_HOME/autostart/com.leomoon.JalaliTray.desktop`, falling back to `~/.config/autostart/`. Keep an AppImage in a stable location before enabling this option, because moving it later invalidates the startup entry.

## Build

Requirements:

- Python 3.12 or newer
- A project-local `.venv`
- `uv` installed only inside that `.venv`

From the repository root:

```sh
python -m venv .venv
.venv/bin/python -m pip install "uv==0.13.5"
.venv/bin/uv sync --all-extras --locked
.venv/bin/python scripts/generate_qt.py
QT_QPA_PLATFORM=offscreen .venv/bin/python -m pytest -q
```

Run the application during development with:

```sh
.venv/bin/python -m leomoon_jalalitray
```

On Windows, use `.venv\Scripts\python.exe` in place of `.venv/bin/python`.

## Packaging

Release packages are platform-specific: Windows uses x64 and ARM64 Inno Setup installers, Linux uses x86_64 and ARM64 AppImages, and macOS uses one native ARM64 DMG. Each package is built from the same PyInstaller one-directory application and includes release metadata and SHA-256 checksums.

The platform workflows install the locked dependencies in a project-local `.venv`, regenerate the Qt sources, run Ruff and pytest, build the native bundle, then package and smoke-test the final artifact. Windows and macOS support optional protected signing credentials. Linux AppImage tooling is downloaded with pinned SHA-256 checksums.

## Settings and privacy

Theme and Start at login preferences are controlled locally from the tray menu. The application does not require an account or send calendar conversion data to a network service.

## Remove

Use the normal uninstall method for the installed package. Disable **Start at login** before deleting a macOS application bundle or moving a Linux AppImage, or remove the corresponding per-user startup entry described above.

## Third-party notices

The application includes Qt for Python, DarkDetect, PersianTools, Vazir fonts, and icon assets. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for their notices and licenses.
