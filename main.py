import sys
import multiprocessing
from ObjectDetection import ObjectDetection
from UI import UI
import cv2 as cv
import threading
import keyboard as keyboard
from PhotoManager import Screenshot as ss

nparray = ss.capture_screen()

od = ObjectDetection(0.15, "Default")
od.detect_objects(nparray, 1, 2)

