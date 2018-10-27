from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QWidget, QDesktopWidget, QApplication, QFileDialog, QAction
import os
from evaluation_screen import *


class Ui_MainWindow2(object):


    def __init__ (self, curWindow):
        self.curWindow = curWindow
        self.files = ""
        self.file_path = ""

    def openfile_model(self):
        options = QFileDialog.Options()
        name_obj = QFileDialog.getExistingDirectoryUrl(None ,
            "QFileDialog.getOpenFileName()", options=options)
        self.folder_path = name_obj.path()
        if self.folder_path:
            #a first check
            files = os.listdir(self.folder_path)
            if len(files) == 3:
                self.label_model.setText("ok")

    def center(self, window):
        qr = window.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        window.move(qr.topLeft())

    def openfile_video(self):
        options = QFileDialog.Options()
        name_obj = QFileDialog.getOpenFileName(None ,
            "*.npy", options=options)
        self.file_path = name_obj[0]
        if self.file_path.split('.')[1] == "npy":
            self.label_testing.setText("ok")

    def next_screen(self):
        if self.checkBox.isChecked():
            self.files = "models/final_model_001"
            self.file_path = "testing/video1.npy"
            print('loading')
            self.curWindow.close()
            self.window = QtWidgets.QMainWindow()
            self.ui = Ui_MainWindow_Evaluation(self.files, self.file_path )
            self.ui.setup(self.window)
            self.center(self.window)
            self.window.setFixedSize(1280, 805)
            self.window.show()
        else:
            if self.files == "" and self.file_path == "":
                QMessageBox.warning(self.curWindow, "Error", "Wrong load", )
            else:
                print("no default")
                self.files = ""
                self.file_path = ""

    def setup(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(80, 50, 651, 451))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.load_model = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.load_model.setObjectName("load_model")
        self.horizontalLayout_10.addWidget(self.load_model)
        self.label_model = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_model.setObjectName("label_model")
        self.horizontalLayout_10.addWidget(self.label_model, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout.addLayout(self.horizontalLayout_10)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 0)
        self.horizontalLayout.setSpacing(7)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.load_testing = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.load_testing.setObjectName("load_testing")
        self.horizontalLayout.addWidget(self.load_testing)
        self.label_testing = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_testing.setObjectName("label_testing")
        self.horizontalLayout.addWidget(self.label_testing, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(80, 510, 271, 25))
        self.checkBox.setObjectName("checkBox")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(640, 510, 90, 28))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 28))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.load_model.clicked.connect(self.openfile_model)
        self.load_testing.clicked.connect(self.openfile_video)

        self.pushButton.clicked.connect(self.next_screen)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Selection Menu"))
        self.load_model.setText(_translate("MainWindow", "Select a model"))
        self.label_model.setText(_translate("MainWindow", "Pending..."))
        self.load_testing.setText(_translate("MainWindow", "Select the testing video file (.npy)"))
        self.label_testing.setText(_translate("MainWindow", "Pending..."))
        self.checkBox.setText(_translate("MainWindow", "Load default files"))
        self.pushButton.setText(_translate("MainWindow", "NEXT"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

