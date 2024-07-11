# HEAD GROUP
from raya.enumerations import LEDS_EXECUTION_CONTROL

LEDS_NOTIFY_OBSTACLE = {
    'group': 'head',
    'color': 'RED',
    'animation': 'MALFUNCTION_VER_1',
    'speed': 1,
    'repetitions': 0,
}

LEDS_GARY_SPEAKING = {
    'group': 'head',
    'color': 'CYAN',
    'animation': 'MOTION_4',
    'speed': 1,
    'repetitions': 0,
}

LEDS_NAVIGATING_TO_DELIVERY_POINT = {
    'group': 'head',
    'color': 'CYAN',
    'animation': 'MOTION_12',
    'speed': 1,
    'repetitions': 0,
    'execution_control': LEDS_EXECUTION_CONTROL.AFTER_CURRENT, 
}
