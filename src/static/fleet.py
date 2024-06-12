from raya.enumerations import FLEET_UPDATE_STATUS

FLEET_REQUEST_HELP = {
    'title': 'Requesting Help',
    'message': 'I`m stuck, please send help',
}

FLEET_REQUEST_CONFIRMATION_PACKAGE = {
    'title': 'Requesting Confirmation',
    'message': 'The package has been delivered. Please confirm',
    'timeout': 30.0
}


FLEET_REQUEST_ACTION_USER = {
    'title': 'I need help',
    'subtitle': 'can you help me?',
    'buttons': [
        'My package was delivered successfully', 
        'My package is not the one that i ordered',
        'My package is damaged',
        'My package is missing'
    ],
    'timeout': 60
}

# FLEET STATUS

FLEET_MESSAGE_WAITING_PACKAGE_LOAD = 'The robot is waiting for the package to be loaded.'
FLEET_MESSAGE_WAITING_CART_UNLOAD = 'The robot is waiting for the cart to be unloaded.'

FLEET_STATUS_GOING_TO_CART_POINT  = 'Going to the cart point.'
FLEET_CHECK_IF_LOCALIZED = 'Checking if robot is localized.'
FLEET_ALL_POINTS_REACHED = 'All packages delivered.'
FLEET_RETURNING_TO_WAREHOUSE = 'All delivery points reached, Returning to the warehouse.'
FLEET_PARKING_CART = 'Leaving the delivery cart in the warehouse.'

FLEET_REQUESTING_FOR_HELP = 'Gary is requesting for help.'
FLEET_WAITING_FOR_HELP = 'Waiting for help.'
FLEET_TIMEOUT_REQUEST_FOR_HELP = '\'RayaFleetTimeout\' reached, operator did not respond to the request for help.'
FLEET_RESPONSE_TO_REQUEST_FOR_HELP = 'Fleet responded to the request for help, with '
FLEET_WAIT_FOR_PACKAGE_CONFIRMATION = 'Waiting for package confirmation.'
FLEET_PACKAGE_CONFIRM_USING_CHEST = 'The package was confirm using the chest button.'
FLEET_PACKAGE_CONFIRM_USING_UI = 'The package was confirm using the options using the ui oprtions.'
FLEET_GOING_TO_HOME_LOCATION = 'Going to the home location.'
FLEET_ABORT_APP_RELEASE_CART = 'The App was aborted, The cart is being released.'
FLEET_CART_RELEASED = 'The cart was released.'

FLEET_GOING_TO_WAREHOUSE_ENTRANCE = 'Going to the warehouse entrance.'
FLEET_GOING_TO_WAREHOUSE_EXIT = 'Going to the warehouse exit.'
FLEET_ENTERING_WAREHOUSE = 'Entering the warehouse.'
FLEET_LEAVING_WAREHOUSE = 'Leaving the warehouse.'
FLEET_WAIT_FOR_BUTTON_DOOR = 'Waiting for the door to be open and the button to be pressed.'
FLEET_BUTTON_WAS_PRESS = 'The button was press, the robot is moving.'
FLEET_ROBOT_NAVIGATING_TO_HOME = 'The robot is navigating to the home location.'
FLEET_ROBOT_MOVING_TO_ATTACH_POINT = 'The robot is moving to the attach point.'
FLEET_ROBOT_MOVING_TO_DETACH_POINT = 'The robot is moving to the detach point.'
FLEET_ROBOT_ATTACHING_TO_CART = 'The robot is attaching to the cart.'
FLEET_ROBOT_DETACHING_TO_CART = 'The robot is detaching to the cart.'
FLEET_ROBOT_OUTSIDE_WAREHOUSE = 'The robot is outside the warehouse.'
