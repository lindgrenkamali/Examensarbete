import PyQt5
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QThread
import sys
from ObjectDetection import ObjectDetection
import keyboard


class ObjectDetectionThread(QThread):
    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        while True:
            ObjectDetection.find_object()


class UI:

    @staticmethod
    def start_ui():
        app = QApplication(sys.argv)
        win = QMainWindow()
        win.setGeometry(200, 200, 300, 300)
        win.setWindowTitle("ObjectDetection")

        button1 = QtWidgets.QPushButton(win)
        button1.setText("Start object detection")
        button1.clicked.connect()
        button1.move(0, 50)

        win.show()
        sys.exit(app.exec_())
