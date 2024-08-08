from raya.tools.fsm import FSM
from raya.logger import RaYaLogger

class TakeCartFSM(FSM):
    def __init__(self, *args, **kwarg):
        self.log = RaYaLogger(
            name='TakeCartFSM',
        )
        super().__init__(*args, **kwarg)
