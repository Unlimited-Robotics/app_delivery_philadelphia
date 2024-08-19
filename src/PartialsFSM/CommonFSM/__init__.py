from raya.tools.fsm import FSM
from raya.logger import RaYaLogger

from .helpers import CommonHelpers
from .actions import CommonActions
from .transitions import CommonTransitions


class CommonFSM(FSM):
    def __init__(self, *args, **kwarg):
        self.log = RaYaLogger(
            name='CommonFSM',
        )
        super().__init__(*args, **kwarg)