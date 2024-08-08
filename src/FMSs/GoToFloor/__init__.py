from raya.tools.fsm import FSM
from raya.logger import RaYaLogger

class GoToFloorFSM(FSM):
    def __init__(self, *args, **kwarg):
        self.log = RaYaLogger(
            name='GoToFloorFSM',
        )
        super().__init__(*args, **kwarg)
