from raya.enumerations import UI_THEME_TYPE, LEDS_EXECUTION_CONTROL

TYPE_NAME = 'automatic_door'
CAMERAS_DETECTING_DOOR = ['nav_bottom']

# PARAMETERS DEFAULT VALUES
SOUND_OPEN_DOOR_NAME = 'open_door_1'
SOUND_THANKS_DOOR_NAME = 'thank_you_door_1'
LEDS_DOOR_OPEN_ANIMATION = 'MOTION_10_VER_3'
DELAY_AFTER_DOOR_OPENED = 1.0
FLEET_CALL_MESSAGE = 'Hi i am Gary, Please open the door for me. Thank you!'
DOOR_CLOSE_TIMEOUT = 10.0
TIME_BEFORE_FIRST_CALL = 60.0 * 1 # 1 minute
TIME_BEETWEEN_CALLS = 60.0 * 2 # 2 minutes
DOOR_TAG_TIMEOUT = 3.0
RANGE_DEGREES_TAG_VISIBLE = 50


# DICTIONARIES FOR PARAM VALUES
SOUND_OPEN_DOOR_REQUEST = {
        'name': SOUND_OPEN_DOOR_NAME,
        'volume': 100,
        'duration': 4.0,
    }
SOUND_THANKS_DOOR_AUDIO = {
        'name': SOUND_THANKS_DOOR_NAME,
        'volume': 100,
        'duration': 3.0,
    }
LEDS_DOOR_OPENED = {
    'group': 'head',
    'color': 'GREEN',
    'animation': LEDS_DOOR_OPEN_ANIMATION,
    'speed': 1,
    'repetitions': 1,
    'execution_control': LEDS_EXECUTION_CONTROL.OVERRIDE, 
}
UI_COMMON_OPTIONS = {
    'theme': UI_THEME_TYPE.WHITE,
    'back_button_text': '',
}
UI_LOTTIE_DOOR = 'res:lottie_door.json'
UI_SCREEN_WAIT_FOR_DOOR_OPEN = {
    'title':'Please open the door',
    'lottie': UI_LOTTIE_DOOR,
    **UI_COMMON_OPTIONS
}
FLEET_REQUEST_USER_ACTION = {
    'request_type': 'call',
    'request_args':{
        'message': FLEET_CALL_MESSAGE
    },
    'timeout': 1.0
}
