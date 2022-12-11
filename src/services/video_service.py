import cv2
from cv2 import aruco
import numpy as np
import time
import datetime
import math

from src.config.constants import FRAME, MODE, POINT
from src.models.ar_marker import ArMarkerPoint
from src.services.loggiing_service import LoggingService


class VideoService:
    __available_point_counts = [1, 4]
    __ar_marker_ids = [0, 2, 3, 4, 5, 6]
    __dict_aruco = aruco.Dictionary_get(aruco.DICT_APRILTAG_36h11)
    __parameters = aruco.DetectorParameters_create()

    @classmethod
    def execute(cls, video_connector, mode):
        markers, frame = cls._read_mark_id_points(video_connector)
        cls._display_frame(frame)  # フレームを画面に表示

        if mode == MODE["initialize"]:
            if cls._is_available_point_counts(markers):
                command, point_w = self._get_command_by_ar_marker_points(markers)
                cv2.putText(
                    frame,
                    point_w,
                    FRAME['POSITION'],
                    FRAME['FONT'],
                    FRAME['FONT_SCALE'],
                    FRAME['FONT_COLOR'],
                    3,
                    cv2.LINE_AA,
                    True
                )
                return command

        return None

    @classmethod
    def _read_mark_id_points(cls, video_connector):
        """
        静止画を取得し、arucoマークのidリストを取得する
        """
        frame, corners, ids = cls._read_capture(video_connector)
        if ids is None:
            return [], frame

        read_ids = np.ravel(ids)
        if not self._is_available_point_counts(read_ids):
            return [], frame

        read_ar_marker_points = self._build_read_ar_marker_points(read_ids, corners)

        return read_ar_marker_points, frame

    def _get_command_by_ar_marker_points(self, read_ar_marker_points):
        """読み取ったar_markerのidに応じてシリアル通信を送信する"""
        if len(read_ar_marker_points) == 1:
            command, point_w = self._get_command_when_single_ar_marker_id(read_ar_marker_points[0])
            return command, point_w
        if len(read_ar_marker_points) == 4:
            command, point_w = self._send_serial_when_multi_ar_marker_points(read_ar_marker_points)
            return command, point_w

        return '', ''

    @classmethod
    def _read_capture(cls, video_connector):
        ret, frame = video_connector.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        corners, ids, rejected_img_points = aruco.detectMarkers(gray,cls.__dict_aruco, parameters=cls.__parameters)
        return frame, corners, ids

    @staticmethod
    def _build_read_ar_marker_points(read_ids, corners):
        read_ar_marker_points = []

        for read_id in read_ids:
            index = np.where(ids == read_id)[0][0]
            corner_points = corners[index][0]
            ar_marker_point = ArMarkerPoint(read_id, corner_points)
            read_ar_marker_points.append(ar_marker_point)

        read_ar_marker_points = sorted(read_ar_marker_points)

        return read_ar_marker_points

    @staticmethod
    def _calc_from_points(ar_marker_point: ArMarkerPoint):
        center_width = ar_marker_point.center_width()
        center_height = ar_marker_point.center_height()
        angle = ar_marker_point.angle()
        hypotenuse = ar_marker_point.hypotenuse()

        return center_width, center_height, angle, hypotenuse

    @classmethod
    def _is_available_point_counts(cls, ar_marker_points):
        """ar_markerのidが読み取り数が有効数であるかどうかを判定する"""
        return len(ar_marker_points) in cls.__available_point_counts

    @classmethod
    def _get_command_when_single_ar_marker_id(cls, ar_marker_point):
        center_width, center_height, angle, hypotenuse = cls._calc_from_points(ar_marker_point)
        command = cls._get_command_by_angle(angle)

        if FRAME['HEIGHT_LIMIT'] > center_height:
            if center_width > FRAME['W_H'] + FRAME['MARGIN']:
                point_w = POINT['L_TURN']
            elif center_width < FRAME['W_H'] - FRAME['MARGIN']:
                point_w = POINT['R_TURN']
            else:
                point_w = POINT['CENTER']
        else:
            point_w = POINT['STOP']

        return command, point_w

    @classmethod
    def _get_command_by_angle(cls, angle):
        """ar_markerの角度からコマンドを取得する"""
        if angle > 3:
            command = 'l'
        elif angle < -3:
            command = 'r'
        else:
            command = ' '

        return command

    @classmethod
    def _send_serial_when_multi_ar_marker_points(cls, ar_marker_points):
        now = datetime.datetime.now()
        ar_marker_ids = [str(marker.ar_marker_id) for marker in ar_marker_points]
        row_data = f'{now.strftime("%Y/%m/%d")},{now.strftime("%H:%M:%S")},{",".join(ar_marker_ids)}'
        LoggingService.write_log(row_data)

        command = "".join(ar_marker_ids).ljust(16, '0')
        point_w = POINT['MULTI']

        return command, point_w

    @classmethod
    def _display_frame(cls, frame):
        cv2.imshow("camera", frame)
        cls._show_line(frame)

    @classmethod
    def _show_line(cls, frame):
        cv2.line(frame, (0, FRAME['HEIGHT_LIMIT']), (640, FRAME['HEIGHT_LIMIT']), (0, 0, 255), 1)
        cv2.line(frame, (FRAME['W_H'], 0), (FRAME['W_H'], 480), (255, 0, 0), 1)
        cv2.line(frame, (FRAME['W_H'] + FRAME['MARGIN'], 0), (FRAME['W_H'] + FRAME['MARGIN'], 480), (0, 255, 0), 2)
        cv2.line(frame, (FRAME['W_H'] - FRAME['MARGIN'], 0), (FRAME['W_H'] - FRAME['MARGIN'], 480), (0, 255, 0), 2)
