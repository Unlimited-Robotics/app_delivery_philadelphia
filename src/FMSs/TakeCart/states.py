from src.FMSs.BaseAppFSM.states import STATES as BASE_STATES

# The first state is always the initial one
STATES = [
    'CHECK_IF_INSIDE_ZONE',
    'GO_TO_HOME_LOCATION',
    'GO_TO_CART_POINT',
    'ATTACH_TO_CART',
    'GO_TO_ELEVATOR',
    'END',
]
STATES.extend(BASE_STATES)

# First state of FSM, if not defined, the FSM starts in the first element of
# the STATES list
# INITIAL_STATE = 'GO_TO_CART_POINT'
INITIAL_STATE = 'GO_TO_ELEVATOR'


# If the FSM falls into one of these states, the execution finishes.
END_STATES = [
    'END',
]

# STATES_TRANSITION_TIMEOUTS = [
#     3.0, ''
# ]