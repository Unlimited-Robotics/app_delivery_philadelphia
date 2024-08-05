from copy import copy
from src.FMSs.BaseAppFSM.actions import CommonAction
from raya.enumerations import FLEET_UPDATE_STATUS, POSITION_UNIT, ANGLE_UNIT

from src.app import RayaApplication
from src.static.skills import *
from src.static.navigation import *
from src.static.ui import *
from src.static.leds import *
from src.static.fleet import *
from src.static.constants import *
from .helpers import Helpers

class Actions(CommonAction):

    def __init__(self, app: RayaApplication, helpers: Helpers):
        super().__init__(app=app,helpers=helpers)
        self.app = app
        self.helpers = helpers


    async def enter_GO_TO_HOME_LOCATION(self):
        await self.app.fleet.update_app_status(
            status=FLEET_UPDATE_STATUS.INFO,
            message=FLEET_ROBOT_NAVIGATING_TO_HOME
        )
        await self.app.ui.show_animation(**UI_SCREEN_NAVIGATING)
        home = await self.helpers.get_home_position()
        await self.app.nav.navigate_to_position(
            **home,
            callback_feedback_async=self.helpers.nav_feedback_async,
            callback_finish_async=self.helpers.nav_finish_async,
            wait=False
        )


    async def enter_GO_TO_CART_POINT(self):
        await self.app.fleet.update_app_status(
            status=FLEET_UPDATE_STATUS.INFO,
            message=FLEET_ROBOT_MOVING_TO_ATTACH_POINT
        )
        await self.app.ui.show_animation(**UI_SCREEN_NAVIGATING)
        cart_location = await self.helpers.get_cart_load_point()
        self.app.log.debug(f'navigate_to_position {cart_location}')
        await self.app.nav.navigate_to_position(
            **cart_location,
            callback_feedback_async=self.helpers.nav_feedback_async,
            callback_finish_async=self.helpers.nav_finish_async,
        )


    async def enter_ATTACH_TO_CART(self):
        EXECUTION_ARG_ATTACH_SKILL['target_tags'] = [self.app.cart_number]
        
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


    async def enter_GO_TO_ELEVATOR(self):
        point = await self.helpers.get_elevator_waiting_point()
        copy_ui_screen = copy(UI_SCREEN_NAV_TO_PACKAGE_POINT)
        current_package_location_name = self.helpers.current_package['map_name']
        message = copy_ui_screen['title'].replace(
            '[department_name]', 
            current_package_location_name
        )
        copy_ui_screen['title'] = message
        # TODO add ui screen for elevator
        
        execute_args = {
            'steps': SKILL_NAVIGATION['home_elev']
        }
        await self.app.skill_nav_steps.execute_main(
            execute_args=execute_args,
            callback_done=self.helpers.cb_skill_done,
            callback_feedback=self.helpers.cb_skill_feedback,
            wait=False
        )


    async def aborted(self, error, msg):
        pass
