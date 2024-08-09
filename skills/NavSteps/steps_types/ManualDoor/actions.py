import typing
if typing.TYPE_CHECKING:
    from src.app import RayaApplication

from raya.exceptions import RayaTaskNotRunning

from ..AutomaticDoor import Actions as AutomaticDoorActions
from .errors import *
from .constants import *
from .helpers import Helpers


class Actions(AutomaticDoorActions):

    def __init__(self, app: 'RayaApplication', helpers: Helpers):
        super().__init__(app=app, helpers=helpers)
        self.helpers: Helpers

    
    async def enter_SETUP(self):
        await super().enter_SETUP()


    async def enter_WAIT_FOR_DOOR_OPEN(self):
        await super().enter_WAIT_FOR_DOOR_OPEN()
        await self.helpers.start_door_close_timeout()


    async def leave_WAIT_FOR_DOOR_OPEN(self):
        await super().leave_WAIT_FOR_DOOR_OPEN()


    async def enter_CALL_FOR_HELP(self):
        self.log.debug('Creating task for calling the user')
        self.app.create_task(
            name=self.helpers.task_timer_call_for_help,
            afunc=self.helpers.call_task
        )


    async def leave_CALL_FOR_HELP(self):
        try:
            self.app.cancel_task(name=self.helpers.task_timer_call_for_help)
        except RayaTaskNotRunning:
            pass


    async def enter_NAVIGATE_THROUGH_DOOR(self):    
        await super().enter_NAVIGATE_THROUGH_DOOR()

    
    async def leave_NAVIGATE_THROUGH_DOOR(self):
        await super().leave_NAVIGATE_THROUGH_DOOR()


    async def enter_END(self):
        await super().enter_END()
