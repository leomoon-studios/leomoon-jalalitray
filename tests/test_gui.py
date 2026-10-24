from __future__ import annotations

from datetime import date

from PyQt5 import QtGui, QtWidgets


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
