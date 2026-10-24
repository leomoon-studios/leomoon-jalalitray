#-*- coding: utf-8 -*-

# TODO:

# import os #open notepad test
import os
import sys
#load dlls
dllpath = os.path.dirname(os.path.realpath(sys.argv[0]))
os.environ["PATH"] += os.pathsep + dllpath
os.environ["DYLD_FALLBACK_LIBRARY_PATH"] = dllpath
from datetime import date, datetime
import calendar
import webbrowser #web links
from PySide6 import QtCore, QtGui, QtWidgets
from .calendar_logic import (
    GREGORIAN_MONTHS,
    JALALI_MONTHS,
    JALALI_WEEKDAYS,
    age_years,
    date_to_unpadded_iso,
    gregorian_to_jalali,
    gregorian_year_choices,
    is_gregorian_leap_year,
    is_jalali_leap_year,
    jalali_to_gregorian,
    jalali_weekday,
    jalali_year_choices,
    seconds_until_midnight,
    tray_icon_resource,
    windows_startup_command,
)
from ._generated.main_window import Ui_main
from .version import __version__
from darkdetect import isDark
if sys.platform.startswith('win'):
    import winreg #startup reg

title = 'LeoMoon JalaliTray'
titlef = 'دگردیس سالنامه پارسی'
ver = __version__

mYearLst = gregorian_year_choices()
jYearLst = jalali_year_choices()
twentyeight = list(range(1, 28+1))
twentyeight = [str(x) for x in twentyeight]
twentynine = list(range(1, 29+1))
twentynine = [str(x) for x in twentynine]
thirty = list(range(1, 30+1))
thirty = [str(x) for x in thirty]
thirtyone = list(range(1, 31+1))
thirtyone = [str(x) for x in thirtyone]
jDays = JALALI_WEEKDAYS
jMonths = JALALI_MONTHS
mMonths = GREGORIAN_MONTHS

