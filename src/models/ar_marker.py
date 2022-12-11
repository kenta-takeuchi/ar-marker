import math

class ArMarkerPoint:
    def __init__(self, ar_marker_id, corner_points):
        self.ar_marker_id = ar_marker_id
        self.corner_points = corner_points.tolist()
        self.left_top = corner_points[0].tolist()
        self.right_top = corner_points[1].tolist()
        self.right_bottom = corner_points[2].tolist()
        self.left_bottom = corner_points[3].tolist()

    def __lt__(self, other):
        return self.left_top < other.left_top

    def show(self):
        return f'ar_marker_id: {self.ar_marker_id}, corner_points: {self._corner_points_formatter()}\n'

    def _corner_points_formatter(self):
        return [self.left_top, self.right_top, self.right_bottom, self.left_bottom]

    def width(self):
        """左上X - 右上X"""
        return self.left_top[0] - self.right_top[0]

    def center_width(self):
        return self.left_top[0] + self.width() / 2

    def height(self):
        """右上ｙ-左上ｙ"""
        return self.right_top[1] - self.left_top[1]

    def center_height(self):
        return self.left_top[1] + self.height() / 2

    def angle(self):
        """底辺と高さから角度を求める"""
        return math.atan(self.height() / self.width()) * 180 / math.pi

    def hypotenuse(self):
        """底辺と高さから斜辺を求める"""
        return round(math.sqrt(math.pow(self.width(), 2) + math.pow(self.height(), 2)))
