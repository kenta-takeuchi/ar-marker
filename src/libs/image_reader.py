import cv2
from cv2 import aruco
import numpy as np
import time


class ImageReader:
    dict_aruco = aruco.Dictionary_get(aruco.DICT_4X4_50)
    parameters = aruco.DetectorParameters_create()

    def __init__(self, camera_id):
        self.cap = cv2.VideoCapture(camera_id)

    def get_mark_ids(self):
        ret, frame = self.cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        corners, ids, rejected_img_points = aruco.detectMarkers(gray, dict_aruco, parameters=parameters)

        list_ids = np.ravel(ids)

        return list_ids

    def get_mark_coordinate(self, num_id):
        """
        静止画を取得し、所望のマークの座標を取得する
        """
        ids = self.get_mark_ids()

        if num_id not in np.ravel(ids):
            return None

        index = np.where(ids == num_id)[0][0]  # num_id が格納されているindexを抽出
        corner_ul = corners[index][0][0]
        corner_ur = corners[index][0][1]
        corner_br = corners[index][0][2]
        corner_bl = corners[index][0][3]

        center = [(corner_ul[0] + corner_br[0]) / 2, (corner_ul[1] + corner_br[1]) / 2]

        print('左上 : {}'.format(corner_ul))
        print('右上 : {}'.format(corner_ur))
        print('右下 : {}'.format(corner_br))
        print('左下 : {}'.format(corner_bl))
        print('中心 : {}'.format(center))

        return center
