import typing
if typing.TYPE_CHECKING:
    from src.app import RayaApplication

from ..CommonType import CommonTransitions

from .errors import *
from .constants import *
from .helpers import Helpers


class Transitions(CommonTransitions):

    def __init__(self, app: 'RayaApplication', helpers: Helpers):
        super().__init__(app=app, helpers=helpers)
        self.helpers: Helpers


    async def SETUP(self):
        self.set_state('TELEOPERATION')


    async def TELEOPERATION(self):
        if self.helpers.teleoperation_response is not None:
            if 'action' in self.helpers.teleoperation_response.keys():
                action = self.helpers.teleoperation_response['action']
                if action == 'button_clicked':
                    self.set_state('END')


    async def END(self):
        pass