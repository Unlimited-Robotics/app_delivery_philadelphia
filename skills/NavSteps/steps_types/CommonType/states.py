from .errors import *


# The first state is always the initial one
STATES = [
        'SETUP',
        'END',
]

# First state of FSM, if not defined, the FSM starts in the first element of
# the STATES list
INITIAL_STATE = 'SETUP'


# If the FSM falls into one of these states, the execution finishes.
END_STATES = [
        'END'
]


# If one of the states takes more than an especified time, it aborts.
# Format: 'STATE': (<timeout>, <error_tuple>)
STATES_ABORT_TIMEOUTS = {}

STATES_TRANSITION_TIMEOUTS = {}
