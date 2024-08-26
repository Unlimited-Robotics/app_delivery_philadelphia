TYPE_NAME = 'nav_to_point'

OBSTACLE_DETECTION_THRESHOLDS = [1, 2]
NAV_CODES_IS_NAVIGATING = [4, 6, 241]
NAV_CODES_OBSTACLE_DETECTED = [5, 7, 9, 17]
NAV_CODES_TRY_PLAN = [3]
NAV_CODES_FINISH_NAV = [0]
DISTANCE_TO_FINISH_PARTIAL_NAVS = 3.0


# Code	Msg
# 1	    new goal received 42
# 2	    goal updated
# 3	    planning
# 4	    new path computed
# 5	    could not plan, clearing global costmap and waiting
# 6	    following the path
# 7	    could not follow path, clearing local costmap and waiting
# 8	    trying to follow the path again
# 9	    could not navigate, clearing costmaps and and waiting
# 11	adjusting orientation
# 12	goal reached
# 13	plan is valid
# 14	checking if path is valid
# 15	path expired
# 17	follow path halted
# 19	plan NOT VALID
# 20	old path timestamp restarted
# 21	position reached
# 30	New path computed after: {sec} seconds.
# 241	{distance_to_goal}


from raya.enumerations import LEDS_EXECUTION_CONTROL, UI_THEME_TYPE
from raya.enumerations import UI_ANIMATION_TYPE

SOUND_OBSTACLE_DETECTED_1 = {
        'name': 'clear_the_way_1',
        'volume': 100,
        'duration': 2.0,
    }
SOUND_OBSTACLE_DETECTED_2 = {
        'name': 'clear_the_way_2',
        'volume': 100,
        'duration': 6.0,
    }

SOUNDS_OBSTACLES_DETECTED = [
    SOUND_OBSTACLE_DETECTED_1, 
    SOUND_OBSTACLE_DETECTED_2
]

SOUND_THANK_YOU = {
        'name': 'thank_you_1',
        'volume': 100,
        'duration': 1.0,
    }

LEDS_NOTIFY_OBSTACLE = {
    'group': 'head',
    'color': 'YELLOW',
    'animation': 'MALFUNCTION_VER_1',
    'speed': 1,
    'repetitions': 1,
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


UI_OBSTACLE_DETECTED = 'res:caution.gif'
UI_SCREEN_OBSTACLE_DETECTED = {
    'title': 'Please clear the way',
    'subtitle': 'I\'m on duty',
    'path': UI_OBSTACLE_DETECTED,
    'format': UI_ANIMATION_TYPE.GIF,
    **UI_COMMON_OPTIONS
}
