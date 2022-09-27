import numpy as np
import cv2 as cv
import win32gui, win32ui, win32con
from threading import Lock
lock = Lock()


class PhotoManager:

    def __init__(self, window):
        self.Window = window

    def capture_screen(self):

        lock.acquire()

        w = 1920
        h = 1080

        hwnd = win32gui.FindWindow(None, self.Window)

        wDC = win32gui.GetWindowDC(hwnd)

        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()

        dataBitMap.CreateCompatibleBitmap(dcObj, w, h)

        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (w, h), dcObj, (0, 0), win32con.SRCCOPY)

        signedIntsArray = dataBitMap.GetBitmapBits(True)
        window = np.fromstring(signedIntsArray, dtype='uint8')
        window.shape = (h, w, 4)

        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        lock.release()

        window = window[...,:3]
        window = np.ascontiguousarray(window)

        return window

    @staticmethod
    def path_to_cvimage(filepath):
        return cv.imdecode(np.fromfile(filepath, dtype=np.uint8), cv.IMREAD_UNCHANGED)
