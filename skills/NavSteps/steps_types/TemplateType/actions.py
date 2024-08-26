import typing
if typing.TYPE_CHECKING:
    from src.app import RayaApplication

from ..CommonType import CommonActions

from .errors import *
from .constants import *
from .helpers import Helpers


class Actions(CommonActions):

    def __init__(self, app: 'RayaApplication', helpers: Helpers):
        super().__init__(app=app, helpers=helpers)
        self.helpers: Helpers
    