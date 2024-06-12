from raya.tools.fsm import BaseActions
from raya.enumerations import FLEET_UPDATE_STATUS

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
        await self.app.nav.navigate_to_position(
            **NAV_CART_POINT,
            callback_feedback_async=self.helpers.nav_feedback_door_async,
            callback_finish_async=self.helpers.nav_finish_async,
        )
        self.helpers.start_timer()


    async def enter_WAIT_FOR_BUTTON_OPEN_ENTRANCE(self):
        await self.app.fleet.update_app_status(
            status=FLEET_UPDATE_STATUS.INFO,
            message=FLEET_WAIT_FOR_BUTTON_DOOR
        )
        await self.app.ui.display_screen(**UI_SCREEN_WAIT_FOR_DOOR_OPEN)
        await self.app.leds.animation(
            **LEDS_WAIT_FOR_BUTTON_CHEST_BUTTON,
            wait=True
        )

    
    async def leave_WAIT_FOR_BUTTON_OPEN_ENTRANCE(self):
        await self.app.sound.cancel_all_sounds()
        await self.app.leds.turn_off_all()


    async def enter_GO_TO_CART_POINT(self):
        await self.app.fleet.update_app_status(
            status=FLEET_UPDATE_STATUS.INFO,
            message=FLEET_ROBOT_MOVING_TO_DETACH_POINT
        )
        await self.app.ui.display_screen(**UI_SCREEN_ENTERING_TO_WAREHOUSE)
        await self.app.nav.navigate_to_position(
            **NAV_CART_POINT,
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
            callback_feedback=self.helpers.cb_skill_attach_feedback,
            wait=False
        )
        
    
    async def enter_WAIT_FOR_UNLOAD_PACKAGE(self):
        await self.app.fleet.update_app_status(
                status=FLEET_UPDATE_STATUS.WARNING,
                message=FLEET_MESSAGE_WAITING_CART_UNLOAD
            )
        await self.app.ui.display_screen(**UI_SCREEN_WAIT_FOR_CART_UNLOAD)
        await self.app.leds.animation(
            **LEDS_WAIT_FOR_BUTTON_CHEST_BUTTON, 
            wait=True
        )


    async def DETACH_CART_to_END(self):
        await self.app.sound.cancel_all_sounds()
        await self.app.leds.turn_off_all()
        await self.app.fleet.update_app_status(
                status=FLEET_UPDATE_STATUS.INFO,
                message=FLEET_CART_RELEASED
            )


    async def aborted(self, error, msg):
        pass
