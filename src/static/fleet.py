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

FLEET_STATUS_GOING_TO_CART_POINT  = {
    'message': 'Going to the cart point.',
    'status': FLEET_UPDATE_STATUS.INFO
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

FLEET_MESSAGE_OPEN_DOOR = 'The robot tried to enter the warehouse but the door was closed. Waiting for the door to open.'
FLEET_MESSAGE_WAITING_PACKAGE_LOAD = 'The robot is waiting for the package to be loaded.'
FLEET_MESSAGE_WAITING_CART_UNLOAD = 'The robot is waiting for the cart to be unloaded.'
FLEET_MESSAGE_CLOSED_DOOR = 'The robot tried to leave the warehouse but the door was closed. Waiting for the door to open.'

FLEET_DOOR_OPEN = 'The door is open.'
FLEET_CHECK_IF_LOCALIZED = 'Checking if robot is localized.'
FLEET_ALL_POINTS_REACHED = 'All packages delivered.'
FLEET_RETURNING_TO_WAREHOUSE = 'Returning to the warehouse.'

FLEET_REQUESTING_FOR_HELP = 'Gary is requesting for help.'
FLEET_TIMEOUT_REQUEST_FOR_HELP = '\'RayaFleetTimeout\' reached, operator did not respond to the request for help.'
FLEET_RESPONSE_TO_REQUEST_FOR_HELP = 'Fleet responded to the request for help, with '
