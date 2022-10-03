class ArMarkerPoint:
    def __init__(self, ar_marker_id, corner_points):
        self.ar_marker_id = ar_marker_id
        self.corner_points = corner_points.tolist()
        self.corner_ul = corner_points[0].tolist()
        self.corner_ur = corner_points[1].tolist()
        self.corner_br = corner_points[2].tolist()
        self.corner_bl = corner_points[3].tolist()

    def __lt__(self, other):
        return self.corner_ul < other.corner_ul

    def show(self):
        return f'ar_marker_id: {self.ar_marker_id}, corner_points: {self._corner_points_formatter()}\n'

    def _corner_points_formatter(self):
        return [self.corner_ul, self.corner_ur, self.corner_br, self.corner_bl]
