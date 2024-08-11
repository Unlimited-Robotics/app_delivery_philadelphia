import typing
if typing.TYPE_CHECKING:
    from src.app import RayaApplication

# from ..CommonType import CommonActions
from ...PartialsFSM.RetryState import Actions as RetryActions

from raya.exceptions import RayaNavNotNavigating

from .errors import *
from .constants import *
from .helpers import Helpers

from raya.exceptions import RayaNavAlreadyNavigating

class Actions(RetryActions):

    def __init__(self, app: 'RayaApplication', helpers: Helpers):
        RetryActions.__init__(self=self, app=app, helpers=helpers)
        self.helpers: Helpers


    async def enter_NAVIGATING_TO_POINT(self):
        if self.app.nav.is_navigating():
            point = self.helpers._fsm.step.point.get_only_coordinates()
            self.log.warn('Already navigating')
            self.log.warn(f'Updating current nav goal to: {point}')
            try:
                await self.app.nav.update_current_nav_goal(
                    **point,
                    callback_feedback_async=self.helpers.nav_feedback_async,
                    callback_finish_async=self.helpers.nav_finish_async,
                    wait=False
                )
            except RayaNavNotNavigating:
                point = self.helpers._fsm.step.point.to_dict()
                self.log.debug(f'Navigating to point: {point}')
                await self.app.nav.navigate_to_position(
                    **point,
                    callback_feedback_async=self.helpers.nav_feedback_async,
                    callback_finish_async=self.helpers.nav_finish_async,
                    wait=False
                )
        else:
            point = self.helpers._fsm.step.point.to_dict()
            self.log.debug(f'Navigating to point: {point}')
            try:
                await self.app.nav.navigate_to_position(
                    **point,
                    callback_feedback_async=self.helpers.nav_feedback_async,
                    callback_finish_async=self.helpers.nav_finish_async,
                    wait=False
                )
            except RayaNavAlreadyNavigating:
                self.log.error('RayaNavAlreadyNavigating')
        await self.app.ui.show_animation(
            **self.helpers._fsm.step.custom_ui_screen
        )

    
    async def leave_NAVIGATING_TO_POINT(self):
        await self.helpers.custom_turn_off_leds()
        await self.helpers.custom_cancel_sound()