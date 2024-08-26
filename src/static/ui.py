# SCREENS
from raya.enumerations import UI_THEME_TYPE, UI_ANIMATION_TYPE

UI_COMMON_OPTIONS = {
    'theme': UI_THEME_TYPE.WHITE,
    'back_button_text': '',
}

UI_LOTTIE_DOOR = 'res:lottie_door.json'
UI_LOTTIE_CHECK_DELIVERY = 'res:lottie_check.json'
UI_LOTTIE_TELEOPERATION = 'res:lottie_teleoperation.json'
UI_LOTTIE_DELIVERING_PACKAGE = 'res:lottie_package_walking.json'
UI_OBSTACLE_DETECTED = 'res:caution.gif'


UI_SCREEN_LOCALIZING = {
    'title':'Localizing 🕵',
    **UI_COMMON_OPTIONS
}

UI_SCREEN_NAVIGATING = {
    'title':'Hello! I\'m Gary, your delivery robot',
    'lottie': UI_LOTTIE_DELIVERING_PACKAGE,
    **UI_COMMON_OPTIONS
}

UI_SCREEN_PICK_CART = {
    'title':'Picking your cart',
    'lottie': UI_LOTTIE_DELIVERING_PACKAGE,
    **UI_COMMON_OPTIONS
}

UI_SCREEN_NAV_TO_PACKAGE_POINT = {
    'title':'Delivering items to [department_name]',
    'lottie': UI_LOTTIE_DELIVERING_PACKAGE,
    **UI_COMMON_OPTIONS
}

UI_SCREEN_DELIVERING_SUCCESS = {
    'title':'Thank you', 
    'subtitle':'Notification sent to the responsible',
    'lottie': UI_LOTTIE_CHECK_DELIVERY,
    **UI_COMMON_OPTIONS
}

UI_SCREEN_RELEASE_CART = {
    'title':'Releasing Cart', 
    'subtitle':'Please wait while the cart is being released.',
    **UI_COMMON_OPTIONS
}

UI_SCREEN_OPTIONS_DELIVERY_ARRIVED = {
    'title':'Delivery Confirmation',
    'max_items_shown': 0,
    'data': [
            {
                'id': 1, 
                'name': 'Confirm Delivery Package', 
                'imgSrc': 'res:package_confirm.png'
            }, 
            {
                'id': 2, 
                'name': 'Package Not Found', 
                'imgSrc': 'res:package_not_found.png'
            },
            {
                'id': 3, 
                'name': 'Problem With The Package', 
                'imgSrc': 'res:package_problem.png'
            },
        ],
    'custom_style': {
        'selector': {
            'background': '#FFFFFF',
        },
    },
    **UI_COMMON_OPTIONS
}

UI_SCREEN_OPTIONS_ELEVATOR_ENTERING = {
    'title':'I need to go to the floor [floor], Which elevator should I use?',
    'max_items_shown': 0,
    'data': [
            {'id': '1', 'name': 'Elevator 1'}, 
            {'id': '2', 'name': 'Elevator 2'},
            {'id': '3', 'name': 'Elevator 3'},
        ],
    **UI_COMMON_OPTIONS
}

UI_SCREEN_TELEOPERATION = {
    'title': 'Hello! I\'m Gary, your delivery robot',
    'subtitle': 'Remote Control Activation',
    'lottie': UI_LOTTIE_TELEOPERATION,
    **UI_COMMON_OPTIONS
}

UI_CALL_TO_ACTION_TELEOPERATION_DONE = {
    'title': 'Teleoperation',
    'subtitle': 'Please take control of the robot',
    'button_text': 'Done',
    **UI_COMMON_OPTIONS
}

UI_SCREEN_NAV_TO_FLOOR = {
    'title':'Navigating to floor [floor]',
    'lottie': UI_LOTTIE_DELIVERING_PACKAGE,
    **UI_COMMON_OPTIONS
}

UI_SCREEN_FAILED = {
    'title':'Failed',
    **UI_COMMON_OPTIONS
}

UI_KEYBOARD = {
    'title': 'Please type your name',
    **UI_COMMON_OPTIONS
}
