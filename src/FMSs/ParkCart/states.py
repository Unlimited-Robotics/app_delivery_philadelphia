
# The first state is always the initial one
STATES = [
        'CHECK_IF_INSIDE_ZONE',
        'ENTER_WAREHOUSE',
        'WAIT_FOR_BUTTON_OPEN_ENTRANCE',
        'GO_TO_CART_POINT',
        'WAIT_FOR_UNLOAD_PACKAGE',
        'END',
    ]


# First state of FSM, if not defined, the FSM starts in the first element of
# the STATES list
INITIAL_STATE = 'CHECK_IF_INSIDE_ZONE'


# If the FSM falls into one of these states, the execution finishes.
END_STATES = [
    'END',
]
