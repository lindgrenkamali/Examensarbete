import cv2
import win32gui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import hsvfilter
from PhotoManager import PhotoManager as pm
from PyQt5 import QtCore, QtWidgets
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from win32api import GetSystemMetrics
from ScreenManager import ScreenManager
from Worker import Worker
from Corner import Corner


class Ui_MainWindow(object):

    def __init__(self, MainWindow):
        super().__init__()
        self.ScreenWidth = GetSystemMetrics(0)
        self.ScreenHeight = GetSystemMetrics(1)

        self.SM = ScreenManager(self.ScreenWidth, self.ScreenWidth)
        self.Corner_x = 0
        self.Corner_y = 0
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.Start_Stop = QtWidgets.QPushButton(self.centralwidget)
        self.ToolButton = QtWidgets.QToolButton(self.centralwidget)
        self.MenuBar = QtWidgets.QMenuBar(MainWindow)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.Corner = Corner(self.Corner_x, self.Corner_y, self.SM, 320, 180)
        self.Screen = QtWidgets.QLabel(self.centralwidget)
        self.Threshold = QtWidgets.QSlider(self.centralwidget)
        self.RadioButton_mode_Default = QtWidgets.QRadioButton(self.centralwidget)
        self.RadioButton_mode_FPS = QtWidgets.QRadioButton(self.centralwidget)
        self.ResolutionBox = QtWidgets.QComboBox(self.centralwidget)
        self.PositionBox = QtWidgets.QComboBox(self.centralwidget)
        self.PlainText = QPlainTextEdit(self.centralwidget)
        self.PlainText.setGeometry(QtCore.QRect(self.SM.GetSize(420), self.SM.GetSize(405),
                                                self.SM.GetSize(300), self.SM.GetSize(50)))
        self.PlainText.setReadOnly(True)
        self.File = ""
        self.H_Min = QtWidgets.QSlider(self.centralwidget)
        self.S_Min = QtWidgets.QSlider(self.centralwidget)
        self.V_Min = QtWidgets.QSlider(self.centralwidget)
        self.H_Max = QtWidgets.QSlider(self.centralwidget)
        self.S_Max = QtWidgets.QSlider(self.centralwidget)
        self.V_Max = QtWidgets.QSlider(self.centralwidget)
        self.S_Add = QtWidgets.QSlider(self.centralwidget)
        self.S_Sub = QtWidgets.QSlider(self.centralwidget)
        self.V_Add = QtWidgets.QSlider(self.centralwidget)
        self.V_Sub = QtWidgets.QSlider(self.centralwidget)
        self.Window = QtWidgets.QComboBox(self.centralwidget)

        self.ResolutionLabel = QtWidgets.QLabel(self.centralwidget)
        self.ThresholdLabel = QtWidgets.QLabel(self.centralwidget)
        self.ModeLabel = QtWidgets.QLabel(self.centralwidget)
        self.FpsLabel = QtWidgets.QLabel(self.centralwidget)
        self.PositionLabel = QtWidgets.QLabel(self.centralwidget)
        self.DefaultLabel = QtWidgets.QLabel(self.centralwidget)
        self.WindowLabel = QtWidgets.QLabel(self.centralwidget)

        self.H_MinLabel = QtWidgets.QLabel(self.centralwidget)
        self.S_MinLabel = QtWidgets.QLabel(self.centralwidget)
        self.V_MinLabel = QtWidgets.QLabel(self.centralwidget)
        self.H_MaxLabel = QtWidgets.QLabel(self.centralwidget)
        self.S_MaxLabel = QtWidgets.QLabel(self.centralwidget)
        self.V_MaxLabel = QtWidgets.QLabel(self.centralwidget)
        self.S_AddLabel = QtWidgets.QLabel(self.centralwidget)
        self.S_SubLabel = QtWidgets.QLabel(self.centralwidget)
        self.V_AddLabel = QtWidgets.QLabel(self.centralwidget)
        self.V_SubLabel = QtWidgets.QLabel(self.centralwidget)

        self.Mode = "Default"

    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(self.SM.GetSize(720), self.SM.GetSize(900))

        self.centralwidget.setObjectName("centralwidget")
        self.set_screen()
        self.set_threshold()
        self.set_radiobuttons()
        self.set_positionbox()
        self.set_resolutionbox()
        self.set_hsv()

        self.WindowLabel.setGeometry(QtCore.QRect(self.SM.GetSize(10), self.SM.GetSize(555),
                                     self.SM.GetSize(160), self.SM.GetSize(16)))

        self.Window.setGeometry(QtCore.QRect(self.SM.GetSize(80), self.SM.GetSize(550),
                                self.SM.GetSize(160), self.SM.GetSize(32)))

        self.Window.addItem("None")
        win32gui.EnumWindows(self.winEnumHandler, None)

        self.Start_Stop.setGeometry(QtCore.QRect(self.SM.GetSize(170), self.SM.GetSize(700),
                                                 self.SM.GetSize(130), self.SM.GetSize(30)))
        self.Start_Stop.setObjectName("StartStop_ObjectDetection")
        self.Start_Stop.clicked.connect(self.startStopButton)
        self.Start_Stop.setEnabled(False)

        self.ToolButton.setGeometry(QtCore.QRect(self.SM.GetSize(10), self.SM.GetSize(700),
                                                 self.SM.GetSize(120), self.SM.GetSize(30)))
        self.ToolButton.setObjectName("toolButton")
        self.ToolButton.clicked.connect(self.get_object)
        MainWindow.setCentralWidget(self.centralwidget)

        self.MenuBar.setGeometry(QtCore.QRect(0, 0, self.SM.GetSize(700), self.SM.GetSize(18)))
        self.MenuBar.setObjectName("menubar")
        MainWindow.setMenuBar(self.MenuBar)

        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def winEnumHandler(self, hwnd, ctx):
        if win32gui.IsWindowVisible(hwnd):
            window = win32gui.GetWindowText(hwnd)
            if window != "":
                self.Window.addItem(win32gui.GetWindowText(hwnd))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ObjectDetection - David SUT20"))
        self.Start_Stop.setText(_translate("MainWindow", "Start"))
        self.ToolButton.setText(_translate("MainWindow", "Choose file"))
        self.ThresholdLabel.setText(_translate("MainWindow", str(self.Threshold.value() / 100)))
        self.ModeLabel.setText(_translate("MainWindow", "Mode:"))
        self.DefaultLabel.setText(_translate("MainWindow", "Default"))
        self.FpsLabel.setText(_translate("MainWindow", "FPS"))
        self.PositionLabel.setText(_translate("MainWindow", "Position:"))
        self.ResolutionLabel.setText(_translate("MainWindow", "Resolution:"))
        self.WindowLabel.setText(_translate("MainWindow", "Window: "))

        self.H_MinLabel.setText(_translate("MainWindow", "H-Min: " + str(self.H_Min.value())))
        self.S_MinLabel.setText(_translate("MainWindow", "S-Min: " + str(self.S_Min.value())))
        self.V_MinLabel.setText(_translate("MainWindow", "V-Min: " + str(self.V_Min.value())))
        self.H_MaxLabel.setText(_translate("MainWindow", "H-Max: " + str(self.H_Max.value())))
        self.S_MaxLabel.setText(_translate("MainWindow", "S-Max: " + str(self.S_Max.value())))
        self.V_MaxLabel.setText(_translate("MainWindow", "V-Max: " + str(self.V_Max.value())))
        self.S_AddLabel.setText(_translate("MainWindow", "S-Add: " + str(self.S_Add.value())))
        self.S_SubLabel.setText(_translate("MainWindow", "S-Sub: " + str(self.S_Sub.value())))
        self.V_AddLabel.setText(_translate("MainWindow", "V-Add: " + str(self.V_Add.value())))
        self.V_SubLabel.setText(_translate("MainWindow", "V-Sub: " + str(self.V_Sub.value())))

    def set_hsv(self):
        self.H_Min.setGeometry(QtCore.QRect(self.SM.GetSize(490), self.SM.GetSize(480),
                                            self.SM.GetSize(200), self.SM.GetSize(16)))

        self.H_Min.setGeometry(QtCore.QRect(self.SM.GetSize(490), self.SM.GetSize(520),
                                            self.SM.GetSize(200), self.SM.GetSize(16)))

        self.S_Min.setGeometry(QtCore.QRect(self.SM.GetSize(490), self.SM.GetSize(560),
                                            self.SM.GetSize(200), self.SM.GetSize(16)))
        self.V_Min.setGeometry(QtCore.QRect(self.SM.GetSize(490), self.SM.GetSize(600),
                                            self.SM.GetSize(200), self.SM.GetSize(16)))
        self.H_Max.setGeometry(QtCore.QRect(self.SM.GetSize(490), self.SM.GetSize(640),
                                            self.SM.GetSize(200), self.SM.GetSize(16)))
        self.S_Max.setGeometry(QtCore.QRect(self.SM.GetSize(490), self.SM.GetSize(680),
                                            self.SM.GetSize(200), self.SM.GetSize(16)))
        self.V_Max.setGeometry(QtCore.QRect(self.SM.GetSize(490), self.SM.GetSize(720),
                                            self.SM.GetSize(200), self.SM.GetSize(16)))
        self.S_Add.setGeometry(QtCore.QRect(self.SM.GetSize(490), self.SM.GetSize(760),
                                            self.SM.GetSize(200), self.SM.GetSize(16)))
        self.S_Sub.setGeometry(QtCore.QRect(self.SM.GetSize(490), self.SM.GetSize(800),
                                            self.SM.GetSize(200), self.SM.GetSize(16)))
        self.V_Add.setGeometry(QtCore.QRect(self.SM.GetSize(490), self.SM.GetSize(840),
                                            self.SM.GetSize(200), self.SM.GetSize(16)))
        self.V_Sub.setGeometry(QtCore.QRect(self.SM.GetSize(490), self.SM.GetSize(880),
                                            self.SM.GetSize(200), self.SM.GetSize(16)))

        self.H_Min.setMaximum(179)
        self.S_Min.setMaximum(255)
        self.V_Min.setMaximum(255)
        self.H_Max.setMaximum(179)
        self.S_Max.setMaximum(255)
        self.V_Max.setMaximum(255)
        self.S_Add.setMaximum(255)
        self.S_Sub.setMaximum(255)
        self.V_Add.setMaximum(255)
        self.V_Sub.setMaximum(255)

        self.H_Max.setValue(179)
        self.S_Max.setValue(255)
        self.V_Max.setValue(255)

        self.H_Min.setOrientation(QtCore.Qt.Horizontal)
        self.S_Min.setOrientation(QtCore.Qt.Horizontal)
        self.V_Min.setOrientation(QtCore.Qt.Horizontal)
        self.H_Max.setOrientation(QtCore.Qt.Horizontal)
        self.S_Max.setOrientation(QtCore.Qt.Horizontal)
        self.V_Max.setOrientation(QtCore.Qt.Horizontal)
        self.S_Add.setOrientation(QtCore.Qt.Horizontal)
        self.S_Sub.setOrientation(QtCore.Qt.Horizontal)
        self.V_Add.setOrientation(QtCore.Qt.Horizontal)
        self.V_Sub.setOrientation(QtCore.Qt.Horizontal)

        self.H_MinLabel.setGeometry(QtCore.QRect(self.SM.GetSize(410), self.SM.GetSize(520),
                                                 self.SM.GetSize(70), self.SM.GetSize(10)))
        self.S_MinLabel.setGeometry(QtCore.QRect(self.SM.GetSize(410), self.SM.GetSize(560),
                                                 self.SM.GetSize(70), self.SM.GetSize(10)))
        self.V_MinLabel.setGeometry(QtCore.QRect(self.SM.GetSize(410), self.SM.GetSize(600),
                                                 self.SM.GetSize(70), self.SM.GetSize(10)))
        self.H_MaxLabel.setGeometry(QtCore.QRect(self.SM.GetSize(410), self.SM.GetSize(640),
                                                 self.SM.GetSize(70), self.SM.GetSize(10)))
        self.S_MaxLabel.setGeometry(QtCore.QRect(self.SM.GetSize(410), self.SM.GetSize(680),
                                                 self.SM.GetSize(70), self.SM.GetSize(10)))
        self.V_MaxLabel.setGeometry(QtCore.QRect(self.SM.GetSize(410), self.SM.GetSize(720),
                                                 self.SM.GetSize(70), self.SM.GetSize(10)))
        self.S_AddLabel.setGeometry(QtCore.QRect(self.SM.GetSize(410), self.SM.GetSize(760),
                                                 self.SM.GetSize(70), self.SM.GetSize(10)))
        self.S_SubLabel.setGeometry(QtCore.QRect(self.SM.GetSize(410), self.SM.GetSize(800),
                                                 self.SM.GetSize(70), self.SM.GetSize(10)))
        self.V_AddLabel.setGeometry(QtCore.QRect(self.SM.GetSize(410), self.SM.GetSize(840),
                                                 self.SM.GetSize(70), self.SM.GetSize(10)))
        self.V_SubLabel.setGeometry(QtCore.QRect(self.SM.GetSize(410), self.SM.GetSize(880),
                                                 self.SM.GetSize(70), self.SM.GetSize(10)))

        self.H_Min.valueChanged.connect(self.update_h_min)
        self.S_Min.valueChanged.connect(self.update_s_min)
        self.V_Min.valueChanged.connect(self.update_v_min)
        self.H_Max.valueChanged.connect(self.update_h_max)
        self.S_Max.valueChanged.connect(self.update_s_max)
        self.V_Max.valueChanged.connect(self.update_v_max)
        self.S_Add.valueChanged.connect(self.update_s_add)
        self.S_Sub.valueChanged.connect(self.update_s_sub)
        self.V_Add.valueChanged.connect(self.update_v_add)
        self.V_Sub.valueChanged.connect(self.update_v_sub)


    def set_screen(self):
        self.Screen.setGeometry(QtCore.QRect(0, 0, self.SM.GetSize(720), self.SM.GetSize(405)))
        self.Screen.setText("")
        self.Screen.setScaledContents(True)
        self.Screen.setObjectName("screen")
        black = QPixmap(16, 16)
        black.fill(Qt.black)
        self.Black = black
        self.Screen.setPixmap(self.Black)

    def set_threshold(self):
        self.Threshold.setGeometry(QtCore.QRect(self.SM.GetSize(10), self.SM.GetSize(450), self.SM.GetSize(160), self.SM.GetSize(16)))
        self.Threshold.setMinimum(40)
        self.Threshold.setMaximum(100)
        self.Threshold.setOrientation(QtCore.Qt.Horizontal)
        self.Threshold.setObjectName("Threshold")
        self.Threshold.valueChanged.connect(self.update_threshold)

        self.ThresholdLabel.setGeometry(QtCore.QRect(self.SM.GetSize(200), self.SM.GetSize(450),
                                                     self.SM.GetSize(160), self.SM.GetSize(16)))
        self.ThresholdLabel.setObjectName("thresholdLabel")

    def set_radiobuttons(self):

        self.ModeLabel.setGeometry(self.SM.GetSize(10), self.SM.GetSize(500), self.SM.GetSize(50), self.SM.GetSize(16))
        self.ModeLabel.setObjectName("modeLabel")

        self.RadioButton_mode_Default.setGeometry(QtCore.QRect(self.SM.GetSize(70), self.SM.GetSize(500),
                                                               self.SM.GetSize(95), self.SM.GetSize(20)))
        self.RadioButton_mode_Default.setChecked(True)
        self.RadioButton_mode_Default.setObjectName("Default")
        self.RadioButton_mode_Default.clicked.connect(self.update_mode)
        self.Mode = self.RadioButton_mode_Default.objectName()

        self.DefaultLabel.setGeometry(QtCore.QRect(self.SM.GetSize(100), self.SM.GetSize(500),
                                                   self.SM.GetSize(50), self.SM.GetSize(16)))
        self.DefaultLabel.setObjectName("defaultLabel")

        self.RadioButton_mode_FPS.setGeometry(QtCore.QRect(self.SM.GetSize(170), self.SM.GetSize(500),
                                                           self.SM.GetSize(95), self.SM.GetSize(20)))
        self.RadioButton_mode_FPS.setObjectName("FPS")
        self.RadioButton_mode_FPS.clicked.connect(self.update_mode)

        self.FpsLabel.setGeometry(QtCore.QRect(self.SM.GetSize(200), self.SM.GetSize(500),
                                               self.SM.GetSize(160), self.SM.GetSize(16)))
        self.FpsLabel.setObjectName("fpsLabel")

    def get_object(self):
        Tk().withdraw()
        filepath = askopenfilename()
        print(filepath)
        if filepath != "":
            self.File = pm.path_to_cvimage(filepath)
            self.PlainText.appendPlainText(filepath)
            self.Start_Stop.setEnabled(True)

    def set_resolutionbox(self):

        self.ResolutionLabel.setGeometry(self.SM.GetSize(10), self.SM.GetSize(655),
                                         self.SM.GetSize(160), self.SM.GetSize(16))

        self.ResolutionBox.setGeometry(self.SM.GetSize(80), self.SM.GetSize(650),
                                       self.SM.GetSize(160), self.SM.GetSize(32))

        self.ResolutionBox.addItem("320 x 180")
        self.ResolutionBox.addItem("640 x 360")
        self.ResolutionBox.addItem("960 x 540")
        self.ResolutionBox.addItem("1024 x 576")
        self.ResolutionBox.addItem("1280 x 720")
        self.ResolutionBox.activated.connect(self.update_resolution)

    def set_positionbox(self):
        self.PositionLabel.setGeometry(QtCore.QRect(self.SM.GetSize(10), self.SM.GetSize(600),
                                                    self.SM.GetSize(160), self.SM.GetSize(16)))
        self.PositionLabel.setObjectName("positionLabel")

        self.PositionBox.addItem("UpperLeft")
        self.PositionBox.addItem("UpperRight")
        self.PositionBox.addItem("LowerLeft")
        self.PositionBox.addItem("LowerRight")
        self.PositionBox.setGeometry(self.SM.GetSize(80), self.SM.GetSize(595),
                                     self.SM.GetSize(160), self.SM.GetSize(32))
        self.PositionBox.activated.connect(self.set_position)

    def set_position(self, index):
        if index == 0:
            self.Corner.x = 0
            self.Corner.y = 0

        elif index == 1:
            self.Corner.x = self.ScreenWidth - self.Corner.Width
            self.Corner.y = 0

        elif index == 2:
            self.Corner.x = 0
            self.Corner.y = self.ScreenHeight - self.Corner.Height

        elif index == 3:
            self.Corner.x = self.ScreenWidth - self.Corner.Width
            self.Corner.y = self.ScreenHeight - self.Corner.Height

        self.Corner.move_window()


    def update_image_slot(self, np):
        self.lastMatch = np
        cvImage = cv2.cvtColor(np, cv2.COLOR_BGR2RGB)
        ConvertToQtFormat = QImage(cvImage.data, cvImage.shape[1], cvImage.shape[0], QImage.Format_RGB888)
        Pic = ConvertToQtFormat.scaled(self.SM.GetSize(640), self.SM.GetSize(360), Qt.KeepAspectRatio)
        Pic = QPixmap.fromImage(Pic)
        self.Screen.setPixmap(Pic)

    def black_screen(self):
        self.Screen.setPixmap(self.Black)

    def startStopButton(self):
        if self.Start_Stop.text() == "Start":
            hsv = hsvfilter.HSVFilter(self.H_Min.value(), self.S_Min.value(), self.V_Min.value(),
                                      self.H_Max.value(), self.S_Max.value(), self.V_Max.value(),
                                      self.S_Add.value(), self.S_Sub.value(), self.V_Add.value(),
                                      self.V_Sub.value())
            self.Corner.show()
            self.Corner.Worker = Worker(self.Threshold.value(), self.Mode, self.File,
                                        hsv, False, self.Window.currentText())
            self.Corner.Worker.start()
            self.Corner.Worker.ImageUpdate.connect(self.Corner.update_image_slot)
            self.Worker = Worker(self.Threshold.value(), self.Mode, self.File, hsv, True,
                                 self.Window.currentText())
            self.Worker.start()
            self.Worker.ImageUpdate.connect(self.update_image_slot)
            self.Worker.BlackScreen.connect(self.black_screen)
            self.Start_Stop.setText("Stop")

        elif self.Start_Stop.text() == "Stop":
            self.Corner.Worker.stop()
            self.Worker.stop()
            self.Start_Stop.setText("Start")
            self.Corner.close()
            cv2.imshow("LastMatch", self.lastMatch)
            cv2.waitKey()

    def update_resolution(self):
        width, height = self.ResolutionBox.currentText().split(" x ")
        self.Corner.Width = int(width)
        self.Corner.Height = int(height)
        self.Corner.setFixedSize(self.Corner.Width, self.Corner.Height)

    def update_threshold(self):
        threshold = self.Threshold.value()
        self.ThresholdLabel.setText(str(threshold / 100))
        self.Worker.ObjectDetection.Threshold = self.Threshold.value() / 100
        self.Corner.Worker.ObjectDetection.Threshold = self.Threshold.value() / 100

    def update_mode(self):
        if self.RadioButton_mode_Default.isChecked():
            self.Mode = "Default"
            self.ToolButton.setEnabled(True)
            self.Threshold.setEnabled(True)
            self.H_Max.setEnabled(True)
            self.S_Max.setEnabled(True)
            self.V_Max.setEnabled(True)
            self.H_Min.setEnabled(True)
            self.S_Min.setEnabled(True)
            self.V_Min.setEnabled(True)
            self.S_Add.setEnabled(True)
            self.S_Sub.setEnabled(True)
            self.V_Add.setEnabled(True)
            self.V_Sub.setEnabled(True)
            if len(self.File):
                self.Start_Stop.setEnabled(True)
            else:
                self.Start_Stop.setEnabled(False)

        elif self.RadioButton_mode_FPS.isChecked():
            self.Mode = "FPS"
            self.ToolButton.setEnabled(False)
            self.Start_Stop.setEnabled(True)
            self.Threshold.setEnabled(False)
            self.H_Max.setEnabled(False)
            self.S_Max.setEnabled(False)
            self.V_Max.setEnabled(False)
            self.H_Min.setEnabled(False)
            self.S_Min.setEnabled(False)
            self.V_Min.setEnabled(False)
            self.S_Add.setEnabled(False)
            self.S_Sub.setEnabled(False)
            self.V_Add.setEnabled(False)
            self.V_Sub.setEnabled(False)


    def update_h_max(self):
        self.H_MaxLabel.setText("H-Max: " + str(self.H_Max.value()))
        self.Worker.HSV.H_Max = self.H_Max.value()

    def update_s_max(self):
        self.S_MaxLabel.setText("S-Max: " + str(self.S_Max.value()))
        self.Worker.HSV.H_Max = self.S_Max.value()

    def update_v_max(self):
        self.V_MaxLabel.setText("V-Max: " + str(self.V_Max.value()))
        self.Worker.HSV.H_Max = self.V_Max.value()

    def update_h_min(self):
        self.H_MinLabel.setText("H-Min: " + str(self.H_Min.value()))
        self.Worker.HSV.H_Min = self.H_Min.value()

    def update_s_min(self):
        self.S_MinLabel.setText("S-Min: " + str(self.S_Min.value()))
        self.Worker.HSV.S_Min = self.S_Min.value()

    def update_v_min(self):
        self.V_MinLabel.setText("V-Min: " + str(self.V_Min.value()))
        self.Worker.HSV.V_Min = self.V_Min.value()

    def update_s_add(self):
        self.S_AddLabel.setText("S-Add: " + str(self.S_Add.value()))
        self.Worker.HSV.S_Add = self.S_Add.value()

    def update_s_sub(self):
        self.S_SubLabel.setText("S-Sub: " + str(self.S_Sub.value()))
        self.Worker.HSV.S_Sub = self.S_Sub.value()

    def update_v_add(self):
        self.V_AddLabel.setText("V-Add: " + str(self.V_Add.value()))
        self.Worker.HSV.V_Add = self.V_Add.value()

    def update_v_sub(self):
        self.V_SubLabel.setText("V-Sub: " + str(self.V_Sub.value()))
        self.Worker.HSV.V_Sub = self.V_Sub.value()


def run_objectdetection():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow(MainWindow)
    ui.setupUi(MainWindow)
    MainWindow.show()

    sys.exit(app.exec_())
