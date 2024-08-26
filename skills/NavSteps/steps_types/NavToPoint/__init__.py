import typing
if typing.TYPE_CHECKING:
    from .main import NavToPoint

from ..CommonType import CommonTypeFSM

from .actions import Actions
from .helpers import Helpers
from .transitions import Transitions

from .states import *
from .constants import *
from .errors import *

class NavToPointFSM(CommonTypeFSM):
    
    def __init__(self, *args, **kwarg):
        super().__init__(*args, **kwarg)
        self.step: NavToPoint = self.step
