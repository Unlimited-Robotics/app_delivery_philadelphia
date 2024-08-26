from .errors import *
from ..CommonType import states as CommonStates

STATES = [
        *CommonStates.STATES,
        'WAIT_FOR_DOOR_OPEN',
        'NAVIGATE_THROUGH_DOOR',
        'NAVIGATE_THROUGH_DOOR_FAILED',
]

INITIAL_STATE = 'SETUP'


END_STATES = [
        'END'
]


# Format: 'STATE': (<timeout>, <error_tuple>)
STATES_ABORT_TIMEOUTS = {
        *CommonStates.STATES_ABORT_TIMEOUTS,
}

STATES_TRANSITION_TIMEOUTS = {
        *CommonStates.STATES_TRANSITION_TIMEOUTS,
}
