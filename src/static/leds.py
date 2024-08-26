# HEAD GROUP
from raya.enumerations import LEDS_EXECUTION_CONTROL

LEDS_WAITING_FOR_USER_INPUT = {
    'group': 'head',
    'color': 'GREEN',
    'animation': 'MOTION_1',
    'speed': 1,
    'repetitions': 0,
    'execution_control': LEDS_EXECUTION_CONTROL.AFTER_CURRENT, 
}

LEDS_WAITING_FOR_DELIVERY_RESPONSE = LEDS_WAITING_FOR_USER_INPUT

LEDS_BEING_TELEOPERATED = LEDS_WAITING_FOR_USER_INPUT

LEDS_NAVIGATING = {
    'group': 'head',
    'color': 'CYAN',
    'animation': 'MOTION_12',
    'speed': 1,
    'repetitions': 0,
    'execution_control': LEDS_EXECUTION_CONTROL.OVERRIDE, 
}

LEDS_LOCALIZING = {
    'group': 'head',
    'color': 'GREEN',
    'animation': 'MOTION_1',
    'speed': 1,
    'repetitions': 0,
    'execution_control': LEDS_EXECUTION_CONTROL.OVERRIDE, 
}

