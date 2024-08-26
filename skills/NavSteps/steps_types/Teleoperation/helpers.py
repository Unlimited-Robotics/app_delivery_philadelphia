import typing
if typing.TYPE_CHECKING:
    from src.app import RayaApplication
    from . import TeleoperationFSM

from ..CommonType import CommonHelpers

from .errors import *
from .constants import *


class Helpers(CommonHelpers):

    def __init__(self, app: 'RayaApplication'):
        super().__init__(app=app)
        self._fsm: TeleoperationFSM = None
        self.teleoperation_response = None


    def cb_teleoperation_ui_response(self, response):
        self.teleoperation_response = response
    
    