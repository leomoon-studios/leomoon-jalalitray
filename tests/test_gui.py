from __future__ import annotations

from datetime import date

from PySide6 import QtCore, QtGui, QtWidgets


def test_converter_window_constructs_with_rolling_year_choices(qapp: QtWidgets.QApplication) -> None:
    import main

    window = main.mainUi()

    assert window.windowTitle() == "LeoMoon JalaliTray 1.0.0"
    assert window.ui.miladiYCbox.itemText(window.ui.miladiYCbox.count() - 1) == str(date.today().year + 100)
    assert int(window.ui.jalaliYCbox.itemText(window.ui.jalaliYCbox.count() - 1)) >= 1500
    window.close()


def test_tray_icon_clipboard_and_theme_actions(qapp: QtWidgets.QApplication) -> None:
    import main

    parent = QtWidgets.QWidget()
    tray = main.SystemTrayIcon(QtGui.QIcon(":/res/tray/01.svg"), parent)

    tray.trayChange("31")
    tray._jalaliCopy()
    assert len(qapp.clipboard().text().split("-")) == 3
    tray._theme()
    tray._theme()
    tray.hide()
    parent.close()


def test_all_embedded_fonts_and_tray_icons_exist(qapp: QtWidgets.QApplication) -> None:
    import main  # noqa: F401

    for font_name in ("Vazir.ttf", "Vazir-Black.ttf", "Vazir-Bold.ttf", "Vazir-FD.ttf"):
        resource = f":/res/fonts/{font_name}"
        assert QtCore.QFile.exists(resource)
        assert QtGui.QFontDatabase.addApplicationFont(resource) != -1
    for day in range(1, 32):
        assert QtCore.QFile.exists(f":/res/tray/{day:02d}.svg")
