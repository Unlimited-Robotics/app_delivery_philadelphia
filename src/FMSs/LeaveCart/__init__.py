from raya.tools.fsm import FSM
from raya.logger import RaYaLogger

class LeaveCartFSM(FSM):
    def __init__(self, *args, **kwarg):
        self.log = RaYaLogger(
            name='LeaveCartFSM',
        )
        super().__init__(*args, **kwarg)
