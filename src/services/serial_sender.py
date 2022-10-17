import serial

from .singleton import Singleton


class SerialSender(Singleton):
    def __init__(self, bitrate=115200, timeout=0.1):
        self.__serial = None
        # self.connect(bitrate, timeout)

    def connect(self, bitrate=115200, timeout=0.1):
        if self.__serial is None:
            self.__serial = serial.Serial("COM3", bitrate, timeout=timeout)

    def close(self):
        if self.__serial is not None:
            self.__serial.close()
            self.__serial = None

    def _send(self, data):
        if not isinstance(data, (bytes, bytearray)):
            data = data.encode()
        self.__serial.write(data.encode())
