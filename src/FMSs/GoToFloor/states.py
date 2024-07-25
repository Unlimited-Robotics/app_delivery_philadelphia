from src.FMSs.BaseAppFSM.states import STATES as BASE_STATES

# The first state is always the initial one
STATES = [
        'SELECT_ELEVATOR',
        'NAV_TO_ELEVATOR',
        'TELEOPERATING',
        'CHANGE_MAP',
        'TELEOPERATION_DONE',
        'EXIT_FROM_ELEVATOR',
        'LOCALIZING',
        'END',
    ]
STATES.extend(BASE_STATES)

# First state of FSM, if not defined, the FSM starts in the first element of
# the STATES list
INITIAL_STATE = 'SELECT_ELEVATOR'


# If the FSM falls into one of these states, the execution finishes.
END_STATES = [
    'END',
]
