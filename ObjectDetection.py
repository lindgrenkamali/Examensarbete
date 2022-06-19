import cv2 as cv
import numpy as np
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import uuid
import keyboard

class ObjectDetection:

    def __init__(self, threshold, mode, hsv, displayhsv, returnImg):
        self.Threshold = threshold / 100
        self.Mode = mode
        self.HSV = hsv
        self.DisplayHSV = displayhsv
        self.ReturnImg = returnImg

    def np_to_qimage(self, np, w, h):
        cvImage = cv.cvtColor(np, cv.COLOR_BGR2RGB)
        ConvertToQtFormat = QImage(cvImage.data, cvImage.shape[1], cvImage.shape[0], QImage.Format_RGB888)
        Pic = ConvertToQtFormat.scaled(w, h, Qt.KeepAspectRatio)
        return QPixmap.fromImage(Pic)

    def resize_image(self, image, size):
        w = int(image.shape[1] * size)
        h = int(image.shape[0] * size)
        image = cv.resize(image, (w, h))
        return image

    def get_hsv(self, img):
        hsv = cv.cvtColor(img, cv.COLOR_RGB2HSV)

        h, s, v = cv.split(hsv)

        hsv = cv.merge([h, s, v])

        lowerHSV = np.array([self.HSV.H_Min, self.HSV.S_Min, self.HSV.V_Min])
        upperHSV = np.array([self.HSV.H_Max, self.HSV.S_Max, self.HSV.V_Max])
        maskHSV = cv.inRange(hsv, lowerHSV, upperHSV)

        resultHSV = cv.bitwise_and(hsv, hsv, mask=maskHSV)

        img = cv.cvtColor(resultHSV, cv.COLOR_HSV2RGB)

        return img


    def cascade_detection(self, img):
        cascade_csgo = cv.CascadeClassifier("cascadedata/cascade.xml")
        rectangles = cascade_csgo.detectMultiScale(img)
        return rectangles

    def save_img(self, img):

        if keyboard.is_pressed("+"):
            if keyboard.is_pressed("+"):
                cv.imwrite('PositiveCSGO/{}.jpg'.format(uuid.uuid4()), img)

        elif keyboard.is_pressed("-"):
            if keyboard.is_pressed("-"):
                cv.imwrite('NegativeCSGO/{}.jpg'.format(uuid.uuid4()), img)

        elif self.Mode == "Default" and keyboard.is_pressed("§"):
            if keyboard.is_pressed("§"):
                cv.imwrite('hsvfiles/{}.jpg'.format(uuid.uuid4()), img)

    def draw_rectangles(self, img, rectangles):
        col = (0, 255, 0)
        line_type = cv.LINE_4

        for (x, y, w, h) in rectangles:

            top_left = (x, y)
            bottom_right = (x + w, y + h)

            cv.rectangle(img, top_left, bottom_right, col, 2, line_type)

        return img



    def detect_objects(self, currentImage, object):

        if self.DisplayHSV and self.Mode == "Default":
            currentImage = self.get_hsv(currentImage)

        self.save_img(currentImage)

        currentImage = self.resize_image(currentImage, 0.5)

        objectImage = object

        rgbImg = currentImage


        if self.Mode == "Default":

            objectImage = self.resize_image(objectImage, 0.5)

            result = cv.matchTemplate(cv.cvtColor(currentImage, cv.COLOR_RGB2GRAY), cv.cvtColor(objectImage, cv.COLOR_RGB2GRAY), cv.TM_CCOEFF_NORMED)
            object_w = objectImage.shape[1]
            object_h = objectImage.shape[0]

            results = np.where(result >= self.Threshold)
            locations = list(zip(*results[::-1]))

            rectangles = []
            for l in locations:
                rectangle = [int(l[0]), int(l[1]), object_w, object_h]
                rectangles.append(rectangle)
                rectangles.append(rectangle)

            rectangles, weights = cv.groupRectangles(rectangles, groupThreshold=1, eps=0.5)

            if len(rectangles) and self.ReturnImg:

                return self.draw_rectangles(rgbImg, rectangles), self.ReturnImg

            else:
                return self.draw_rectangles(rgbImg, rectangles), False

        elif self.Mode == "FPS":
            rectangles = self.cascade_detection(rgbImg)

            if len(rectangles) and self.ReturnImg:

                return self.draw_rectangles(rgbImg, rectangles), self.ReturnImg

            else:
                return self.draw_rectangles(rgbImg, rectangles), False

        return rgbImg, False
