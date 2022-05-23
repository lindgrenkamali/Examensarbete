import mss
import numpy as np


class Screenshot:
    @staticmethod
    def capture_screen():
        with mss.mss() as mss_instance:
            monitor_1 = mss_instance.monitors[1]
            screenshot = np.array(mss_instance.grab(monitor_1))
            return screenshot
