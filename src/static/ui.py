# SCREENS
from raya.enumerations import UI_THEME_TYPE, UI_ANIMATION_TYPE

UI_COMMON_OPTIONS = {
    'theme': UI_THEME_TYPE.WHITE,
    'back_button_text': '',
}

UI_LOTTIE_DOOR = 'res:lottie_door.json'
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

UI_SCREEN_WAIT_FOR_DOOR_OPEN = {
    'title':'Please open the door',
    'lottie': UI_LOTTIE_DOOR,
    **UI_COMMON_OPTIONS
}

UI_SCREEN_NAV_TO_PACKAGE_POINT = {
    'title':'Delivering items to [department_name]',
    'lottie': UI_LOTTIE_DELIVERING_PACKAGE,
    **UI_COMMON_OPTIONS
}

UI_SCREEN_DELIVERING_SUCCESS = {
    'title':'Delivering Success ✅', 
    'subtitle':'The package was delivered successfully',
    **UI_COMMON_OPTIONS
}

UI_PACKAGE_NOT_DELIVERED = {
    'title':'Package deliver failed 🚫', 
    **UI_COMMON_OPTIONS
}

UI_SCREEN_RELEASE_CART = {
    'title':'Releasing Cart', 
    'subtitle':'Please wait while the cart is being released.',
    **UI_COMMON_OPTIONS
}

UI_SCREEN_WAIT_FOR_HELP_SELECTOR = {
    'title':'I\'m stuck, please help me, and choose an option',
    'max_items_shown': 0,
    'data': [
            {'id': 1, 'name': 'Abort App 🚫'}, 
            {'id': 2, 'name': 'Continue 🚶‍♂️'},
        ],
    **UI_COMMON_OPTIONS
}

UI_SCREEN_OPTIONS_DELIVERY_ARRIVED = {
    'title':'Delivery Confirmation',
    'max_items_shown': 0,
    'data': [
            {'id': 1, 'name': 'Confirm delivery package 📦'}, 
            {'id': 2, 'name': 'Package not found'},
            {'id': 3, 'name': 'Problem with my package'},
        ],
    **UI_COMMON_OPTIONS
}

UI_SCREEN_OPTIONS_ELEVATOR_ENTERING = {
    'title':'I need to go to the floor [floor], Which elevator should i use?',
    'max_items_shown': 0,
    'data': [
            {'id': '1', 'name': 'Elevator 1'}, 
            {'id': '2', 'name': 'Elevator 2'},
            {'id': '3', 'name': 'Elevator 3'},
        ],
    **UI_COMMON_OPTIONS
}

UI_CALL_TO_ACTION_TELEOPERATION = {
    'title': 'Teleoperation',
    'subtitle': 'Please take control of the robot',
    'button_text': '',
    **UI_COMMON_OPTIONS
}

UI_CALL_TO_ACTION_TELEOPERATION_DONE = {
    'title': 'Teleoperation',
    'subtitle': 'Please take control of the robot',
    'button_text': 'Done 🎉',
    **UI_COMMON_OPTIONS
}

UI_SCREEN_NAV_TO_FLOOR = {
    'title':'Navigating to floor [floor]',
    'lottie': UI_LOTTIE_DELIVERING_PACKAGE,
    **UI_COMMON_OPTIONS
}

UI_SCREEN_OBSTACLE_DETECTED = {
    'title': 'Please clear the way',
    'subtitle': 'I\'m on duty',
    'path': UI_OBSTACLE_DETECTED,
    'format': UI_ANIMATION_TYPE.GIF,
    **UI_COMMON_OPTIONS
}


UI_SCREEN_FAILED = {
    'title':'Failed',
    **UI_COMMON_OPTIONS
}
