from copy import copy

from raya.tools.fsm import BaseActions
from raya.enumerations import FLEET_UPDATE_STATUS
from raya.exceptions import RayaCommandAlreadyRunning

from src.app import RayaApplication
from src.static.navigation import *
from src.static.ui import *
from src.static.leds import *
from src.static.fleet import *
from src.static.constants import *
from src.static.skills import *

from .helpers import Helpers

class Actions(BaseActions):

    def __init__(self, app: RayaApplication, helpers: Helpers):
        super().__init__()
        self.app = app
        self.helpers = helpers


    async def enter_ENTER_WAREHOUSE(self):
        await self.app.fleet.update_app_status(
            status=FLEET_UPDATE_STATUS.INFO,
            message=FLEET_ENTERING_WAREHOUSE
        )
        await self.app.ui.display_screen(**UI_SCREEN_ENTERING_TO_WAREHOUSE)
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
        await self.app.ui.display_screen(**UI_SCREEN_WAIT_FOR_DOOR_OPEN)


    async def leave_WAIT_FOR_ENTRANCE_DOOR_OPEN(self):
        await self.app.sound.cancel_all_sounds()
        try:
            await self.app.leds.turn_off_all()
        except RayaCommandAlreadyRunning:
            pass


    async def enter_GO_TO_CART_POINT(self):
        await self.app.fleet.update_app_status(
            status=FLEET_UPDATE_STATUS.INFO,
            message=FLEET_ROBOT_MOVING_TO_DETACH_POINT
        )
        await self.app.ui.display_screen(**UI_SCREEN_ENTERING_TO_WAREHOUSE)
        
        point = copy(NAV_CART_POINT)
        self.app.log.warn(f'NAV_CART_POINT point: {point}')
        point['angle'] += 180.0
        self.app.log.warn(f'NAV_CART_POINT point: {point}')
        await self.app.nav.navigate_to_position(
            **point,
            callback_feedback_async=self.helpers.nav_feedback_async,
            callback_finish_async=self.helpers.nav_finish_async,
        )


    async def enter_DETACH_CART(self):
        await self.app.fleet.update_app_status(
            status=FLEET_UPDATE_STATUS.INFO,
            message=FLEET_ROBOT_DETACHING_TO_CART
        )
        await self.app.skill_detach.execute_main(
            execute_args=EXECUTION_ARG_DETACH_SKILL,
            callback_done=self.helpers.cb_skill_detach_done,
            callback_feedback=self.helpers.cb_skill_dettach_feedback,
            wait=False
        )
        
    
    async def enter_WAIT_FOR_UNLOAD_PACKAGE(self):
        self.helpers.reset_chest_button()
        await self.app.fleet.update_app_status(
                status=FLEET_UPDATE_STATUS.WARNING,
                message=FLEET_MESSAGE_WAITING_CART_UNLOAD
            )
        await self.app.ui.display_screen(**UI_SCREEN_WAIT_FOR_CART_UNLOAD)
        try:
            await self.app.leds.animation(
                **LEDS_WAIT_FOR_BUTTON_CHEST_BUTTON, 
                wait=True
            )
        except RayaCommandAlreadyRunning:
            pass


    async def enter_END(self):
        # TODO: disable detector
        await self.helpers._disable_door_detection()
        await self.app.sound.cancel_all_sounds()
        try:
            await self.app.leds.turn_off_all()
        except RayaCommandAlreadyRunning:
            pass
        await self.app.fleet.update_app_status(
                status=FLEET_UPDATE_STATUS.INFO,
                message=FLEET_CART_RELEASED
            )


    async def aborted(self, error, msg):
        pass
