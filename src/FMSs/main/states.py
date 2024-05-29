from src.static.app_errors import *


# The first state is always the initial one
STATES = [
        'SETUP_ACTIONS',
        'GO_TO_CART_POINT',
        'NAV_TO_DELIVERY_POINT',
        'NOTIFY_ORDER_ARRIVED',
        'WAIT_FOR_CHEST_CONFIRMATION',
        'PACKAGE_DELIVERED',
        'PACKAGE_NOT_DELIVERED',
        
        'CHECK_IF_MORE_PACKAGES',
        'RETURN_TO_WAREHOUSE',
        'REQUEST_FOR_HELP',
        'WAIT_FOR_CHEST_BY_OPERATOR',
        'RELEASE_CART',
        'GO_TO_RELEASE_POINT',
        'NOTIFY_ALL_PACKAGES_STATUS',
        'END',
    ]


# First state of FSM, if not defined, the FSM starts in the first element of
# the STATES list
INITIAL_STATE = 'SETUP_ACTIONS'


# If the FSM falls into one of these states, the execution finishes.
END_STATES = [
    'NAV_TO_DELIVERY_POINT',
]


# If one of the states takes more than an especified time, it aborts.
# Format: 'STATE': (<timeout>, <error_tuple>)
# STATES_TIMEOUTS = {
#     'LOCALIZING' : (10.0, APPERR_COULD_NOT_LOCALIZE),
# }
