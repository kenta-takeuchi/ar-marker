import cv2
from cv2 import aruco
import numpy as np
import time

from models.ar_marker import ArMarkerPoint


class VideoReader:
    def __init__(self, camera_id):
        self.camera = cv2.VideoCapture(camera_id)

        # aruco設定
        self.ar_marker_ids = [0, 2, 3, 4, 5, 6]
        self.output_path = './read_ar_marker_logs.txt'
        self.dict_aruco = aruco.Dictionary_get(aruco.DICT_4X4_50)
        self.parameters = aruco.DetectorParameters_create()

    def execute(self):
        """
            カメラを起動し、指定したar_marker
        """
        while True:
            markers, frame = self._read_mark_id_points()  # フレームを取得
            cv2.imshow('camera', frame)  # フレームを画面に表示

            # キー操作があればwhileループを抜ける
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # カメラオブジェクトとウィンドウの解放
        self.camera.release()
        cv2.destroyAllWindows()

    def _read_mark_id_points(self):
        """
        静止画を取得し、arucoマークのidリストを取得する
        """
        ret, frame = self.camera.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        corners, ids, rejected_img_points = aruco.detectMarkers(gray, self.dict_aruco, parameters=self.parameters)

        if ids is None:
            return [], frame

        with open(self.output_path, mode='a') as f:
            read_ar_marker_points = []
            read_ids = np.ravel(ids)

            for read_id in read_ids:
                if read_id in self.ar_marker_ids:
                    index = np.where(ids == read_id)[0][0]
                    corner_points = corners[index][0]
                    ar_marker_point = ArMarkerPoint(read_id, corner_points)
                    read_ar_marker_points.append(ar_marker_point)

            read_ar_marker_points = sorted(read_ar_marker_points)
            [f.write(marker.show()) for marker in read_ar_marker_points]

        return read_ar_marker_points, frame