class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        self.themeFlg = False
        self.sleep = 1 #sleep amount for timer
        self.pDate = "0000-00-00"
        self.cDate = date_to_unpadded_iso(gregorian_to_jalali(datetime.now().date()))
        self.mainUi = mainUi(self)
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        self.setToolTip(title+' '+ver)
        menu = QtWidgets.QMenu(parent)
        titleAction = menu.addAction(title+' '+ver)
        titleAction.setEnabled(False)
        menu.addSeparator()
        jtitleAction = menu.addAction('جلالی')
        jtitleAction.setEnabled(False)
        menu.addSeparator()
        self.jalalifAction = menu.addAction('')
        self.jalalifAction.setFont(QtGui.QFont('Vazir FD', 10))
        self.jalalifAction.triggered.connect(self._jalalifCopy)
        self.jalaliAction = menu.addAction(' :جلالی')
        self.jalaliAction.setFont(QtGui.QFont('Vazir FD', 10))
        self.jalaliAction.triggered.connect(self._jalaliCopy)
        mtitleAction = menu.addAction('میلادی')
        mtitleAction.setEnabled(False)
        menu.addSeparator()
        self.miladifAction = menu.addAction('')
        self.miladifAction.triggered.connect(self._miladifCopy)
        self.miladiAction = menu.addAction('میلادی: ')
        self.miladiAction.triggered.connect(self._miladiCopy)
        # self.miladiAction.setFont(QtGui.QFont('Vazir FD', 10))
        self.miladiAction.triggered.connect(self._miladiCopy)
        menu.addSeparator()
        converterWin = menu.addAction("Open Date Converter")
        converterWin.triggered.connect(self.converter)
        menu.addSeparator()
        if sys.platform.startswith('win'):
            self.startupMenu = menu.addAction("Start with Windows")
            self.startupMenu.triggered.connect(self.startup)
            self.startupMenu.setCheckable(True)
            try:
                #try query startup key. if exists then startup is true
                winreg.QueryValueEx(winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Run', 0, winreg.KEY_READ), 'LeoMoon JalaliTray')
                self.startupMenu.setChecked(True)
            except Exception:
                pass
        ###############################################################################
        ####### Theme startup #########################################################
        ###############################################################################
        self.themeAction = menu.addAction("Dark Mode")
        self.themeAction.triggered.connect(self._theme)
        self.themeAction.setCheckable(True)
        if isDark():
            self.themeFlg = False
            self._theme()
        else:
            self.themeFlg = True
            self._theme()
        websiteAction = menu.addAction("Visit LeoMoon Studios website")
        websiteAction.triggered.connect(self.website)
        exitAction = menu.addAction("Exit")
        exitAction.triggered.connect(self.exit)
        self.setContextMenu(menu)
        self.activated.connect(self.onTrayIcon)
        self.start_timer()

    def _jalalifCopy(self):
        self.cDate = date_to_unpadded_iso(gregorian_to_jalali(datetime.now().date()))
        clean = self.cDate.split('-')
        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.setText(self.dow()+'، '+clean[2]+' '+jMonths[int(clean[1])-1]+' '+clean[0])

    def _jalaliCopy(self):
        self.cDate = date_to_unpadded_iso(gregorian_to_jalali(datetime.now().date()))
        clean = self.cDate.split('-')
        if len(clean[1]) == 1:
            clean[1] = '0'+clean[1]
        if len(clean[2]) == 1:
            clean[2] = '0'+clean[2]
        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.setText(clean[0]+'-'+clean[1]+'-'+clean[2])
        # print(clean[0]+'-'+clean[1]+'-'+clean[2])

    def _miladifCopy(self):
        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.setText(datetime.today().strftime("%A, %d %b, %Y"))
        # print(datetime.today().strftime("%A, %d %b, %Y"))

    def _miladiCopy(self):
        clean2 = str(datetime.now().date()).split('-')
        if len(clean2[1]) == 1:
            clean2[1] = '0'+clean2[1]
        if len(clean2[2]) == 1:
            clean2[2] = '0'+clean2[2]
        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.setText(clean2[0]+'-'+clean2[1]+'-'+clean2[2])
        # print(clean2[0]+'-'+clean2[1]+'-'+clean2[2])

    def onTrayIcon(self, reason):
        if sys.platform.startswith('win'):
            if reason == self.Trigger:
                #if self.mainUi.isVisible(): #no minimize
                #    #self.mainUi.hide()
                #    if self.mainUi.windowState() == QtCore.Qt.WindowActive:
                #        self.mainUi.hide()
                #    else:
                #        self.mainUi.activateWindow()
                #else:
                #    self.mainUi.show()
                if self.mainUi.windowState() == QtCore.Qt.WindowState.WindowMinimized:
                    self.mainUi.setWindowState(QtCore.Qt.WindowState.WindowNoState)
                    self.mainUi.activateWindow()
                elif self.mainUi.isVisible():
                    self.mainUi.hide()
                else:
                    self.mainUi.show()
                    self.mainUi.activateWindow()

    def startup(self):
        if sys.platform.startswith('win'):
            valexists = False
            try:
                winreg.QueryValueEx(winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Run', 0, winreg.KEY_READ), 'LeoMoon JalaliTray')
                valexists = True
            except:
                pass
            if valexists:
                winreg.DeleteValue(winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Run', 0, winreg.KEY_ALL_ACCESS), 'LeoMoon JalaliTray')
                self.startupMenu.setChecked(False)
            else:
                winreg.SetValueEx(winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Run', 0, winreg.KEY_ALL_ACCESS), 'LeoMoon JalaliTray', 0, winreg.REG_SZ, windows_startup_command(sys.executable))
                self.startupMenu.setChecked(True)

    def converter(self):
        self.mainUi.show()
        if self.mainUi.windowState() == QtCore.Qt.WindowState.WindowMinimized:
            self.mainUi.setWindowState(QtCore.Qt.WindowState.WindowNoState)
        self.mainUi.activateWindow()

    def _theme(self):
        if not self.themeFlg:
            dark_theme = QtGui.QPalette()
            dark_theme.setColor(QtGui.QPalette.ColorRole.Window, QtGui.QColor(55,53,53))
            dark_theme.setColor(QtGui.QPalette.ColorRole.WindowText, QtGui.QColor(227,227,227))
            dark_theme.setColor(QtGui.QPalette.ColorRole.Base, QtGui.QColor(30,30,30))
            dark_theme.setColor(QtGui.QPalette.ColorRole.AlternateBase, QtGui.QColor(55,55,55))
            dark_theme.setColor(QtGui.QPalette.ColorRole.ToolTipBase, QtGui.QColor(50,50,50))
            dark_theme.setColor(QtGui.QPalette.ColorRole.ToolTipText, QtGui.QColor(227,227,227))
            dark_theme.setColor(QtGui.QPalette.ColorRole.Text, QtGui.QColor(227,227,227))
            dark_theme.setColor(QtGui.QPalette.ColorRole.Link, QtGui.QColor(227,227,227))
            dark_theme.setColor(QtGui.QPalette.ColorRole.Button, QtGui.QColor(50,50,50))
            dark_theme.setColor(QtGui.QPalette.ColorRole.ButtonText, QtGui.QColor(227,227,227))
            dark_theme.setColor(QtGui.QPalette.ColorRole.BrightText, QtGui.QColor(227,227,227))
            dark_theme.setColor(QtGui.QPalette.ColorRole.Highlight, QtGui.QColor(18,131,220))
            dark_theme.setColor(QtGui.QPalette.ColorRole.HighlightedText, QtCore.Qt.GlobalColor.black)
            dark_theme.setColor(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Button, QtGui.QColor(53, 53, 53))
            dark_theme.setColor(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Button, QtGui.QColor(53, 53, 53))
            dark_theme.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.ButtonText, QtGui.QColor(85,83,83))
            dark_theme.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.WindowText, QtGui.QColor(85,83,83))
            dark_theme.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Text, QtGui.QColor(85,83,83))
            dark_theme.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Light, QtGui.QColor(53, 53, 53))
            QtGui.QGuiApplication.setPalette(dark_theme)
            self.mainUi.setStyleSheet("""
                                        QFrame#banner {background-color: qlineargradient(x1:0 y1:0, x2:0 y2:1, stop:0 #5e5b5b, stop:1 #373535); border-radius: 0px;}
                                        QLabel#titleLbl {color: rgb(227,227,227);}
                                        QLabel#verLbl {color: rgb(227,227,227);}
                                        """)
            self.themeAction.setChecked(True)
        else:
            light_theme = QtGui.QPalette()
            light_theme.setColor(QtGui.QPalette.ColorRole.Window, QtGui.QColor(240,240,240))
            light_theme.setColor(QtGui.QPalette.ColorRole.WindowText, QtGui.QColor(68,68,68))
            light_theme.setColor(QtGui.QPalette.ColorRole.Base, QtGui.QColor(255,255,255))
            light_theme.setColor(QtGui.QPalette.ColorRole.AlternateBase, QtGui.QColor(255,255,255))
            light_theme.setColor(QtGui.QPalette.ColorRole.ToolTipBase, QtGui.QColor(240,240,240))
            light_theme.setColor(QtGui.QPalette.ColorRole.ToolTipText, QtGui.QColor(68,68,68))
            light_theme.setColor(QtGui.QPalette.ColorRole.Text, QtGui.QColor(68,68,68))
            light_theme.setColor(QtGui.QPalette.ColorRole.Link, QtGui.QColor(68,68,68))
            light_theme.setColor(QtGui.QPalette.ColorRole.Button, QtGui.QColor(240,240,240))
            light_theme.setColor(QtGui.QPalette.ColorRole.ButtonText, QtGui.QColor(68,68,68))
            light_theme.setColor(QtGui.QPalette.ColorRole.BrightText, QtGui.QColor(68,68,68))
            light_theme.setColor(QtGui.QPalette.ColorRole.Highlight, QtGui.QColor(18,131,220))
            light_theme.setColor(QtGui.QPalette.ColorRole.HighlightedText, QtCore.Qt.GlobalColor.white)
            light_theme.setColor(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Button, QtGui.QColor(240,240,240))
            light_theme.setColor(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Button, QtGui.QColor(240,240,240))
            light_theme.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.ButtonText, QtGui.QColor(118,118,118))
            light_theme.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.WindowText, QtGui.QColor(118,118,118))
            light_theme.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Text, QtGui.QColor(118,118,118))
            light_theme.setColor(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Light, QtGui.QColor(243,243,243))
            QtGui.QGuiApplication.setPalette(light_theme)
            self.mainUi.setStyleSheet("""
                                        QFrame#banner {background-color: qlineargradient(x1:0 y1:0, x2:0 y2:1, stop:0 #c9c9c9, stop:1 #F0F0F0); border-radius: 0px;}
                                        QLabel#titleLbl {color: rgb(68,68,68);}
                                        QLabel#verLbl {color: rgb(68,68,68);}
                                        """)
            self.themeAction.setChecked(False)
        self.themeFlg = not self.themeFlg

    def website(self):
        webbrowser.open('http://leomoon.com/', new=2)

    def exit(self):
        self.hide() #hide tray before exiting
        QtCore.QCoreApplication.exit()

    def dow(self):
        var = datetime.today().strftime("%A")
        if var == 'Monday': var = jDays[0]
        if var == 'Tuesday': var = jDays[1]
        if var == 'Wednesday': var = jDays[2]
        if var == 'Thursday': var = jDays[3]
        if var == 'Friday': var = jDays[4]
        if var == 'Saturday': var = jDays[5]
        if var == 'Sunday': var = jDays[6]
        return var
        # oJalaliFormatted = dow+'، '+oJalaliList[2]+' '+jMonths[int(oJalaliList[1])-1]+'، '+oJalaliList[0]+self.kabise(oJalaliList[0])
        # self.ui.m2jLbl.setText(oJalaliFormatted)

    def check(self):
        """check and see if date has changed"""
        self.cDate = date_to_unpadded_iso(gregorian_to_jalali(datetime.now().date()))
        if self.pDate != self.cDate:
            clean = self.cDate.split('-')
            self.jalalifAction.setText(self.dow()+'، '+clean[2]+' '+jMonths[int(clean[1])-1]+' '+clean[0])
            self.miladifAction.setText(datetime.today().strftime("%A, %d %b, %Y"))
            if len(clean[1]) == 1:
                clean[1] = '0'+clean[1]
            if len(clean[2]) == 1:
                clean[2] = '0'+clean[2]
            clean2 = str(datetime.now().date()).split('-')
            self.setToolTip(title+' '+ver+"\n\n"+datetime.today().strftime("%A")+' | '+self.dow()+"\n"+'Jalali: '+clean[0]+'-'+clean[1]+'-'+clean[2]+'\n'+'Miladi: '+str(datetime.now().date()))
            self.trayChange(clean[2])
            self.jalaliAction.setText(clean[0]+'-'+clean[1]+'-'+clean[2])
            self.miladiAction.setText(clean2[0]+'-'+clean2[1]+'-'+clean2[2])
            self.pDate = self.cDate
        return self.cDate

    def trayChange(self, day):
        """changes tray icon based on day value of check method"""
        self.setIcon(QtGui.QIcon(tray_icon_resource(int(day))))

    def midnight(self):
        """get the number of seconds until midnight"""
        return seconds_until_midnight()

    def start_timer(self):
        """timer for check function"""
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.check)
        self.timer.setInterval(self.sleep*1000)
        self.timer.start()

