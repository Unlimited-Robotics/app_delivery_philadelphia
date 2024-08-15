from copy import deepcopy

from src.FMSs.BaseAppFSM.actions import CommonAction
from raya.enumerations import FLEET_UPDATE_STATUS

from src.static.navigation import *
from src.static.ui import *
from src.static.leds import *
from src.static.fleet import *
from src.static.constants import *
from src.static.skills import *

from .helpers import Helpers

class Actions(CommonAction):

    def __init__(self, app, helpers: Helpers):
        super().__init__(app=app,helpers=helpers)
        self.helpers: Helpers


    async def enter_GO_TO_DETACH_CART_POINT(self):
        execute_args = {
            'steps': SKILL_NAVIGATION['00']['elev_detach']
        }
        await self.app.skill_nav_steps.execute_main(
            execute_args=execute_args,
            callback_done=self.helpers.cb_skill_done,
            callback_feedback=self.helpers.cb_skill_feedback,
            wait=False
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


    async def enter_GO_TO_HOME_LOCATION(self):
        await self.app.set_gary_footprint(
            footprint=GARY_FOOTPRINT
        )
        
        home_steps = deepcopy(BASEMENT_ROUTES['home'])
        home_steps[0]['point'] = await self.helpers.get_home_position()
        execute_args = {
            'steps': home_steps
        }
        await self.app.skill_nav_steps.execute_main(
            execute_args=execute_args,
            callback_done=self.helpers.cb_skill_done,
            callback_feedback=self.helpers.cb_skill_feedback,
            wait=False
        )


    async def enter_END(self):
        await self.helpers.custom_cancel_sound()
        await self.helpers.custom_turn_off_leds()
        await self.app.fleet.update_app_status(
                status=FLEET_UPDATE_STATUS.INFO,
                message=FLEET_CART_RELEASED
            )


    async def aborted(self, error, msg):
        pass
