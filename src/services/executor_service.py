import cv2

from src.config.constants import MODE, FRAME
from src.connector.serial_connector import SerialConnector
from src.connector.video_connector import VideoConnector
from src.services.loggiing_service import LoggingService
from src.services.serial_service import SerialReceiveService, SerialSendService
from src.services.video_service import VideoService


class ExecutorService:
    """
    ar-markerのサービスを実行するクラス
    """

    def __init__(self, camera_id=0):
        """
        コンストラクタ
        :param camera_id: カメラID
        """
        self.serial_connector = SerialConnector()
        self.video_connector = VideoConnector(camera_id)
        self.mode = MODE["initialize"]

    def execute(self):
        while True:
            # シリアル通信を受信する
            en_id, _, _ = SerialReceiveService.execute(self.serial_connector)
            if en_id is not None:  # シリアル通信を受信した場合
                self._change_mode(en_id)  # idに応じてモードを変更する

            # カメラの読み取り処理を実行
            # ar-markerを読み込んだ場合はコマンドを取得する
            command = VideoService.execute(self.video_connector, self.mode)
            if command is not None:
                SerialSendService.execute(self.serial_connector, command)  # シリアル通信でコマンド送信する
 
            # キー操作があればwhileループを抜ける
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        # カメラオブジェクトとウィンドウの解放
        self.serial_connector.close()
        self.video_connector.close()

    def _change_mode(self, en_id):
        """
        ステータスを変更する
        :param status: ステータス
        """
        self.mode = MODE[en_id]
