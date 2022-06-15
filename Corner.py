import cv2
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QVBoxLayout, QLabel
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Corner(QWidget):
    def __init__(self, x, y, sm, width, height):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.run_objectdetection = True
        self.SM = sm
        self.x = 0
        self.y = 0
        self.setLayout(layout)
        self.Width = width
        self.Height = height
        self.setFixedSize(self.Width, self.Height)
        self.move(x, y)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)

        self.Screen = QLabel()
        black = QPixmap(1280, 720)
        black.fill(Qt.black)
        self.Screen.setPixmap(black)
        layout.addWidget(self.Screen)

    def update_image_slot(self, np):
        cvImage = cv2.cvtColor(np, cv2.COLOR_BGR2RGB)
        ConvertToQtFormat = QImage(cvImage.data, cvImage.shape[1], cvImage.shape[0], QImage.Format_RGB888)
        Pic = ConvertToQtFormat.scaled(self.Width, self.Height, Qt.KeepAspectRatio)
        Pic = QPixmap.fromImage(Pic)
        self.Screen.setPixmap(Pic)

    def move_window(self):
        self.move(self.x, self.y)