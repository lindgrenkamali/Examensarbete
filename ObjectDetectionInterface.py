# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ObjectDetectionInterface.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import io

import cv2
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Screenshot import Screenshot as ss
from PyQt5 import QtCore, QtGui, QtWidgets
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from PIL import Image
import numpy as np
from ObjectDetection import ObjectDetection


class CornerWindow(QWidget):
    def __init__(self, x, y):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.run_objectdetection = True
        self.x = 0
        self.y = 0

        self.setLayout(layout)
        self.setFixedSize(320, 180)
        self.move(x, y)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)

        self.screen = QLabel()
        self.Worker = Worker()
        self.Worker.ImageUpdate.connect(self.update_image_slot)
        black = QPixmap(360, 1440)
        black.fill(Qt.black)
        self.screen.setPixmap(black)
        layout.addWidget(self.screen)

    def update_image_slot(self, nparray):
        cvImage = cv2.cvtColor(nparray, cv2.COLOR_RGB2BGR)

        ConvertToQtFormat = QImage(cvImage.data, cvImage.shape[1], cvImage.shape[0], QImage.Format_RGB888)
        Pic = ConvertToQtFormat.scaled(320, 180, Qt.KeepAspectRatio)
        self.screen.setPixmap(QPixmap.fromImage(Pic))

    def move_window(self):
        self.move(self.x, self.y)



