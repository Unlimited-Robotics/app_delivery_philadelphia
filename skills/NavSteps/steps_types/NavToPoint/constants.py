TYPE_NAME = 'nav_to_point'

NAVIGATION_TRY_LIMIT = 1
OBSTACLE_DETECTION_THRESHOLDS = [2, 7]

from raya.enumerations import LEDS_EXECUTION_CONTROL, UI_THEME_TYPE

SOUND_OBSTACLE_DETECTED_1 = {
        'path': 'res:Clear_the_way.mp3',
        'volume': 100,
    }
SOUND_OBSTACLE_DETECTED_2 = {
        'path': 'res:Clear_the_way2.mp3',
        'volume': 100,
    }

SOUNDS_OBSTACLES_DETECTED = [
    SOUND_OBSTACLE_DETECTED_1, 
    SOUND_OBSTACLE_DETECTED_2
]

LEDS_NOTIFY_OBSTACLE = {
    'group': 'head',
    'color': 'YELLOW',
    'animation': 'MALFUNCTION_VER_1',
    'speed': 1,
    'repetitions': 0,
    'execution_control': LEDS_EXECUTION_CONTROL.OVERRIDE,
}

LEDS_NAVIGATING = {
    'group': 'head',
    'color': 'CYAN',
    'animation': 'MOTION_12',
    'speed': 1,
    'repetitions': 0,
    'execution_control': LEDS_EXECUTION_CONTROL.OVERRIDE, 
}

UI_COMMON_OPTIONS = {
    'theme': UI_THEME_TYPE.WHITE,
    'back_button_text': '',
}
UI_LOTTIE_DELIVERING_PACKAGE = 'res:lottie_package_walking.json'

UI_SCREEN_NAVIGATING = {
    'title':'Hello! I\'m Gary, your delivery robot',
    'lottie': UI_LOTTIE_DELIVERING_PACKAGE,
    **UI_COMMON_OPTIONS
}
