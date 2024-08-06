from raya.tools.fsm import FSM

from .actions import CommonAction
from .helpers import CommonHelpers
from .transitions import CommonTransitions

class BaseAppFSM(FSM):
    def __init__(self, *args, **kwarg):
        super().__init__(*args, **kwarg)