class Ui_MainWindow(object):

    def __init__(self):
        super().__init__()
        self.corner_x = 0
        self.corner_y = 0
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.startStop_ObjectDetection = QtWidgets.QPushButton(self.centralwidget)
        self.toolButton = QtWidgets.QToolButton(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.corner = CornerWindow(self.corner_x, self.corner_y)

    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(700, 700)

        self.centralwidget.setObjectName("centralwidget")

        self.setScreen()
        self.setThreshold()
        self.setRadioButtons()
        self.setPositionBox()

        self.startStop_ObjectDetection.setGeometry(QtCore.QRect(170, 600, 131, 31))
        self.startStop_ObjectDetection.setObjectName("StartStop_ObjectDetection")
        self.startStop_ObjectDetection.clicked.connect(self.startStopButton)
        self.startStop_ObjectDetection.setEnabled(False)

        self.toolButton.setGeometry(QtCore.QRect(10, 600, 121, 31))
        self.toolButton.setObjectName("toolButton")
        self.toolButton.clicked.connect(self.get_object)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar.setGeometry(QtCore.QRect(0, 0, 700, 18))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.startStop_ObjectDetection.setText(_translate("MainWindow", "Start"))
        self.toolButton.setText(_translate("MainWindow", "Choose file"))
        self.thresholdLabel.setText(_translate("MainWindow", str(self.threshold.value() / 100)))
        self.modeLabel.setText(_translate("MainWindow", "Mode:"))
        self.defaultLabel.setText(_translate("Main", "Default"))
        self.fpsLabel.setText(_translate("Main", "FPS"))
        self.positionLabel.setText(_translate("Main", "Position:"))

    def setScreen(self):
        self.screen = QtWidgets.QLabel(self.centralwidget)
        self.screen.setGeometry(QtCore.QRect(4, -1, 720, 405))
        self.screen.setText("")
        self.screen.setScaledContents(True)
        self.screen.setObjectName("screen")
        black = QPixmap(16, 16)
        black.fill(Qt.black)
        self.black = black
        self.screen.setPixmap(self.black)

    def setThreshold(self):
        self.threshold = QtWidgets.QSlider(self.centralwidget)
        self.threshold.setGeometry(QtCore.QRect(10, 450, 160, 16))
        self.threshold.setMaximum(100)
        self.threshold.setOrientation(QtCore.Qt.Horizontal)
        self.threshold.setObjectName("Threshold")
        self.threshold.valueChanged.connect(self.update_threshold)
        self.thresholdLabel = QtWidgets.QLabel(self.centralwidget)
        self.thresholdLabel.setGeometry(QtCore.QRect(200, 450, 160, 16))
        self.thresholdLabel.setObjectName("thresholdLabel")

    def setRadioButtons(self):
        self.modeLabel = QtWidgets.QLabel(self.centralwidget)
        self.modeLabel.setGeometry(10, 500, 160, 16)
        self.modeLabel.setObjectName("modeLabel")

        self.radioButton_mode_default = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_mode_default.setGeometry(QtCore.QRect(70, 500, 95, 20))
        self.radioButton_mode_default.setChecked(True)
        self.radioButton_mode_default.setObjectName("Default")
        self.radioButton_mode_default.toggled.connect(self.set_mode)
        self.mode = self.radioButton_mode_default.objectName()

        self.defaultLabel = QtWidgets.QLabel(self.centralwidget)
        self.defaultLabel.setGeometry(QtCore.QRect(100, 500, 160, 16))
        self.defaultLabel.setObjectName("defaultLabel")


        self.radioButton_mode_FPS = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_mode_FPS.setGeometry(QtCore.QRect(170, 500, 95, 20))
        self.radioButton_mode_default.setObjectName("FPS")
        self.fpsLabel = QtWidgets.QLabel(self.centralwidget)
        self.fpsLabel.setGeometry(QtCore.QRect(200, 500, 160, 16))
        self.fpsLabel.setObjectName("fpsLabel")

    def set_mode(self):

        if self.radioButton_mode_default.isChecked():
            self.mode = self.radioButton_mode_default.objectName()
            print("0")

        elif self.radioButton_mode_FPS.isChecked():
            self.mode = self.radioButton_mode_FPS.objectName()
            print("1")


    def get_object(self):
        Tk().withdraw()
        self.objectpath = askopenfilename()
        self.startStop_ObjectDetection.setEnabled(True)

    def setPositionBox(self):

        self.positionLabel = QtWidgets.QLabel(self.centralwidget)
        self.positionLabel.setGeometry(QtCore.QRect(10, 550, 160, 16))
        self.positionLabel.setObjectName("positionLabel")

        self.positionBox = QtWidgets.QComboBox(self.centralwidget)
        self.positionBox.addItem("UpperLeft")
        self.positionBox.addItem("UpperRight")
        self.positionBox.addItem("LowerLeft")
        self.positionBox.addItem("LowerRight")
        self.positionBox.setGeometry(80, 545, 160, 32)
        self.positionBox.activated.connect(self.set_position)

    def set_position(self, index):
        if index == 0:
            self.corner.x = 0
            self.corner.y = 0

        elif index == 1:
            self.corner.x = 1920 - 320
            self.corner.y = 0

        elif index == 2:
            self.corner.x = 0
            self.corner.y = 1080 - 180

        elif index == 3:
            self.corner.x = 1920 - 320
            self.corner.y = 1080 - 180

        self.corner.move_window()


    def update_image_slot(self, nparray):

        cvImage = cv2.cvtColor(nparray, cv2.COLOR_RGB2BGR)

        ConvertToQtFormat = QImage(cvImage.data, cvImage.shape[1], cvImage.shape[0], QImage.Format_RGB888)
        Pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
        self.screen.setPixmap(QPixmap.fromImage(Pic))


    def black_screen(self):
        self.screen.setPixmap(self.black)

    def startStopButton(self):
        if self.startStop_ObjectDetection.text() == "Start":
            self.corner.show()
            self.corner.Worker.start()
            self.objectdetetction = ObjectDetection(self.threshold.value() / 100, self.objectpath)
            self.Worker = Worker()
            self.Worker.start()
            self.Worker.ImageUpdate.connect(self.update_image_slot)
            self.Worker.BlackScreen.connect(self.black_screen)
            self.startStop_ObjectDetection.setText("Stop")

        elif self.startStop_ObjectDetection.text() == "Stop":
            self.Worker.stop()
            self.corner.Worker.stop()
            self.startStop_ObjectDetection.setText("Start")
            self.corner.run_objectdetection = False
            self.corner.close()

    def update_threshold(self):
        self.thresholdLabel.setText(str(self.threshold.value() / 100))

        if hasattr(self, 'objectdetetction'):
            self.objectdetetction.threshold = self.threshold.value() / 100


class Worker(QThread):

    ImageUpdate = pyqtSignal(np.ndarray)
    BlackScreen = pyqtSignal()

    def run(self):
        self.ThreadActive = True

        while self.ThreadActive:
            self.ImageUpdate.emit(ss.capture_screen())

        self.BlackScreen.emit()

    def stop(self):
        self.ThreadActive = False
        self.quit()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
