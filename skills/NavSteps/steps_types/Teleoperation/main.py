from . import TeleoperationFSM

from .constants import *

class Teleoperation:

    def __init__(self,
            name: str,
        ) -> None:
        self.name = name
        self.type = TYPE_NAME
        self.fsm = TeleoperationFSM(
            self_object=self,
            name=self.name, 
            log_transitions=True,
        )
