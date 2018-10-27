from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
from PIL import Image
import time
import math

import threading
# from models.final_model_001.multinomal import model_fc_2

def RGB2YUV( rgb ):

    m = np.array([[ 0.29900, -0.16874,  0.50000],
                 [0.58700, -0.33126, -0.41869],
                 [ 0.11400, 0.50000, -0.08131]])

    yuv = np.dot(rgb,m)
    yuv[:,:,1:]+=128.0
    return yuv

sum1 = 91461941044.18457
std_sum1 = 1875687355110.2168

sum2 = 123215856697.59067
std_sum2 = 113146464589.96437

sum3 = 117359336885.57675
std_sum3 = 128011048786.3762

x_sum = 2030407.3156801462
x_std_sum = 4384368263.496551

speed_sum = 2087542.642747879
speed_std_sum = 10022033.821311038

y_sum = -586132.7977940273
y_std_sum = 12510483.537866063

dataset_data_len = 38000

mean1 = sum1 / (dataset_data_len*100*250)
std_1 = math.sqrt(std_sum1/(dataset_data_len*100*250))

mean2 = sum2 / (dataset_data_len*100*250)
std_2 = math.sqrt(std_sum2/(dataset_data_len*100*250))

mean3 = sum3 / (dataset_data_len*100*250)
std_3 = math.sqrt(std_sum3/(dataset_data_len*100*250))

speed_mean = speed_sum / dataset_data_len
speed_std = math.sqrt(speed_std_sum/dataset_data_len)

x_mean = x_sum / dataset_data_len
x_std = math.sqrt(x_std_sum/dataset_data_len)

y_mean = y_sum / dataset_data_len
y_std = math.sqrt(y_std_sum/dataset_data_len)

def normalize_data(screen, telemetry_values):

    HEIGHT = 100
    WIDTH = 250

    screen = np.array(screen)

    screen[...,0] = ( screen[...,0] - mean1 ) / std_1
    screen[...,1] = ( screen[...,1] - mean2 ) / std_2
    screen[...,2] = ( screen[...,2] - mean3 ) / std_3

    #normalize the features
    telemetry_values['speed'] = ( telemetry_values['speed'] - speed_mean ) / speed_std
    telemetry_values['x']  = ( telemetry_values['x'] - x_mean ) / x_std
    telemetry_values['y'] =  ( telemetry_values['y'] - y_mean ) / y_std

    #create the X values (screen with x,y,speed channels)
    X = []
    x_channel = np.zeros( (HEIGHT,WIDTH)  )
    y_channel = np.zeros( (HEIGHT,WIDTH) )
    speed_channel = np.zeros( (HEIGHT,WIDTH) )
    for h in range(HEIGHT):
        for w in range(WIDTH):
            x_channel[h][w] = telemetry_values['x']
            y_channel[h][w] = telemetry_values['y']
            speed_channel[h][w] = telemetry_values['speed']

    temp = np.concatenate( ( screen , np.expand_dims(x_channel,axis=2) ), axis=2 )
    temp = np.concatenate( (temp, np.expand_dims(y_channel,axis=2)), axis=2 )
    temp = np.concatenate( (temp, np.expand_dims(speed_channel,axis=2)), axis=2 )
    X.append(temp)

    X = np.array(X)

    return X



