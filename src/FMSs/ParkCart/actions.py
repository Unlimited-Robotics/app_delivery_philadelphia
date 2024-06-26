from raya.tools.fsm import BaseActions
from src.app import RayaApplication
from src.static.navigation import *
from src.static.ui import *
from src.static.leds import *
from src.static.fleet import *
from raya.enumerations import FLEET_UPDATE_STATUS, POSITION_UNIT, ANGLE_UNIT

from src.static.constants import *
from .helpers import Helpers

class Actions(BaseActions):

    def __init__(self, app: RayaApplication, helpers: Helpers):
        super().__init__()
        self.app = app
        self.helpers = helpers


    async def enter_ENTER_WAREHOUSE(self):
        await self.app.ui.display_screen(**UI_SCREEN_ENTERING_TO_WAREHOUSE)
        await self.app.nav.navigate_to_position(
            **NAV_CART_POINT,
            callback_feedback_async=self.helpers.nav_feedback_door_async,
            callback_finish_async=self.helpers.nav_finish_async,
        )
        self.helpers.start_timer()


    async def enter_WAIT_FOR_BUTTON_OPEN_ENTRANCE(self):
        await self.app.fleet.update_app_status(
                status=FLEET_UPDATE_STATUS.WARNING,
                message=FLEET_MESSAGE_OPEN_DOOR
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
                message=FLEET_DOOR_OPEN
            )
        await self.app.ui.display_screen(**UI_SCREEN_ENTERING_TO_WAREHOUSE)
        await self.app.nav.navigate_to_position(
            **NAV_CART_POINT,
            callback_feedback_async=self.helpers.nav_feedback_async,
            callback_finish_async=self.helpers.nav_finish_async,
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


    async def WAIT_FOR_UNLOAD_PACKAGE_to_END(self):
        await self.app.sound.cancel_all_sounds()
        await self.app.leds.turn_off_all()
        await self.app.fleet.update_app_status(
                status=FLEET_UPDATE_STATUS.INFO,
                message=FLEET_DOOR_OPEN
            )


    async def aborted(self, error, msg):
        pass
