from . import TemplateFSM

from .constants import *

class Template:

    def __init__(self,
            name: str,
        ) -> None:
        self.name = name
        self.type = TYPE_NAME
        self.fsm = TemplateFSM(
            self_object=self,
            name=self.name, 
            log_transitions=True,
        )
