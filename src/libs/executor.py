from .image_reader import ImageReader
import time


class Executor:
    def __init__(self):
        pass

    def execute(self):
        camera_id = 0
        image_reader = ImageReader(camera_id)

        try:
            while True:
                print(' ----- get_markID ----- ')
                print(image_reader.get_mark_ids())
                time.sleep(0.5)
        except KeyboardInterrupt:
            image_reader.cap.release()

