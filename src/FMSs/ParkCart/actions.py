from copy import copy

from src.FMSs.BaseAppFSM.actions import CommonAction
from raya.enumerations import FLEET_UPDATE_STATUS

from src.app import RayaApplication
from src.static.navigation import *
from src.static.ui import *
from src.static.leds import *
from src.static.fleet import *
from src.static.constants import *
from src.static.skills import *

from .helpers import Helpers

class Actions(CommonAction):

    def __init__(self, app: RayaApplication, helpers: Helpers):
        super().__init__(app=app,helpers=helpers)
        self.app = app
        self.helpers = helpers


    async def enter_ENTER_WAREHOUSE(self):
        await self.app.fleet.update_app_status(
            status=FLEET_UPDATE_STATUS.INFO,
            message=FLEET_ENTERING_WAREHOUSE
        )
        await self.app.ui.show_animation(**UI_SCREEN_NAVIGATING)
        point = copy(NAV_WAREHOUSE_EXIT)
        self.app.log.warn(f'NAV_WAREHOUSE_EXIT point: {point}')
        point['angle'] += 180.0
        self.app.log.warn(f'NAV_WAREHOUSE_EXIT new point: {point}')
        await self.app.nav.navigate_to_position(
            **point,
            callback_feedback_async=self.helpers.nav_feedback_wrapper,
            callback_finish_async=self.helpers.nav_finish_async,
        )


    async def enter_WAIT_FOR_ENTRANCE_DOOR_OPEN(self):
        await self.app.fleet.update_app_status(
            status=FLEET_UPDATE_STATUS.INFO,
            message=FLEET_WAIT_FOR_DOOR
        )
        await self.helpers._enable_door_detection()
        await self.app.ui.show_animation(**UI_SCREEN_WAIT_FOR_DOOR_OPEN)


    async def leave_WAIT_FOR_ENTRANCE_DOOR_OPEN(self):
        await self.app.custom_cancel_sound()
        await self.app.custom_turn_off_leds()


    async def enter_GO_TO_CART_POINT(self):
        await self.app.fleet.update_app_status(
            status=FLEET_UPDATE_STATUS.INFO,
            message=FLEET_ROBOT_MOVING_TO_DETACH_POINT
        )
        await self.app.ui.show_animation(**UI_SCREEN_NAVIGATING)
        
        point = copy(NAV_CART_UNLOAD_POINT)
        self.app.log.warn(f'NAV_CART_UNLOAD_POINT point: {point}')
        await self.app.nav.navigate_to_position(
            **point,
            callback_feedback_async=self.helpers.nav_feedback_async,
            callback_finish_async=self.helpers.nav_finish_async,
        )


    async def enter_DETACH_CART(self):
        self.app.log.warn('Releasing cart...')
        await self.app.fleet.update_app_status(
            status=FLEET_UPDATE_STATUS.INFO,
            message=FLEET_ROBOT_DETACHING_TO_CART
        )
        await self.app.ui.display_screen(**UI_SCREEN_RELEASE_CART)
        await self.app.skill_detach.execute_main(
            execute_args=EXECUTION_ARG_DETACH_SKILL,
            callback_done=self.helpers.cb_skill_detach_done,
            callback_feedback=self.helpers.cb_skill_dettach_feedback,
            wait=False
        )


    async def enter_END(self):
        # TODO: disable detector
        await self.helpers._disable_door_detection()
        await self.app.custom_cancel_sound()
        await self.app.custom_turn_off_leds()
        await self.app.fleet.update_app_status(
                status=FLEET_UPDATE_STATUS.INFO,
                message=FLEET_CART_RELEASED
            )


    async def aborted(self, error, msg):
        pass
