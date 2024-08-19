from raya.tools.fsm import FSM
from raya.logger import RaYaLogger

class MainFSM(FSM):
    def __init__(self, *args, **kwarg):
        self.log = RaYaLogger(
            name='MainFSM',
        )
        super().__init__(*args, **kwarg)
