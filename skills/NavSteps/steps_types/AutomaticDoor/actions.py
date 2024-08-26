import typing
if typing.TYPE_CHECKING:
    from src.app import RayaApplication

from raya.exceptions import RayaNavAlreadyNavigating
from raya.exceptions import RayaTaskNotRunning

from ..CommonType import CommonActions

from .errors import *
from .constants import *
from .helpers import Helpers


class Actions(CommonActions):

    def __init__(self, app: 'RayaApplication', helpers: Helpers):
        super().__init__(app=app, helpers=helpers)
        self.helpers: Helpers
    

    async def enter_SETUP(self):
        self.helpers.withinInitialZone = await self.app.nav.is_in_zone(
                zone_name=self.helpers._fsm.step.zone_name
            )
        await self.helpers.enable_cameras()
        await self.helpers._enable_door_detection()


    async def enter_WAIT_FOR_DOOR_OPEN(self):
        self.log.debug('Creating task for calling the user')
        self.app.create_task(
            name=self.helpers.task_timer_call_for_help,
            afunc=self.helpers.call_task
        )


    async def leave_WAIT_FOR_DOOR_OPEN(self):
        try:
            self.app.cancel_task(name=self.helpers.task_timer_call_for_help)
            self.log.warn('Task for calling the user was canceled')
        except RayaTaskNotRunning:
            pass


    async def enter_NAVIGATE_THROUGH_DOOR(self):
        point = self.helpers._fsm.step.after_door_point.to_dict()
        self.log.debug(f'Navigating to point: {point}')
        try:
            await self.app.nav.navigate_to_position(
                **point,
                callback_feedback_async=self.helpers.nav_feedback_async,
                callback_finish_async=self.helpers.nav_finish_async,
            )
        except RayaNavAlreadyNavigating:
            self.log.error('RayaNavAlreadyNavigating')
        await self.app.ui.show_last_animation()

    
    async def leave_NAVIGATE_THROUGH_DOOR(self):
        pass

    
    async def enter_END(self):
        self.log.debug('Entering END')
        await self.helpers._disable_door_detection()
        await self.helpers.disable_cameras()
