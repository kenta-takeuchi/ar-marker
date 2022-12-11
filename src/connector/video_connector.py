import cv2
from cv2 import aruco
import numpy as np
import time
import datetime
import math

from src.models.ar_marker import ArMarkerPoint
from src.config.constants import FRAME, MODE


class VideoConnector:
    def __init__(self, camera_id):
        self.__camera = None
        self.camera_id = camera_id
        try:
            self.connect()
        except Exception:
            print("VideoConnector: Video connection failed.")

    def connect(self):
        if self.__camera is None:
            self.__camera = cv2.VideoCapture(self.camera_id)

    def close(self):
        if self.__camera is not None:
            self.__camera.release()
            cv2.destroyAllWindows()
            self.__camera = None

    def read(self):
        if self.__camera is None:
            return
        ret, frame = self.__camera.read()
        return ret, frame
