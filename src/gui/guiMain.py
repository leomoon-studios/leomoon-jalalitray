# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'guiMain.ui'
##
## Created by: Qt User Interface Compiler version 6.12.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QMainWindow,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)
import resources_rc

class Ui_main(object):
    def setupUi(self, main):
        if not main.objectName():
            main.setObjectName(u"main")
        main.resize(451, 385)
        main.setMinimumSize(QSize(451, 385))
        main.setMaximumSize(QSize(451, 385))
        icon = QIcon()
        icon.addFile(u":/res/icons/main.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        main.setWindowIcon(icon)
        main.setStyleSheet(u"QFrame#banner {background-color: qlineargradient(x1:0 y1:0, x2:0 y2:1, stop:0 #c9c9c9, stop:1 #F0F0F0); border-radius: 0px;}\n"
"QLabel#titleLbl {color: rgb(68,68,68);}\n"
"QLabel#verLbl {color: rgb(68,68,68);}")
        self.centralwidget = QWidget(main)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.banner = QFrame(self.centralwidget)
        self.banner.setObjectName(u"banner")
        self.banner.setMinimumSize(QSize(0, 81))
        self.banner.setMaximumSize(QSize(16777215, 81))
        self.banner.setLayoutDirection(Qt.RightToLeft)
        self.banner.setFrameShape(QFrame.NoFrame)
        self.banner.setFrameShadow(QFrame.Raised)
        self.banner.setLineWidth(0)
        self.horizontalLayout = QHBoxLayout(self.banner)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer = QSpacerItem(11, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.logoLbl = QLabel(self.banner)
        self.logoLbl.setObjectName(u"logoLbl")
        self.logoLbl.setMinimumSize(QSize(61, 61))
        self.logoLbl.setMaximumSize(QSize(61, 61))
        self.logoLbl.setPixmap(QPixmap(u":/res/icons/main.svg"))
        self.logoLbl.setScaledContents(True)

        self.horizontalLayout.addWidget(self.logoLbl)

        self.horizontalSpacer_2 = QSpacerItem(11, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.titleFrm = QFrame(self.banner)
        self.titleFrm.setObjectName(u"titleFrm")
        self.titleFrm.setFrameShape(QFrame.NoFrame)
        self.titleFrm.setFrameShadow(QFrame.Raised)
        self.titleFrm.setLineWidth(0)
        self.verticalLayout_2 = QVBoxLayout(self.titleFrm)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalSpacer = QSpacerItem(20, 18, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.titleLbl = QLabel(self.titleFrm)
        self.titleLbl.setObjectName(u"titleLbl")
        self.titleLbl.setMaximumSize(QSize(16777215, 25))
        font = QFont()
        font.setFamilies([u"Vazir"])
        font.setPointSize(15)
        font.setBold(True)
        font.setStyleStrategy(QFont.PreferAntialias)
        self.titleLbl.setFont(font)
        self.titleLbl.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout_2.addWidget(self.titleLbl)

        self.verLbl = QLabel(self.titleFrm)
        self.verLbl.setObjectName(u"verLbl")
        font1 = QFont()
        font1.setFamilies([u"Vazir FD"])
        font1.setPointSize(10)
        font1.setStyleStrategy(QFont.PreferAntialias)
        self.verLbl.setFont(font1)
        self.verLbl.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout_2.addWidget(self.verLbl)

        self.verticalSpacer_2 = QSpacerItem(20, 18, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)


        self.horizontalLayout.addWidget(self.titleFrm)


        self.verticalLayout.addWidget(self.banner)

        self.contentFrm = QFrame(self.centralwidget)
        self.contentFrm.setObjectName(u"contentFrm")
        self.contentFrm.setFrameShape(QFrame.NoFrame)
        self.contentFrm.setFrameShadow(QFrame.Raised)
        self.contentFrm.setLineWidth(0)
        self.verticalLayout_3 = QVBoxLayout(self.contentFrm)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.jalaliGrp = QGroupBox(self.contentFrm)
        self.jalaliGrp.setObjectName(u"jalaliGrp")
        font2 = QFont()
        font2.setFamilies([u"Vazir FD"])
        font2.setPointSize(12)
        font2.setStyleStrategy(QFont.PreferAntialias)
        self.jalaliGrp.setFont(font2)
        self.jalaliGrp.setLayoutDirection(Qt.RightToLeft)
        self.jalaliGrp.setAlignment(Qt.AlignCenter)
        self.jalaliGrp.setFlat(False)
        self.verticalLayout_5 = QVBoxLayout(self.jalaliGrp)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(-1, 5, -1, -1)
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.jalaliDCbox = QComboBox(self.jalaliGrp)
        self.jalaliDCbox.setObjectName(u"jalaliDCbox")
        self.jalaliDCbox.setMinimumSize(QSize(0, 30))
        self.jalaliDCbox.setFont(font1)
        self.jalaliDCbox.setLayoutDirection(Qt.LeftToRight)

        self.horizontalLayout_3.addWidget(self.jalaliDCbox)

        self.jalaliMCbox = QComboBox(self.jalaliGrp)
        self.jalaliMCbox.addItem("")
        self.jalaliMCbox.addItem("")
        self.jalaliMCbox.addItem("")
        self.jalaliMCbox.addItem("")
        self.jalaliMCbox.addItem("")
        self.jalaliMCbox.addItem("")
        self.jalaliMCbox.addItem("")
        self.jalaliMCbox.addItem("")
        self.jalaliMCbox.addItem("")
        self.jalaliMCbox.addItem("")
        self.jalaliMCbox.addItem("")
        self.jalaliMCbox.addItem("")
        self.jalaliMCbox.setObjectName(u"jalaliMCbox")
        self.jalaliMCbox.setMinimumSize(QSize(0, 30))
        self.jalaliMCbox.setFont(font1)
        self.jalaliMCbox.setLayoutDirection(Qt.RightToLeft)

        self.horizontalLayout_3.addWidget(self.jalaliMCbox)

        self.jalaliYCbox = QComboBox(self.jalaliGrp)
        self.jalaliYCbox.setObjectName(u"jalaliYCbox")
        self.jalaliYCbox.setMinimumSize(QSize(0, 30))
        self.jalaliYCbox.setFont(font1)
        self.jalaliYCbox.setLayoutDirection(Qt.LeftToRight)

        self.horizontalLayout_3.addWidget(self.jalaliYCbox)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)

        self.j2mLbl = QLabel(self.jalaliGrp)
        self.j2mLbl.setObjectName(u"j2mLbl")
        font3 = QFont()
        font3.setFamilies([u"Vazir"])
        font3.setPointSize(10)
        font3.setStyleStrategy(QFont.PreferAntialias)
        self.j2mLbl.setFont(font3)
        self.j2mLbl.setAlignment(Qt.AlignCenter)

        self.verticalLayout_4.addWidget(self.j2mLbl)


        self.verticalLayout_5.addLayout(self.verticalLayout_4)


        self.verticalLayout_3.addWidget(self.jalaliGrp)

        self.miladiGrp = QGroupBox(self.contentFrm)
        self.miladiGrp.setObjectName(u"miladiGrp")
        self.miladiGrp.setFont(font2)
        self.miladiGrp.setLayoutDirection(Qt.RightToLeft)
        self.miladiGrp.setAlignment(Qt.AlignCenter)
        self.miladiGrp.setFlat(False)
        self.gridLayout = QGridLayout(self.miladiGrp)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(9, 5, -1, -1)
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.miladiDCbox = QComboBox(self.miladiGrp)
        self.miladiDCbox.setObjectName(u"miladiDCbox")
        self.miladiDCbox.setMinimumSize(QSize(0, 30))
        self.miladiDCbox.setFont(font3)
        self.miladiDCbox.setLayoutDirection(Qt.LeftToRight)

        self.horizontalLayout_4.addWidget(self.miladiDCbox)

        self.miladiMCbox = QComboBox(self.miladiGrp)
        self.miladiMCbox.addItem("")
        self.miladiMCbox.addItem("")
        self.miladiMCbox.addItem("")
        self.miladiMCbox.addItem("")
        self.miladiMCbox.addItem("")
        self.miladiMCbox.addItem("")
        self.miladiMCbox.addItem("")
        self.miladiMCbox.addItem("")
        self.miladiMCbox.addItem("")
        self.miladiMCbox.addItem("")
        self.miladiMCbox.addItem("")
        self.miladiMCbox.addItem("")
        self.miladiMCbox.setObjectName(u"miladiMCbox")
        self.miladiMCbox.setMinimumSize(QSize(0, 30))
        self.miladiMCbox.setFont(font3)
        self.miladiMCbox.setLayoutDirection(Qt.LeftToRight)

        self.horizontalLayout_4.addWidget(self.miladiMCbox)

        self.miladiYCbox = QComboBox(self.miladiGrp)
        self.miladiYCbox.setObjectName(u"miladiYCbox")
        self.miladiYCbox.setMinimumSize(QSize(0, 30))
        self.miladiYCbox.setFont(font3)
        self.miladiYCbox.setLayoutDirection(Qt.LeftToRight)

        self.horizontalLayout_4.addWidget(self.miladiYCbox)


        self.verticalLayout_6.addLayout(self.horizontalLayout_4)

        self.m2jLbl = QLabel(self.miladiGrp)
        self.m2jLbl.setObjectName(u"m2jLbl")
        self.m2jLbl.setFont(font1)
        self.m2jLbl.setAlignment(Qt.AlignCenter)

        self.verticalLayout_6.addWidget(self.m2jLbl)


        self.gridLayout.addLayout(self.verticalLayout_6, 0, 0, 1, 1)


        self.verticalLayout_3.addWidget(self.miladiGrp)


        self.verticalLayout.addWidget(self.contentFrm)

        self.statusFrm = QFrame(self.centralwidget)
        self.statusFrm.setObjectName(u"statusFrm")
        self.statusFrm.setMinimumSize(QSize(0, 31))
        self.statusFrm.setMaximumSize(QSize(16777215, 31))
        font4 = QFont()
        font4.setFamilies([u"Vazir"])
        font4.setPointSize(10)
        self.statusFrm.setFont(font4)
        self.statusFrm.setFrameShape(QFrame.NoFrame)
        self.statusFrm.setFrameShadow(QFrame.Raised)
        self.statusFrm.setLineWidth(0)
        self.horizontalLayout_2 = QHBoxLayout(self.statusFrm)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(9, 0, 9, 0)
        self.statusLbl = QLabel(self.statusFrm)
        self.statusLbl.setObjectName(u"statusLbl")
        self.statusLbl.setFont(font3)

        self.horizontalLayout_2.addWidget(self.statusLbl)

        self.copyLbl = QLabel(self.statusFrm)
        self.copyLbl.setObjectName(u"copyLbl")
        self.copyLbl.setMinimumSize(QSize(150, 0))
        self.copyLbl.setMaximumSize(QSize(131, 16777215))
        self.copyLbl.setFont(font3)
        self.copyLbl.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.copyLbl)


        self.verticalLayout.addWidget(self.statusFrm)

        main.setCentralWidget(self.centralwidget)

        self.retranslateUi(main)

        QMetaObject.connectSlotsByName(main)
    # setupUi

    def retranslateUi(self, main):
        main.setWindowTitle(QCoreApplication.translate("main", u"MainWindow", None))
        self.logoLbl.setText("")
        self.titleLbl.setText(QCoreApplication.translate("main", u"Title", None))
        self.verLbl.setText(QCoreApplication.translate("main", u"1.0.0", None))
        self.jalaliGrp.setTitle(QCoreApplication.translate("main", u"\u062c\u0644\u0627\u0644\u06cc \u0628\u0647 \u0645\u06cc\u0644\u0627\u062f\u06cc", None))
        self.jalaliMCbox.setItemText(0, QCoreApplication.translate("main", u"\u0641\u0631\u0648\u0631\u062f\u06cc\u0646", None))
        self.jalaliMCbox.setItemText(1, QCoreApplication.translate("main", u"\u0627\u0631\u062f\u06cc\u0628\u0647\u0634\u062a", None))
        self.jalaliMCbox.setItemText(2, QCoreApplication.translate("main", u"\u062e\u0631\u062f\u0627\u062f", None))
        self.jalaliMCbox.setItemText(3, QCoreApplication.translate("main", u"\u062a\u06cc\u0631", None))
        self.jalaliMCbox.setItemText(4, QCoreApplication.translate("main", u"\u0645\u0631\u062f\u0627\u062f", None))
        self.jalaliMCbox.setItemText(5, QCoreApplication.translate("main", u"\u0634\u0647\u0631\u06cc\u0648\u0631", None))
        self.jalaliMCbox.setItemText(6, QCoreApplication.translate("main", u"\u0645\u0647\u0631", None))
        self.jalaliMCbox.setItemText(7, QCoreApplication.translate("main", u"\u0622\u0628\u0627\u0646", None))
        self.jalaliMCbox.setItemText(8, QCoreApplication.translate("main", u"\u0622\u0630\u0631", None))
        self.jalaliMCbox.setItemText(9, QCoreApplication.translate("main", u"\u062f\u06cc", None))
        self.jalaliMCbox.setItemText(10, QCoreApplication.translate("main", u"\u0628\u0647\u0645\u0646", None))
        self.jalaliMCbox.setItemText(11, QCoreApplication.translate("main", u"\u0627\u0633\u0641\u0646\u062f", None))

        self.j2mLbl.setText(QCoreApplication.translate("main", u"TextLabel", None))
        self.miladiGrp.setTitle(QCoreApplication.translate("main", u"\u0645\u06cc\u0644\u0627\u062f\u06cc \u0628\u0647 \u062c\u0644\u0627\u0644\u06cc", None))
        self.miladiMCbox.setItemText(0, QCoreApplication.translate("main", u"January", None))
        self.miladiMCbox.setItemText(1, QCoreApplication.translate("main", u"February", None))
        self.miladiMCbox.setItemText(2, QCoreApplication.translate("main", u"March", None))
        self.miladiMCbox.setItemText(3, QCoreApplication.translate("main", u"April", None))
        self.miladiMCbox.setItemText(4, QCoreApplication.translate("main", u"May", None))
        self.miladiMCbox.setItemText(5, QCoreApplication.translate("main", u"June", None))
        self.miladiMCbox.setItemText(6, QCoreApplication.translate("main", u"July", None))
        self.miladiMCbox.setItemText(7, QCoreApplication.translate("main", u"August", None))
        self.miladiMCbox.setItemText(8, QCoreApplication.translate("main", u"September", None))
        self.miladiMCbox.setItemText(9, QCoreApplication.translate("main", u"October", None))
        self.miladiMCbox.setItemText(10, QCoreApplication.translate("main", u"November", None))
        self.miladiMCbox.setItemText(11, QCoreApplication.translate("main", u"December", None))

        self.m2jLbl.setText(QCoreApplication.translate("main", u"TextLabel", None))
        self.statusLbl.setText("")
        self.copyLbl.setText(QCoreApplication.translate("main", u"\u00a9 LeoMoon Studios", None))
    # retranslateUi
