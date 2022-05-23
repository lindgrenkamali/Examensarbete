import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow

import keyboard as keyboard

from ObjectDetection import ObjectDetection
app = QApplication(sys.argv)
win = QMainWindow()
win.setGeometry(200, 200, 300, 300)
win.setWindowTitle("ObjectDetection")
win.show()

while not (keyboard.is_pressed('§')):

    ObjectDetection.find_object()