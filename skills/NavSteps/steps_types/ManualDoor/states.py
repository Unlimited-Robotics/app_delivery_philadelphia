from .errors import *
from ..CommonType import states as CommonStates
from ..AutomaticDoor import states as AutomaticDoorStates

STATES = [
        *CommonStates.STATES,
        *AutomaticDoorStates.STATES,
        'CALL_FOR_HELP',
]

INITIAL_STATE = 'SETUP'


END_STATES = [
        'END'
]


# Format: 'STATE': (<timeout>, <error_tuple>)
STATES_ABORT_TIMEOUTS = {
        *CommonStates.STATES_ABORT_TIMEOUTS,
        *AutomaticDoorStates.STATES_ABORT_TIMEOUTS,
}

STATES_TRANSITION_TIMEOUTS = {
        *CommonStates.STATES_TRANSITION_TIMEOUTS,
        *AutomaticDoorStates.STATES_TRANSITION_TIMEOUTS,
}
