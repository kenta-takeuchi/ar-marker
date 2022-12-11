import serial

from src.base.singleton import Singleton


class SerialConnector(Singleton):
    def __init__(self, bitrate=115200, timeout=0.1):
        self.__serial = None
        self.output_path = "read_test.csv"
        try:
            self.connect(bitrate, timeout)
        except Exception:
            print("SerialConnector: Serial connection failed.")

    def connect(self, bitrate=115200, timeout=0.1):
        if self.__serial is None:
            self.__serial = serial.Serial("COM3", bitrate, timeout=timeout)

    def close(self):
        if self.__serial is None:
            return

        self.__serial.close()
        self.__serial = None

    def send(self, data):
        if self.__serial is None:
            return

        if not isinstance(data, (bytes, bytearray)):
            data = data.encode()
        self.__serial.write(data)

    def read(self):
        if self.__serial is None:
            return None

        return self.__serial.readline()
