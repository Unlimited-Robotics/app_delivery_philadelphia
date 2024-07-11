# SCREENS
from raya.enumerations import UI_THEME_TYPE

UI_COMMON_OPTIONS = {
    'theme': UI_THEME_TYPE.WHITE,
    'back_button_text': '',
}

UI_LOTTIE_DOOR = 'res:lottie_door.json'
UI_LOTTIE_DELIVERING_PACKAGE = 'res:lottie_package_walking.json'


UI_SCREEN_LOCALIZING = {
    'title':'Starting Application', 
    'subtitle':'Localizing 🕵',
    **UI_COMMON_OPTIONS
}

UI_SCREEN_NAV_TO_WAREHOUSE = {
    'title':'Navigating', 
    'subtitle':'Going to warehouse',
    **UI_COMMON_OPTIONS
}

UI_SCREEN_ENTERING_TO_WAREHOUSE = {
    'title':'Navigating', 
    'subtitle':'Entering warehouse',
    **UI_COMMON_OPTIONS
}

# TODO add sound for this interaction
UI_SCREEN_WAIT_FOR_DOOR_OPEN = {
    'title':'Please open the door',
    'lottie': UI_LOTTIE_DOOR,
    **UI_COMMON_OPTIONS
}

UI_SCREEN_NAV_TO_WAREHOUSE_EXIT = {
    'title':'Navigating', 
    'subtitle':'Navigating to warehouse exit',
    **UI_COMMON_OPTIONS
}

UI_SCREEN_NAV_TO_HOME = {
    'title':'Navigating', 
    'subtitle':'Navigating to home position',
    **UI_COMMON_OPTIONS
}

UI_SCREEN_LEAVE_WAREHOUSE = {
    'title':'Navigating', 
    'subtitle':'Leaving warehouse',
    **UI_COMMON_OPTIONS
}

UI_SCREEN_NAV_TO_WAREHOUSE_RETURN = {
    'title':'Navigating', 
    'subtitle':'Going back to warehouse',
    **UI_COMMON_OPTIONS
}

UI_SCREEN_NAV_TO_PACKAGE_POINT = {
    'title':'Navigating', 
    'subtitle':'Delivering package',
    **UI_COMMON_OPTIONS
}

UI_SCREEN_DELIVERING_SUCCESS = {
    'title':'Delivering Success ✅', 
    'subtitle':'The package was delivered successfully',
    **UI_COMMON_OPTIONS
}

UI_SCREEN_ALL_PACKAGES_DONE = {
    'title':'Delivering finished', 
    'subtitle':'The app went through all the packages and parked the cart.',
    **UI_COMMON_OPTIONS
}

UI_SCREEN_RELEASE_CART = {
    'title':'Releasing Cart', 
    'subtitle':'Please wait while the cart is being released.',
    **UI_COMMON_OPTIONS
}

UI_PACKAGE_NOT_DELIVERED = {
    'title':'Package deliver failed 🚫', 
    **UI_COMMON_OPTIONS
}

UI_SCREEN_REQUEST_FOR_HELP = {
    'title':'Request for Help',
    'subtitle':'I\'m stuck, contacting the fleet...',
    **UI_COMMON_OPTIONS
}

UI_SCREEN_WAIT_FOR_HELP_SELECTOR = {
    'title':'I\'m stuck, please help me, and choose an option',
    'max_items_shown': 2,
    'data': [
            {'id': 1, 'name': 'Abort App 🚫'}, 
            {'id': 2, 'name': 'Continue 🚶‍♂️'},
        ],
    **UI_COMMON_OPTIONS
}

UI_SCREEN_OPTIONS_DELIVERY_ARRIVED = {
    'title':'Deliver complete, please press one of the following options',
    'max_items_shown': 4,
    'data': [
            {'id': 1, 'name': 'My package was delivered successfully'}, 
            {'id': 2, 'name': 'My package is not the one that i ordered'},
            {'id': 3, 'name': 'My package is damaged'},
            {'id': 4, 'name': 'My package is missing'},
        ],
    **UI_COMMON_OPTIONS
}

UI_SCREEN_FAILED = {
    'title':'Failed',
    **UI_COMMON_OPTIONS
}
