import typing
if typing.TYPE_CHECKING:
    from src.app import RayaApplication
    from . import TemplateFSM

from ..CommonType import CommonHelpers

from .errors import *
from .constants import *


class Helpers(CommonHelpers):

    def __init__(self, app: 'RayaApplication'):
        super().__init__(app=app)
        self._fsm: TemplateFSM = None