class Ui_MainWindow_Evaluation(object):


    def __init__ (self, model, testing_file):


        self.model = model
        self.testing_file = testing_file


        try:
            pre_load_thread = threading.Thread(target=self.load_model_and_data)
            pre_load_thread.start()
        except (KeyboardInterrupt, SystemExit):
            cleanup_stop_thread()
            sys.exit()



    def load_model_and_data(self):


        #load model
        package = "{}.multinomal".format(self.model.replace("/","."))
        name = "model_fc_2"


        the_model = getattr(__import__(package, fromlist=[name]), name)
        self.model_dnn = the_model(3)
        self.model_dnn.load(str(self.model)+"/model_spirosnet-11340")

        self.label_2.setText("Live Input Data")

        try:
            t1 = threading.Thread(target=self.runLiveOriginalImage)
            t1.start()

        except (KeyboardInterrupt, SystemExit):
            cleanup_stop_thread()
            sys.exit()


    def runLiveOriginalImage(self):

        telemetry_values = {}

        sumA = 0
        sumB = 0
        sumC = 0

        videos = 5
        for j in range(1,videos+1):

            self.testing = np.load(self.testing_file.replace("1", str(j)))

            for i in range(len(self.testing)):

                img = Image.fromarray(self.testing[i][0][:100], 'RGB')
                img.save('current_image.png')

                telemetry_values['x'] = self.testing[i][1]['x']
                telemetry_values['y'] = self.testing[i][1]['y']
                telemetry_values['speed'] = self.testing[i][1]['speed']

                X = normalize_data(self.testing[i][0][:100], telemetry_values)

                game_image = Image.fromarray(X[0][...,:3].astype('uint8'))
                features_image = Image.fromarray(X[0][...,3:].astype('uint8'))

                game_image.save('current_image_norm.png')
                features_image.save('features_image.png')

                self.norm_image.setPixmap(
                    QtGui.QPixmap("current_image_norm.png"))

                self.norm_features.setPixmap(
                    QtGui.QPixmap("features_image.png"))

                self.original_image.setPixmap(
                    QtGui.QPixmap("current_image.png"))

                #real values
                real_steering = self.testing[i][2]['steering']
                real_throttle = self.testing[i][2]['throttle']
                real_braking = self.testing[i][2]['brakes']

                #predicted values
                prediction = self.model_dnn.predict([X.reshape(100,250,6)])[0]

                prediction[0] = - prediction[0]
                prediction[2] = - prediction[2]
                for k in range(3):
                    if prediction[k] > 1:
                        prediction[k] = 1
                    if prediction[k] < -1:
                        prediction[k] = -1

                #set them in the ui
                #sorry for the naming :)
                self.label.setText("Real Steering: " + real_steering)
                self.label_6.setText("Real Throttle: " + real_throttle)
                self.label_8.setText("Real Brakes:" + real_braking)

                self.label_3.setText("Predicted Steering: " + str(prediction[1]))
                self.label_7.setText("Predicted Throttle:" + str(prediction[2]))
                self.label_9.setText("Predicted Brakes:" + str(prediction[0]))

                #differences
                se = abs(float(prediction[1]) - float(real_steering) )
                te = abs(float(prediction[2]) - float(real_throttle))
                be =  abs( float(prediction[0]) - float(real_braking))

                self.label_10.setText("Steering Error: " + str(se) )
                self.label_11.setText("Throttle Error: " + str(te) )
                self.label_12.setText("Braking Error: " + str(be) )

                sumA += se
                sumB += te
                sumC += be

                avgA = se/(i*j+1)
                avgB = te/(i*j+1)
                avgC = be/(i*j+1)

                self.label_13.setText("Mean Error: " + str((avgA+avgB+avgC)/3) )

                time.sleep(0.1)


    def center(self, window):
        qr = window.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        window.move(qr.topLeft())


    def setup(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 805)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.dockWidget_6 = QtWidgets.QDockWidget(self.centralwidget)
        self.dockWidget_6.setMaximumSize(QtCore.QSize(500, 700))
        self.dockWidget_6.setObjectName("dockWidget_6")
        self.dockWidgetContents_10 = QtWidgets.QWidget()
        self.dockWidgetContents_10.setObjectName("dockWidgetContents_10")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.dockWidgetContents_10)
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.dockWidgetContents_10)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_3 = QtWidgets.QLabel(self.dockWidgetContents_10)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.line = QtWidgets.QFrame(self.dockWidgetContents_10)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.label_6 = QtWidgets.QLabel(self.dockWidgetContents_10)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.verticalLayout.addWidget(self.label_6)
        self.label_7 = QtWidgets.QLabel(self.dockWidgetContents_10)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.verticalLayout.addWidget(self.label_7)
        self.line_4 = QtWidgets.QFrame(self.dockWidgetContents_10)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.verticalLayout.addWidget(self.line_4)
        self.label_8 = QtWidgets.QLabel(self.dockWidgetContents_10)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.verticalLayout.addWidget(self.label_8)
        self.label_9 = QtWidgets.QLabel(self.dockWidgetContents_10)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.verticalLayout.addWidget(self.label_9)
        self.line_5 = QtWidgets.QFrame(self.dockWidgetContents_10)
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.verticalLayout.addWidget(self.line_5)
        self.label_10 = QtWidgets.QLabel(self.dockWidgetContents_10)
        self.label_10.setObjectName("label_10")
        self.verticalLayout.addWidget(self.label_10)
        self.label_11 = QtWidgets.QLabel(self.dockWidgetContents_10)
        self.label_11.setObjectName("label_11")
        self.verticalLayout.addWidget(self.label_11)
        self.label_12 = QtWidgets.QLabel(self.dockWidgetContents_10)
        self.label_12.setObjectName("label_12")
        self.verticalLayout.addWidget(self.label_12)
        self.line_6 = QtWidgets.QFrame(self.dockWidgetContents_10)
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.verticalLayout.addWidget(self.line_6)
        self.label_13 = QtWidgets.QLabel(self.dockWidgetContents_10)
        self.label_13.setObjectName("label_13")

        font = QtGui.QFont()
        font.setPointSize(17)
        self.label_13.setFont(font)

        self.verticalLayout.addWidget(self.label_13)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.dockWidget_6.setWidget(self.dockWidgetContents_10)
        self.horizontalLayout_2.addWidget(self.dockWidget_6)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 28))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.dockWidget_4 = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget_4.setObjectName("dockWidget_4")
        self.dockWidgetContents_8 = QtWidgets.QWidget()
        self.dockWidgetContents_8.setObjectName("dockWidgetContents_8")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.dockWidgetContents_8)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.stackedWidget = QtWidgets.QStackedWidget(self.dockWidgetContents_8)
        self.stackedWidget.setMinimumSize(QtCore.QSize(650, 500))
        self.stackedWidget.setMaximumSize(QtCore.QSize(900, 700))
        self.stackedWidget.setFrameShape(QtWidgets.QFrame.Panel)
        self.stackedWidget.setFrameShadow(QtWidgets.QFrame.Plain)
        self.stackedWidget.setLineWidth(1)
        self.stackedWidget.setObjectName("stackedWidget")
        self.inventory = QtWidgets.QWidget()
        self.inventory.setObjectName("inventory")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.inventory)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_2 = QtWidgets.QLabel(self.inventory)
        self.label_2.setMinimumSize(QtCore.QSize(0, 0))
        self.label_2.setMaximumSize(QtCore.QSize(900, 100))
        font = QtGui.QFont()
        font.setPointSize(26)
        self.label_2.setFont(font)
        self.label_2.setScaledContents(False)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_4.addWidget(self.label_2)
        self.label_4 = QtWidgets.QLabel(self.inventory)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_4.addWidget(self.label_4)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(200, -1, 200, -1)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.norm_image = QtWidgets.QLabel(self.inventory)
        self.norm_image.setMinimumSize(QtCore.QSize(0, 50))
        self.norm_image.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.norm_image.setText("")
        self.norm_image.setPixmap(QtGui.QPixmap("../images/wemall.png"))
        self.norm_image.setScaledContents(False)
        self.norm_image.setObjectName("norm_image")
        self.norm_image.setScaledContents(True)
        self.horizontalLayout_4.addWidget(self.norm_image)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setContentsMargins(200, -1, 200, -1)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.norm_features = QtWidgets.QLabel(self.inventory)
        self.norm_features.setMinimumSize(QtCore.QSize(0, 50))
        self.norm_features.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.norm_features.setText("")
        self.norm_features.setPixmap(QtGui.QPixmap("../images/wemall.png"))
        self.norm_features.setScaledContents(False)
        self.norm_features.setScaledContents(True)
        self.norm_features.setObjectName("norm_features")
        self.horizontalLayout_10.addWidget(self.norm_features)
        self.verticalLayout_4.addLayout(self.horizontalLayout_10)
        self.label_5 = QtWidgets.QLabel(self.inventory)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_4.addWidget(self.label_5)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setContentsMargins(200, -1, 200, 20)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.original_image = QtWidgets.QLabel(self.inventory)
        self.original_image.setMinimumSize(QtCore.QSize(0, 50))
        self.original_image.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.original_image.setText("")
        self.original_image.setPixmap(QtGui.QPixmap("../images/welove_original.png"))
        self.original_image.setScaledContents(False)
        self.original_image.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.original_image.setObjectName("original_image")
        self.original_image.setScaledContents(True)
        self.horizontalLayout_9.addWidget(self.original_image)
        self.verticalLayout_4.addLayout(self.horizontalLayout_9)
        self.verticalLayout_4.setStretch(0, 1)
        self.stackedWidget.addWidget(self.inventory)
        self.gridLayout_9.addWidget(self.stackedWidget, 0, 0, 1, 1)
        self.dockWidget_4.setWidget(self.dockWidgetContents_8)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget_4)


        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)



        #self.runLiveEvaluation()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Evaluation Screen"))
        self.label.setText(_translate("MainWindow", "Real Steering: "))
        self.label_3.setText(_translate("MainWindow", "Predicted Steering: "))
        self.label_6.setText(_translate("MainWindow", "Real Throttle:"))
        self.label_7.setText(_translate("MainWindow", "Predicted Throttle:"))
        self.label_8.setText(_translate("MainWindow", "Real Brakes:"))
        self.label_9.setText(_translate("MainWindow", "Predicted Brakes:"))
        self.label_10.setText(_translate("MainWindow", "Steering Error:"))
        self.label_11.setText(_translate("MainWindow", "Throttle Error:"))
        self.label_12.setText(_translate("MainWindow", "Braking Error:"))
        self.label_13.setText(_translate("MainWindow", "Mean Error: "))
        self.label_2.setText(_translate("MainWindow", "Please Wait..."))
        self.label_4.setText(_translate("MainWindow", "Normalized data"))
        self.label_5.setText(_translate("MainWindow", "Original data"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
