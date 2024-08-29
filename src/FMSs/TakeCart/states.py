from src.FMSs.BaseAppFSM.states import STATES as BASE_STATES

# The first state is always the initial one
STATES = [
    'GO_TO_CART_POINT',
    'APPROACH_TO_CART',
    'ATTACH_TO_CART_EXEC',
    'ATTACH_TO_CART_FINISH',
    'GO_TO_ELEVATOR',
    'END',
]
STATES.extend(BASE_STATES)

# First state of FSM, if not defined, the FSM starts in the first element of
# the STATES list
INITIAL_STATE = 'GO_TO_CART_POINT'

# If the FSM falls into one of these states, the execution finishes.
END_STATES = [
    'END',
]
