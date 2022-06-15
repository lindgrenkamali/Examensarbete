from PyQt5.QtCore import QThread, pyqtSignal
import numpy as np
from ObjectDetection import ObjectDetection
from PhotoManager import PhotoManager

class Worker(QThread):

    ImageUpdate = pyqtSignal(np.ndarray)
    BlackScreen = pyqtSignal()
    UpdateThreshold = pyqtSignal()

    def __init__(self, threshold, mode, file, hsv, displayhsv, window):
        super(Worker, self).__init__()
        self.ThreadActive = True
        self.Threshold = threshold
        self.Mode = mode
        self.File = file
        self.HSV = hsv
        self.ObjectDetection = ObjectDetection(threshold, mode, hsv, displayhsv)
        self.Window = window
        self.PhotoManager = PhotoManager(self.Window)

    def run(self):

        while self.ThreadActive:
            qImage = self.ObjectDetection.detect_objects(self.PhotoManager.capture_screen(), self.File)
            self.ImageUpdate.emit(np.array(qImage))

        self.BlackScreen.emit()

    def stop(self):
        self.ThreadActive = False
        self.quit()