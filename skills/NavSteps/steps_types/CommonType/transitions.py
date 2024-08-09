import typing
if typing.TYPE_CHECKING:
    from src.app import RayaApplication

from ...PartialsFSM.CommonFSM import CommonTransitions

from .errors import *
from .constants import *
from .helpers import Helpers

class Transitions(CommonTransitions):

    def __init__(self, app: 'RayaApplication', helpers: Helpers):
        super().__init__(app=app, helpers=helpers)
