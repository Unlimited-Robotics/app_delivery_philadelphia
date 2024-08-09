from . import CommonTypeFSM
from .constants import *

class CommonType:
    
    def __init__(self, name) -> None:
        self.name = name
        self.type = TYPE_NAME
        self.fsm = CommonTypeFSM(
            self_object=self,
            name=self.name, 
            log_transitions=True,
        )
