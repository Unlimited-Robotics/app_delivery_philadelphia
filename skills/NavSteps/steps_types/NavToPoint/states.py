from .errors import *
from ..CommonType import states as CommonStates
from ...PartialsFSM.RetryState import states as RetryStates

STATES = [
        *CommonStates.STATES,
        *RetryStates.STATES,
        'NAVIGATING_TO_POINT',
        'NAVIGATING_TO_POINT_FAILED'
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
