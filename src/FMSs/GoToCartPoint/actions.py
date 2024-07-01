from raya.tools.fsm import BaseActions
from raya.enumerations import FLEET_UPDATE_STATUS, POSITION_UNIT, ANGLE_UNIT

from src.app import RayaApplication
from src.static.skills import *
from src.static.navigation import *
from src.static.ui import *
from src.static.leds import *
from src.static.fleet import *
from src.static.constants import *
from .helpers import Helpers
from raya.exceptions import RayaCommandAlreadyRunning

class Actions(BaseActions):

    def __init__(self, app: RayaApplication, helpers: Helpers):
        super().__init__()
        self.app = app
        self.helpers = helpers

    
    async def enter_GO_TO_WAREHOUSE_ENTRANCE(self):
        await self.app.fleet.update_app_status(
            status=FLEET_UPDATE_STATUS.INFO,
            message=FLEET_GOING_TO_WAREHOUSE_ENTRANCE
        )
        await self.app.ui.display_screen(**UI_SCREEN_NAV_TO_WAREHOUSE)
        await self.app.nav.navigate_to_position(
            **NAV_WAREHOUSE_ENTRANCE,
            callback_feedback_async=self.helpers.nav_feedback_async,
            callback_finish_async=self.helpers.nav_finish_async,
        )


    async def enter_ENTER_WAREHOUSE(self):
        await self.app.fleet.update_app_status(
            status=FLEET_UPDATE_STATUS.INFO,
            message=FLEET_ENTERING_WAREHOUSE
        )
        await self.app.ui.display_screen(**UI_SCREEN_ENTERING_TO_WAREHOUSE)
        await self.app.nav.navigate_to_location(
            location_name=NAV_HOME_POSITION_NAME,
            **NAVIGATION_OPTIONS,
            callback_feedback_async=self.helpers.nav_feedback_wrapper,
            callback_finish_async=self.helpers.nav_finish_async,
            wait=False
        )
        self.helpers.start_timer()


    async def enter_WAIT_FOR_BUTTON_OPEN_ENTRANCE(self):
        self.helpers.reset_chest_button()
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
        try:
            await self.app.leds.turn_off_all()
        except RayaCommandAlreadyRunning:
            pass


    async def enter_GO_TO_HOME_LOCATION(self):
        await self.app.fleet.update_app_status(
            status=FLEET_UPDATE_STATUS.INFO,
            message=FLEET_ROBOT_NAVIGATING_TO_HOME
        )
        await self.app.ui.display_screen(**UI_SCREEN_NAV_TO_HOME)
        await self.app.nav.navigate_to_location(
            location_name=NAV_HOME_POSITION_NAME,
            **NAVIGATION_OPTIONS,
            callback_feedback_async=self.helpers.nav_feedback_async,
            callback_finish_async=self.helpers.nav_finish_async,
            wait=False
        )


    async def enter_GO_TO_CART_POINT(self):
        await self.app.fleet.update_app_status(
            status=FLEET_UPDATE_STATUS.INFO,
            message=FLEET_ROBOT_MOVING_TO_ATTACH_POINT
        )
        await self.app.ui.display_screen(**UI_SCREEN_ENTERING_TO_WAREHOUSE)
        self.app.log.debug(f'navigate_to_position {NAV_CART_POINT}')
        await self.app.nav.navigate_to_position(
            **NAV_CART_POINT,
            callback_feedback_async=self.helpers.nav_feedback_async,
            callback_finish_async=self.helpers.nav_finish_async,
        )


    async def enter_ATTACH_TO_CART(self):
        await self.app.fleet.update_app_status(
            status=FLEET_UPDATE_STATUS.INFO,
            message=FLEET_ROBOT_ATTACHING_TO_CART
        )
        await self.app.skill_att2cart.execute_main(
            execute_args=EXECUTION_ARG_ATTACH_SKILL,
            callback_done=self.helpers.cb_skill_attach_done,
            callback_feedback=self.helpers.cb_skill_attach_feedback,
            wait=False
        )


    async def enter_WAIT_FOR_LOAD_PACKAGE(self):
        # TODO: attach skill should do this?
        await self.app.set_gary_footprint(
            footprint=GARY_SELECTED_CART_FOOTPRINT
        )
        
        self.helpers.reset_chest_button()
        await self.app.fleet.update_app_status(
                status=FLEET_UPDATE_STATUS.WARNING,
                message=FLEET_MESSAGE_WAITING_PACKAGE_LOAD
            )
        await self.app.ui.display_screen(**UI_SCREEN_WAIT_FOR_PACKAGE_LOAD)
        await self.app.leds.animation(
            **LEDS_WAIT_FOR_BUTTON_CHEST_BUTTON, 
            wait=True
        )


    async def leave_WAIT_FOR_LOAD_PACKAGE(self):
        await self.app.sound.cancel_all_sounds()
        try:
            await self.app.leds.turn_off_all()
        except RayaCommandAlreadyRunning:
            pass

    
    async def enter_GO_TO_WAREHOUSE_EXIT(self):
        await self.app.fleet.update_app_status(
            status=FLEET_UPDATE_STATUS.INFO,
            message=FLEET_GOING_TO_WAREHOUSE_EXIT
        )
        await self.app.ui.display_screen(**UI_SCREEN_NAV_TO_WAREHOUSE_EXIT)
        await self.app.nav.navigate_to_position(
            **NAV_WAREHOUSE_EXIT,
            callback_feedback_async=self.helpers.nav_feedback_async,
            callback_finish_async=self.helpers.nav_finish_async,
        )


    async def enter_LEAVE_WAREHOUSE(self):
        await self.app.fleet.update_app_status(
            status=FLEET_UPDATE_STATUS.INFO,
            message=FLEET_LEAVING_WAREHOUSE
        )
        package = self.app.locations[0]
        point = {
            'x': package[0],
            'y': package[1],
            'angle': package[2],
            'pos_unit': POSITION_UNIT.PIXELS, 
            'ang_unit': ANGLE_UNIT.DEGREES,
            **NAVIGATION_OPTIONS
        }
        text = (   
            f'Delivering package 1 of {len(self.app.locations)}'
        )
        UI_SCREEN_LEAVE_WAREHOUSE['subtitle'] = text
        await self.app.ui.display_screen(**UI_SCREEN_LEAVE_WAREHOUSE)
        await self.app.nav.navigate_to_position(
            **point,
            callback_feedback_async=self.helpers.nav_feedback_wrapper,
            callback_finish_async=self.helpers.nav_finish_async,
        )
        self.helpers.start_timer()


    async def enter_WAIT_FOR_BUTTON_EXITING(self):
        self.helpers.reset_chest_button()
        await self.app.fleet.update_app_status(
            status=FLEET_UPDATE_STATUS.INFO,
            message=FLEET_WAIT_FOR_BUTTON_DOOR
        )
        await self.app.ui.display_screen(**UI_SCREEN_WAIT_FOR_DOOR_OPEN)
        await self.app.leds.animation(
            **LEDS_WAIT_FOR_BUTTON_CHEST_BUTTON,
            wait=True
        )


    async def leave_WAIT_FOR_BUTTON_EXITING(self):
        await self.app.sound.cancel_all_sounds()
        try:
            await self.app.leds.turn_off_all()
        except RayaCommandAlreadyRunning:
            pass


    async def LEAVE_WAREHOUSE_to_END(self):
        await self.app.fleet.update_app_status(
            status=FLEET_UPDATE_STATUS.INFO,
            message=FLEET_ROBOT_OUTSIDE_WAREHOUSE
        )
        pass


    async def aborted(self, error, msg):
        pass
