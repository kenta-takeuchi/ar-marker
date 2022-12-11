import cv2

FRAME = {
    'W_H': 320,
    'H_H': 240,
    'MARGIN':  50,
    'HEIGHT_LIMIT': 350,
    'FONT': cv2.FONT_HERSHEY_SIMPLEX,
    'POSITION': (10, 450),
    'FONT_SCALE': 2,
    'FONT_COLOR': (255, 255, 0),
}

POINT = {
    'L_TURN': 'L_TURN',
    'R_TURN': 'R_TURN',
    'CENTER': 'CENTER',
    'STOP': 'STOP',
    'MULTI': 'MULTI',
}

MODE = {
    "initialize": 'initialize',
}
