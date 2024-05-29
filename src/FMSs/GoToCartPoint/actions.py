from raya.tools.fsm import BaseActions
from src.app import RayaApplication
from src.static.navigation import *
from src.static.ui import *

from .helpers import Helpers

class Actions(BaseActions):

    def __init__(self, app: RayaApplication, helpers: Helpers):
        super().__init__()
        self.app = app
        self.helpers = helpers

    
    async def enter_GO_TO_WAREHOUSE_ENTRANCE(self):
        await self.app.ui.display_screen(**UI_SCREEN_NAV_TO_WAREHOUSE)
        await self.app.nav.navigate_to_position(
            **NAV_WAREHOUSE_ENTRANCE,
            callback_feedback_async=self.helpers.nav_feedback_async,
            callback_finish_async=self.helpers.nav_finish_async,
        )
        
    async def enter_ENTER_WAREHOUSE(self):
        await self.app.ui.display_screen(**UI_SCREEN_ENTERING_TO_WAREHOUSE)
        await self.app.nav.navigate_to_position(
            **NAV_WAREHOUSE_EXIT,
            callback_feedback_async=self.helpers.nav_feedback_door_async,
            callback_finish_async=self.helpers.nav_finish_async,
        )
    
    async def enter_WAIT_FOR_BUTTON_OPEN_ENTRANCE(self):
        await self.app.ui.display_screen(**UI_SCREEN_WAIT_FOR_DOOR_OPEN)


    async def enter_GO_TO_CART_POINT(self):
        await self.app.ui.display_screen(**UI_SCREEN_ENTERING_TO_WAREHOUSE)
        await self.app.nav.navigate_to_position(
            **NAV_CART_POINT,
            callback_feedback_async=self.helpers.nav_feedback_async,
            callback_finish_async=self.helpers.nav_finish_async,
        )


    async def enter_WAIT_FOR_LOAD_PACKAGE(self):
        await self.app.ui.display_screen(**UI_SCREEN_WAIT_FOR_PACKAGE_LOAD)

    
    async def enter_GO_TO_WAREHOUSE_EXIT(self):
        await self.app.ui.display_screen(**UI_SCREEN_NAV_TO_WAREHOUSE_EXIT)
        await self.app.nav.navigate_to_position(
            **NAV_WAREHOUSE_EXIT,
            callback_feedback_async=self.helpers.nav_feedback_async,
            callback_finish_async=self.helpers.nav_finish_async,
        )
    
    async def enter_LEAVE_WAREHOUSE(self):
        package = self.app.locations[0]
        point = {
            'x': package[0],
            'y': package[1],
            'angle': package[2],
            'pos_unit': POSITION_UNIT.PIXELS, 
            'ang_unit': ANGLE_UNIT.DEGREES,
        }
        await self.app.ui.display_screen(**UI_SCREEN_LEAVE_WAREHOUSE)
        await self.app.nav.navigate_to_position(
            **point,
            callback_feedback_async=self.helpers.nav_feedback_door_async,
            callback_finish_async=self.helpers.nav_finish_async,
        )


    async def enter_WAIT_FOR_BUTTON_EXITING(self):
        await self.app.ui.display_screen(**UI_SCREEN_WAIT_FOR_DOOR_OPEN)


    async def aborted(self, error, msg):
        pass
