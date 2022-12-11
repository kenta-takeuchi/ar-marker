import serial

from src.base.singleton import Singleton


class LoggingService(Singleton):
    __output_path = "./read_ar_marker_logs.csv"

    @staticmethod
    def write_log(log):
        try:
            with open(__output_path, mode="a") as f:
                f.write(f'{log}\n')
        except Exception:
            print(f"LoggingService: Write log failed. log: {log}")
