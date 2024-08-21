# HEAD GROUP
from raya.enumerations import LEDS_EXECUTION_CONTROL

LEDS_WAITING_FOR_DELIVERY_RESPONSE = {
    'group': 'head',
    'color': 'GREEN',
    'animation': 'MOTION_1',
    'speed': 1,
    'repetitions': 0,
    'execution_control': LEDS_EXECUTION_CONTROL.AFTER_CURRENT, 
}
