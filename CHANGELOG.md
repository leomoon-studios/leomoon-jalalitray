# Changelog

## 2.0.0 (2026-10-24)

- Native release packages for Windows x64 and ARM64, Linux x86_64 and ARM64 AppImages, and macOS ARM64 DMG.
- GitHub Actions builds, package smoke tests, checksums, and tag-driven GitHub releases with linked commit and contributor credits.
- Cross-platform **Start at login** control in the tray menu, using Windows Run entries, macOS LaunchAgents, and Linux XDG autostart entries.
- Regression tests for Jalali and Gregorian calendar conversion, plus UI and startup behavior tests.
- Updated bundled Vazir fonts, including the bold face.
- Documented the tag-driven release process, package naming, signing-secret handling, contribution workflow, and third-party package notices.
- Migrated the application from PyQt5 to PySide6 and Qt 6.
- Moved the application to a standard `src/` package layout with generated Qt sources and modern project metadata.
- Locked maintained Python dependencies in `uv.lock` and updated DarkDetect, PersianTools, PyInstaller, and development tooling.
- Replaced legacy build scripts and bundled compatibility DLLs with deterministic PyInstaller packaging and native platform installers.
- Updated supported systems to current Windows, Linux, and macOS releases.
- Improved Windows installer smoke tests to wait for asynchronous uninstall cleanup.

## 1.0.9 (2024-09-03)

  - Fixed bug when copying Persian date
  - Minor improvement

## 1.0.8 (2022-08-29)

  - Added years old calculation
  - Improved year dropdown to not show future years
  - Improved darkmode

## 1.0.7 (2021-10-05)

  - Added cross-platform auto dark mode
  - Added dark mode toggle in system tray menu
  - Added entires to copy date in system tray menu
  - Fixed issues with Gregorian calendar conversion
  - Updated all dependencies

## 1.0.6 (2021-06-19)

  - Added day of week to tooltip and right click menu

## 1.0.5 (2020-12-19)

  - Fixed compatibility issue with macOS Big Sur
  - Minimum supported macOS has changed to 10.14 Mojave
  - Fixed uninstall icon for Windows setup
  - Updated all dependencies

## 1.0.4 (2020-12-08)

  - Added Start with Windows option to tray menu

## 1.0.3 (2020-05-20)

  - Fixed crash on Windows 10 update 1909
  - Updated all dependencies

## 1.0.2

  - Updated core to the latest version
  - Updated all dependencies
  - Embedded main font into the application
  - Fixed DPI scaling not working sometimes
  - Minimum supported macOS has changed to 10.13

## 1.0.1

  - Minor changes
  - Windows binary is now digitally signed

## 1.0.0

- Initial release
