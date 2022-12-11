from src.connector.serial_connector import SerialConnector
from src.services.loggiing_service import LoggingService


class SerialReceiveService:
    """
    シリアル通信を行うクラス
    """
    @classmethod
    def execute(cls, serial_connector):
        """
        シリアル通信のデータを受信した場合、ログを出力する
        """
        serial_data = cls._receive_serial(serial_connector)
        if serial_data is None:
            return None, None, None

        en_id, en_data, en_strength = cls._split_serial_data(serial_data)
        row_data = cls._convert_to_row_data(en_id, en_data, en_strength)
        LoggingService.write_log(row_data)
        return en_id, en_data, en_strength

    @classmethod
    def _receive_serial(cls, serial_connector: SerialConnector):
        """
        シリアル通信を受信して、str型に変換して返す
        """
        binary_line = serial_connector.read()
        if binary_line is None:
            return None

        return str(binary_line.decode())

    @classmethod
    def _split_serial_data(cls, serial_data: str):
        """
        str型のシリアルデータを分割して返す
        """
        en_id = serial_data[0:8]
        en_data = serial_data[9:24]
        en_strength = int(serial_data[25:28])
        return en_id, en_data, en_strength

    @classmethod
    def _convert_to_row_data(cls, en_id, en_data, en_strength):
        """
        分割したシリアルデータをcsvに書き込むための形式に変換する
        """
        return f"{en_id},{en_data},{en_strength}"


class SerialSendService:
    """
    シリアル通信を行うクラス
    """
    @classmethod
    def execute(cls, serial_connector: SerialConnector, command: str):
        """
        シリアル通信を送信する
        """
        serial_connector.send(command)
