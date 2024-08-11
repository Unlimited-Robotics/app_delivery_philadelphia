import typing
if typing.TYPE_CHECKING:
    from .main import CommonType

from ...PartialsFSM import CommonFSM
from raya.logger import RaYaLogger

from .actions import CommonActions
from .helpers import CommonHelpers
from .transitions import CommonTransitions

from .states import *
from .constants import *
from .errors import *

class CommonTypeFSM(CommonFSM):
    
    def __init__(self, *args, **kwarg):
        self.step:CommonType = kwarg.pop('self_object')
        super().__init__(*args, **kwarg)
        self.log = RaYaLogger(
            name=self.step.name,
        )
