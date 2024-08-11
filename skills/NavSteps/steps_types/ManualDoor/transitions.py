import typing
if typing.TYPE_CHECKING:
    from src.app import RayaApplication

from ..AutomaticDoor import Transitions as AutomaticDoorTransitions

from .errors import *
from .constants import *
from .helpers import Helpers


class Transitions(AutomaticDoorTransitions):

    def __init__(self, app: 'RayaApplication', helpers: Helpers):
        super().__init__(app=app, helpers=helpers)
        self.helpers: Helpers


    async def SETUP(self):
        await super().SETUP()


    async def WAIT_FOR_DOOR_OPEN(self):
        await super().WAIT_FOR_DOOR_OPEN()
        if await self.helpers.check_door_close_timeout():
            self.set_state('CALL_FOR_HELP')


    async def CALL_FOR_HELP(self):
        if not await self.helpers.tag_door_visible():
            self.set_state('NAVIGATE_THROUGH_DOOR') 


    async def NAVIGATE_THROUGH_DOOR(self):
        await super().NAVIGATE_THROUGH_DOOR()


    async def NAVIGATE_THROUGH_DOOR_FAILED(self):
        await super().NAVIGATE_THROUGH_DOOR_FAILED()


    async def END(self):
        await super().END()
