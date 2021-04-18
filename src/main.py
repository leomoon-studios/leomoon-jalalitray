#-*- coding: utf-8 -*-

import os #open notepad test
import sys
from datetime import datetime
import calendar
import webbrowser #web links
from PyQt5 import QtWidgets, QtCore, QtGui
import resources_rc
import ext.jalali as jalali #https://github.com/mjnaderi/Jalali.py 20140725
from gui.guiMain import Ui_main
if sys.platform.startswith('win'):
    import winreg #startup reg

#version: 1.0.6

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True) #enable highdpi scaling
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True) #use highdpi icons

title = 'LeoMoon JalaliTray'
titlef = 'دگردیس سالنامه پارسی'
ver = '1.0.0'
jYearLst = list(range(1200, 1501))
jYearLst = [str(x) for x in jYearLst]
mYearLst = list(range(1800, 2201))
mYearLst = [str(x) for x in mYearLst]
twentyeight = list(range(1, 28+1))
twentyeight = [str(x) for x in twentyeight]
twentynine = list(range(1, 29+1))
twentynine = [str(x) for x in twentynine]
thirty = list(range(1, 30+1))
thirty = [str(x) for x in thirty]
thirtyone = list(range(1, 31+1))
thirtyone = [str(x) for x in thirtyone]
jDays = ['دوشنبه', 'سه‌شنبه', 'چهارشنبه', 'پنجشنبه', 'جمعه', 'شنبه', 'یکشنبه']
jMonths = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند']
mDays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
mMonths = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        self.sleep = 1 #sleep amount for timer
        self.pDate = "0000-00-00"
        self.cDate = jalali.Gregorian(datetime.now().date()).persian_string()
        self.mainUi = mainUi(self)
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        self.setToolTip(title+' '+ver)
        menu = QtWidgets.QMenu(parent)
        titleAction = menu.addAction(title+' '+ver)
        titleAction.setEnabled(False)
        menu.addSeparator()
        self.dayOfWeek = menu.addAction('')
        self.dayOfWeek.setEnabled(False)
        self.jalaliAction = menu.addAction('Jalali: ')
        self.jalaliAction.setEnabled(False)
        self.miladiAction = menu.addAction('Miladi: ')
        self.miladiAction.setEnabled(False)
        menu.addSeparator()
        converterWin = menu.addAction("Open Date Converter")
        converterWin.triggered.connect(self.converter)
        menu.addSeparator()
        if sys.platform.startswith('win'):
            self.startupMenu = menu.addAction("Start with Windows")
            self.startupMenu.triggered.connect(self.startup)
            self.startupMenu.setCheckable(True)
            try:
                value, regtype = winreg.QueryValueEx(winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run', 0, winreg.KEY_READ), 'LeoMoon JalaliTray')
                self.startupMenu.setChecked(True)
            except Exception as e:
                pass
        websiteAction = menu.addAction("Visit LeoMoon Studios website")
        websiteAction.triggered.connect(self.website)
        exitAction = menu.addAction("Exit")
        exitAction.triggered.connect(self.exit)
        self.setContextMenu(menu)
        self.activated.connect(self.onTrayIcon)
        diag = QtWidgets.QColorDialog()
        self.timer()

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
                if self.mainUi.windowState() == QtCore.Qt.WindowMinimized:
                    self.mainUi.setWindowState(QtCore.Qt.WindowNoState)
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
                #if startup, remove it
                winreg.QueryValueEx(winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'SOFTWARE\\Microsoft\Windows\\CurrentVersion\\Run', 0, winreg.KEY_READ), 'LeoMoon JalaliTray')
                valexists = True
            except:
                pass
            if valexists:
                winreg.DeleteValue(winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'SOFTWARE\\Microsoft\Windows\\CurrentVersion\\Run', 0, winreg.KEY_ALL_ACCESS), 'LeoMoon JalaliTray')
                self.startupMenu.setChecked(False)
            else:
                winreg.SetValueEx(winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\\Microsoft\Windows\\CurrentVersion\\Run', 0, winreg.KEY_ALL_ACCESS), 'LeoMoon JalaliTray', 1, winreg.REG_SZ, '"'+sys.executable+'"')
                self.startupMenu.setChecked(True)

    def converter(self):
        self.mainUi.show()
        if self.mainUi.windowState() == QtCore.Qt.WindowMinimized:
            self.mainUi.setWindowState(QtCore.Qt.WindowNoState)
        self.mainUi.activateWindow()

    def website(self):
        webbrowser.open('http://leomoon.com/', new=2)

    def exit(self):
        self.hide() #hide tray before exiting
        QtCore.QCoreApplication.exit()

    def check(self):
        """check and see if date has changed"""
        self.cDate = jalali.Gregorian(datetime.now().date()).persian_string()
        if self.pDate != self.cDate:
            clean = self.cDate.split('-')
            if len(clean[1]) == 1:
                clean[1] = '0'+clean[1]
            if len(clean[2]) == 1:
                clean[2] = '0'+clean[2]
            self.setToolTip(title+' '+ver+"\n"+datetime.today().strftime("%A")+"\n"+'Jalali: '+clean[0]+'-'+clean[1]+'-'+clean[2]+'\n'+'Miladi: '+str(datetime.now().date()))
            self.trayChange(clean[2])
            self.dayOfWeek.setText(datetime.today().strftime("%A"))
            self.jalaliAction.setText('Jalali: '+clean[0]+'-'+clean[1]+'-'+clean[2])
            self.miladiAction.setText('Miladi: '+str(datetime.now().date()))
            self.pDate = self.cDate
        return self.cDate

    def trayChange(self, day):
        """changes tray icon based on day value of check method"""
        self.setIcon(QtGui.QIcon(":/res/tray/"+day+".svg"))

    def midnight(self):
        """get the number of seconds until midnight"""
        n = datetime.now()
        return ((24 - n.hour - 1) * 60 * 60) + ((60 - n.minute - 1) * 60) + (60 - n.second)

    def timer(self):
        """timer for check function"""
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.check)
        self.timer.setInterval(self.sleep*1000)
        self.timer.start()

