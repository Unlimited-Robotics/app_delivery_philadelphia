import typing
if typing.TYPE_CHECKING:
    from .main import ManualDoor

from ..CommonType import CommonTypeFSM

from .actions import Actions
from .helpers import Helpers
from .transitions import Transitions

from .states import *
from .constants import *
from .errors import *

class ManualDoorFSM(CommonTypeFSM):
    def __init__(self, *args, **kwarg):
        super().__init__(*args, **kwarg)
        self.step: ManualDoor = self.step