class mainUi(QtWidgets.QMainWindow):  #QDialog will only have close button and stay always on top
    def __init__(self, parent=None):
        super().__init__(None)  #not on top & it's own process
        #QtWidgets.QWidget.__init__(self, parent) #always on top same parent process
        #self.parent = parent
        #self.sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        #self.sizePolicy.setHeightForWidth(True)
        #self.setSizePolicy(self.sizePolicy)
        self.ui = Ui_main()
        self.ui.setupUi(self)
        #disable resizing
        self.setFixedSize(self.width(), self.height())
        self.setWindowFlags(QtCore.Qt.WindowType.Window | QtCore.Qt.WindowType.MSWindowsFixedSizeDialogHint | QtCore.Qt.WindowType.WindowMinimizeButtonHint | QtCore.Qt.WindowType.WindowCloseButtonHint)
        #self.setWindowFlags(QtCore.Qt.Tool) #no taskbar button
        self.default_palette = QtGui.QGuiApplication.palette()
        #hotkey
        # self.hotSwitch = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+M"), self)
        # self.hotSwitch.activated.connect(SystemTrayIcon._theme)
        #change text
        self.setWindowTitle(title+' '+ver)
        self.ui.titleLbl.setText(titlef)
        self.ui.titleLbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.ui.verLbl.setText('نسخه '+ver)
        self.ui.verLbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        # self.ui.copyLbl.setOpenExternalLinks(True)
        # self.ui.copyLbl.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.ui.copyLbl.setText('© LeoMoon Studios')
        #set fonts
        self.ui.titleLbl.setFont(QtGui.QFont('Vazir', 15, QtGui.QFont.Weight.Black))
        self.ui.verLbl.setFont(QtGui.QFont('Vazir FD', 10))
        self.ui.copyLbl.setFont(QtGui.QFont('Vazir FD', 10))
        self.ui.statusLbl.setFont(QtGui.QFont('Vazir FD', 10))
        self.ui.jalaliYCbox.addItems(jYearLst)
        self.ui.miladiYCbox.addItems(mYearLst)
        self.ui.jalaliMCbox.currentIndexChanged.connect(self.jalaliMChange)
        self.ui.jalaliYCbox.currentIndexChanged.connect(self.jalaliYChange)
        self.ui.miladiMCbox.currentIndexChanged.connect(self.miladiMChange)
        self.ui.miladiYCbox.currentIndexChanged.connect(self.miladiYChange)
        self.ui.jalaliMCbox.setCurrentIndex(4)
        self.ui.jalaliYCbox.setCurrentIndex(163)
        self.ui.jalaliDCbox.setCurrentIndex(0)
        self.ui.miladiMCbox.setCurrentIndex(6)
        self.ui.miladiYCbox.setCurrentIndex(184)
        self.ui.miladiDCbox.setCurrentIndex(22)
        self.jalali2miladi(self.ui.jalaliYCbox.currentText(), str(int(self.ui.jalaliMCbox.currentIndex()+1)), self.ui.jalaliDCbox.currentText())
        self.miladi2jalali(self.ui.miladiYCbox.currentText(), str(int(self.ui.miladiMCbox.currentIndex()+1)), self.ui.miladiDCbox.currentText())
        self.ui.jalaliDCbox.currentIndexChanged.connect(self.jalaliDChange)
        self.ui.miladiDCbox.currentIndexChanged.connect(self.miladiDChange)
        #platform changes
        if sys.platform.startswith('darwin'): #macos
            self.ui.titleLbl.setFont(QtGui.QFont('Vazir', 20, QtGui.QFont.Weight.Black))
            self.ui.verLbl.setFont(QtGui.QFont('Vazir FD', 13))
            self.ui.copyLbl.setFont(QtGui.QFont('Vazir FD', 13))
            #jalali
            self.ui.jalaliGrp.setFont(QtGui.QFont('Vazir FD', 16))
            self.ui.jalaliYCbox.setFont(QtGui.QFont('Vazir FD', 13))
            self.ui.jalaliMCbox.setFont(QtGui.QFont('Vazir FD', 13))
            self.ui.jalaliDCbox.setFont(QtGui.QFont('Vazir FD', 13))
            self.ui.j2mLbl.setFont(QtGui.QFont('Vazir', 13))
            #miladi
            self.ui.miladiGrp.setFont(QtGui.QFont('Vazir FD', 16))
            self.ui.miladiYCbox.setFont(QtGui.QFont('Vazir', 13))
            self.ui.miladiMCbox.setFont(QtGui.QFont('Vazir', 13))
            self.ui.miladiDCbox.setFont(QtGui.QFont('Vazir', 13))
            self.ui.m2jLbl.setFont(QtGui.QFont('Vazir FD', 13))

    def check(self, val, nums):
        for x in nums:
            if val == x:
                return True
        return False

    def jalaliYChange(self):
        if self.ui.jalaliMCbox.currentIndex() == 11: #29
            if self.kabise(self.ui.jalaliYCbox.currentText())[0]:
                self.ui.jalaliDCbox.clear()
                self.ui.jalaliDCbox.addItems(thirty)
            else:
                self.ui.jalaliDCbox.clear()
                self.ui.jalaliDCbox.addItems(twentynine)
        self.jalali2miladi(self.ui.jalaliYCbox.currentText(), str(int(self.ui.jalaliMCbox.currentIndex()+1)), self.ui.jalaliDCbox.currentText())

    def jalaliMChange(self):
        self.ui.jalaliDCbox.clear()
        if self.ui.jalaliMCbox.currentIndex() == 11: #29
            if self.kabise(self.ui.jalaliYCbox.currentText())[0]:
                self.ui.jalaliDCbox.clear()
                self.ui.jalaliDCbox.addItems(thirty)
            else:
                self.ui.jalaliDCbox.clear()
                self.ui.jalaliDCbox.addItems(twentynine)
        if self.check(self.ui.jalaliMCbox.currentIndex(), [6,7,8,9,10]): #30
            self.ui.jalaliDCbox.addItems(thirty)
        if self.check(self.ui.jalaliMCbox.currentIndex(), [0,1,2,3,4,5]): #31
            self.ui.jalaliDCbox.addItems(thirtyone)
        self.jalali2miladi(self.ui.jalaliYCbox.currentText(), str(int(self.ui.jalaliMCbox.currentIndex()+1)), self.ui.jalaliDCbox.currentText())

    def jalaliDChange(self):
        self.jDayVal = ''
        if self.ui.jalaliDCbox.currentText() == '':
            self.jDayVal = '1'
        else:
            self.jDayVal = self.ui.jalaliDCbox.currentText()
        self.jalali2miladi(self.ui.jalaliYCbox.currentText(), str(int(self.ui.jalaliMCbox.currentIndex()+1)), self.jDayVal)

    def calculateAge(self, born):
        return str(age_years(born.date()))

    def jalali2miladi(self, year, month, day):
        oMiladi = date_to_unpadded_iso(jalali_to_gregorian(int(year), int(month), int(day)))
        oMiladiList = oMiladi.split('-')
        dow = self.dayOfWeek(oMiladi)
        oMiladiFormatted = dow+', '+mMonths[int(oMiladiList[1])-1]+' '+oMiladiList[2]+', '+oMiladiList[0]+self.leap(oMiladiList[0])[1]
        self.ui.j2mLbl.setText(oMiladiFormatted + ': ' + self.calculateAge(datetime(int(oMiladiList[0]), int(oMiladiList[1]), int(oMiladiList[2]))) + " years old")

    def miladiYChange(self):
        if self.ui.miladiMCbox.currentIndex() == 1: #29
            if self.leap(self.ui.miladiYCbox.currentText())[0]:
                self.ui.miladiDCbox.clear()
                self.ui.miladiDCbox.addItems(twentynine)
            else:
                self.ui.miladiDCbox.clear()
                self.ui.miladiDCbox.addItems(twentyeight)
        self.miladi2jalali(self.ui.miladiYCbox.currentText(), str(int(self.ui.miladiMCbox.currentIndex()+1)), self.ui.miladiDCbox.currentText())

    def miladiMChange(self):
        self.ui.miladiDCbox.clear()
        if self.ui.miladiMCbox.currentIndex() == 1: #29
            if self.leap(self.ui.miladiYCbox.currentText())[0]:
                self.ui.miladiDCbox.clear()
                self.ui.miladiDCbox.addItems(twentynine)
            else:
                self.ui.miladiDCbox.clear()
                self.ui.miladiDCbox.addItems(twentyeight)
        if self.check(self.ui.miladiMCbox.currentIndex(), [3,5,8,10]): #30
            self.ui.miladiDCbox.addItems(thirty)
        if self.check(self.ui.miladiMCbox.currentIndex(), [0,2,4,6,7,9,11]): #31
            self.ui.miladiDCbox.addItems(thirtyone)
        self.miladi2jalali(self.ui.miladiYCbox.currentText(), str(int(self.ui.miladiMCbox.currentIndex()+1)), self.ui.miladiDCbox.currentText())

    def miladiDChange(self):
        self.mDayVal = ''
        if self.ui.miladiDCbox.currentText() == '':
            self.mDayVal = '1'
        else:
            self.mDayVal = self.ui.miladiDCbox.currentText()
        self.miladi2jalali(self.ui.miladiYCbox.currentText(), str(int(self.ui.miladiMCbox.currentIndex()+1)), self.mDayVal)

    def miladi2jalali(self, year, month, day):
        converted_date = date(int(year), int(month), int(day))
        oJalali = date_to_unpadded_iso(gregorian_to_jalali(converted_date))
        oJalaliList = oJalali.split('-')
        dow = jalali_weekday(converted_date)
        oJalaliFormatted = dow+'، '+oJalaliList[2]+' '+jMonths[int(oJalaliList[1])-1]+'، '+oJalaliList[0]+self.kabise(oJalaliList[0])[1]
        self.ui.m2jLbl.setText(oJalaliFormatted + ': ' + self.calculateAge(datetime(int(year), int(month), int(day))) + " ساله")

    def dayOfWeek(self, var):
        return(calendar.day_name[datetime.strptime(var, '%Y-%m-%d').weekday()])

    def leap(self, year):
        if is_gregorian_leap_year(int(year)):
            return(True, ' (Leap Year)')
        else:
            return(False, ' (Normal Year)')

    def kabise(self, year):
        if is_jalali_leap_year(int(year)):
            return (True, ' (سال کبیسه)')
        return (False, ' (سال عادی)')

def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    QtGui.QFontDatabase.addApplicationFont(':/res/fonts/Vazir.ttf') #add custom font no install
    QtGui.QFontDatabase.addApplicationFont(':/res/fonts/Vazir-Black.ttf') #add custom font no install
    QtGui.QFontDatabase.addApplicationFont(':/res/fonts/Vazir-Bold.ttf') #add custom font no install
    QtGui.QFontDatabase.addApplicationFont(':/res/fonts/Vazir-FD.ttf') #add custom font no install
    app.setQuitOnLastWindowClosed(False)
    w = QtWidgets.QWidget()
    trayIcon = SystemTrayIcon(QtGui.QIcon(":/res/tray/00.svg"), w)
    trayIcon.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