class mainUi(QtWidgets.QMainWindow):  #QDialog will only have close button and stay always on top
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, None)  #not on top & it's own process
        #QtWidgets.QWidget.__init__(self, parent) #always on top same parent process
        #self.parent = parent
        #self.sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        #self.sizePolicy.setHeightForWidth(True)
        #self.setSizePolicy(self.sizePolicy)
        self.ui = Ui_main()
        self.ui.setupUi(self)
        #disable resizing
        self.setFixedSize(self.width(), self.height())
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.MSWindowsFixedSizeDialogHint | QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowCloseButtonHint)
        #self.setWindowFlags(QtCore.Qt.Tool) #no taskbar button
        #change text
        self.setWindowTitle(title+' '+ver)
        self.ui.titleLbl.setText(titlef)
        self.ui.titleLbl.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.ui.verLbl.setText('نسخه '+ver)
        self.ui.verLbl.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.ui.copyLbl.setOpenExternalLinks(True)
        self.ui.copyLbl.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.ui.copyLbl.setText('<a style="text-decoration:none; color: inherit;" href="http://leomoon.com">© LeoMoon Studios</a>')
        #set fonts
        self.ui.titleLbl.setFont(QtGui.QFont('Vazir', 15, QtGui.QFont.Black))
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
            self.ui.titleLbl.setFont(QtGui.QFont('Vazir', 20, QtGui.QFont.Black))
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
        self.jalali2miladi(self.ui.jalaliYCbox.currentText(), str(int(self.ui.jalaliMCbox.currentIndex()+1)), self.ui.jalaliDCbox.currentText())

    def jalaliMChange(self):
        self.ui.jalaliDCbox.clear()
        if self.ui.jalaliMCbox.currentIndex() == 11: #29
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

    def jalali2miladi(self, year, month, day):
        iJalali = year+'-'+month+'-'+day
        oMiladi = jalali.Persian(iJalali).gregorian_string()
        oMiladiList = oMiladi.split('-')
        dow = self.dayOfWeek(oMiladi)
        oMiladiFormatted = dow+', '+mMonths[int(oMiladiList[1])-1]+' '+oMiladiList[2]+', '+oMiladiList[0]+self.leap(oMiladiList[0])
        self.ui.j2mLbl.setText(oMiladiFormatted)

    def miladiYChange(self):
        self.miladi2jalali(self.ui.miladiYCbox.currentText(), str(int(self.ui.miladiMCbox.currentIndex()+1)), self.ui.miladiDCbox.currentText())

    def miladiMChange(self):
        self.ui.miladiDCbox.clear()
        if self.ui.miladiMCbox.currentIndex() == 11: #29
            self.ui.miladiDCbox.addItems(twentynine)
        if self.check(self.ui.miladiMCbox.currentIndex(), [6,7,8,9,10]): #30
            self.ui.miladiDCbox.addItems(thirty)
        if self.check(self.ui.miladiMCbox.currentIndex(), [0,1,2,3,4,5]): #31
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
        iMiladi = year+'-'+month+'-'+day
        oJalali = jalali.Gregorian(iMiladi).persian_string()
        oJalaliList = oJalali.split('-')
        dow = self.dayOfWeek(year+'-'+month+'-'+day)
        if dow == 'Monday': dow = jDays[0]
        if dow == 'Tuesday': dow = jDays[1]
        if dow == 'Wednesday': dow = jDays[2]
        if dow == 'Thursday': dow = jDays[3]
        if dow == 'Friday': dow = jDays[4]
        if dow == 'Saturday': dow = jDays[5]
        if dow == 'Sunday': dow = jDays[6]
        oJalaliFormatted = dow+'، '+oJalaliList[2]+' '+jMonths[int(oJalaliList[1])-1]+'، '+oJalaliList[0]+self.kabise(oJalaliList[0])
        self.ui.m2jLbl.setText(oJalaliFormatted)

    def dayOfWeek(self, var):
        return(calendar.day_name[datetime.strptime(var, '%Y-%m-%d').weekday()])

    def leap(self, year):
        if (int(year) % 4 == 0 and int(year) % 100 != 0 or int(year) % 400 == 0):
            return(' (Leap Year)')
        else:
            return(' (Normal Year)')

    def kabise(self, year):
        nums = [1, 5, 9, 13, 17, 22, 26, 30]
        for x in nums:
            if int(year) % 33 == x:
                return (' (سال کبیسه)')
        return (' (سال عادی)')

def main():
    app = QtWidgets.QApplication(sys.argv)
    QtGui.QFontDatabase.addApplicationFont(':/res/fonts/Vazir.ttf') #add custom font no install
    QtGui.QFontDatabase.addApplicationFont(':/res/fonts/Vazir-Black.ttf') #add custom font no install
    QtGui.QFontDatabase.addApplicationFont(':/res/fonts/Vazir-Bold.ttf') #add custom font no install
    QtGui.QFontDatabase.addApplicationFont(':/res/fonts/Vazir-FD.ttf') #add custom font no install
    app.setQuitOnLastWindowClosed(False)
    w = QtWidgets.QWidget()
    trayIcon = SystemTrayIcon(QtGui.QIcon(":/res/tray/00.svg"), w)
    trayIcon.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()