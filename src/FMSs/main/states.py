from src.FMSs.BaseAppFSM.states import STATES as BASE_STATES

# The first state is always the initial one
STATES = [
        'SETUP_ACTIONS',
        'GO_TO_CART_POINT',
        'NAV_TO_DELIVERY_POINT',
        'NOTIFY_ORDER_ARRIVED',
        
        'WAIT_FOR_UI_CONFIRMATION',
            'PACKAGE_DELIVERED',
            'PACKAGE_NOT_DELIVERED',
        
        'CHECK_IF_MORE_PACKAGES',
        
        'RETURN_TO_WAREHOUSE_ENTRANCE',
        'PARK_CART',
        'GO_TO_HOME_LOCATION',
        'NOTIFY_ALL_PACKAGES_STATUS',
        'END',
        
        'REQUEST_FOR_HELP',
        'WAIT_FOR_HELP',
        'RELEASE_CART',
    ]
STATES.extend(BASE_STATES)


# First state of FSM, if not defined, the FSM starts in the first element of
# the STATES list
INITIAL_STATE = 'SETUP_ACTIONS'


# If the FSM falls into one of these states, the execution finishes.
END_STATES = [
    'END',
]

# STATES_TRANSITION_TIMEOUTS = {
#     'WAIT_FOR_UI_CONFIRMATION': (30.0, 'PACKAGE_NOT_DELIVERED'),
# }
