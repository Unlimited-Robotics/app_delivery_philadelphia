
# The first state is always the initial one
STATES = [
        'CHECK_IF_INSIDE_ZONE',
        'GO_TO_WAREHOUSE_ENTRANCE',
        'ENTER_WAREHOUSE',
        'GO_TO_HOME_LOCATION',
        'WAIT_FOR_BUTTON_OPEN_ENTRANCE',
        'GO_TO_CART_POINT',
        'WAIT_FOR_LOAD_PACKAGE',
        'ATTACH_TO_CART',
        'GO_TO_WAREHOUSE_EXIT',
        'LEAVE_WAREHOUSE',
        'WAIT_FOR_BUTTON_EXITING',
        'END',
    ]


# First state of FSM, if not defined, the FSM starts in the first element of
# the STATES list
INITIAL_STATE = 'CHECK_IF_INSIDE_ZONE'


# If the FSM falls into one of these states, the execution finishes.
END_STATES = [
    'END',
]

# STATES_TRANSITION_TIMEOUTS = [
#     3.0, ''
# ]