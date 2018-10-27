# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication
from model_selection import *


class Ui_MainWindow(object):


    def ok(self):
        MainWindow.close()
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow2(self.window)
        self.ui.setup(self.window)
        self.center(self.window)

        sizeObject = QtWidgets.QDesktopWidget().screenGeometry(-1)
        screen_height = sizeObject.height() 
        screen_width =  sizeObject.width()

        window_size = (800,600)

        self.window.setFixedSize(window_size[0], window_size[1])
        self.window.show()

    def center(self, window):

        qr = window.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        window.move(qr.topLeft())


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(892, 662)
        self.center(MainWindow)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(-1, 9, 891, 531))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("images/first_screen.png"))
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(60, 550, 781, 51))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(250, 0, 250, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.startPushButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setStrikeOut(False)
        self.startPushButton.setFont(font)
        self.startPushButton.setMouseTracking(False)
        self.startPushButton.setAutoFillBackground(False)
        self.startPushButton.setObjectName("startPushButton")
        self.startPushButton.clicked.connect(self.ok)
        self.verticalLayout_2.addWidget(self.startPushButton)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 892, 28))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Thesis",
        "Evaluation Tool"))
        self.startPushButton.setText(_translate("MainWindow", "START"))



if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    qss_file = open('style_file.qss').read()
    app.setStyleSheet(qss_file)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    MainWindow.setFixedSize(892, 662)
    sys.exit(app.exec_())




