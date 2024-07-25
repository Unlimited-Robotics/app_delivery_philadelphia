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


    async def enter_SELECT_ELEVATOR(self):
        self.helpers.selected_elevator_ui = None
        copy_ui_screen = copy(UI_SCREEN_OPTIONS_ELEVATOR_ENTERING)
        floor = self.app.get_current_target_floor_map_name()
        
        message = copy_ui_screen['title'].replace(
            '[floor]', floor
        )
        copy_ui_screen['title'] = message
        await self.app.ui.display_choice_selector(
            **copy_ui_screen,
            wait=False,
            callback=self.helpers.cb_delivery_arrived_ui_response
        )


    async def enter_NAV_TO_ELEVATOR(self):
        elevator_point = await self.helpers.get_entry_point_to_elevator()
        await self.app.nav.navigate_to_position(
            **elevator_point,
            callback_feedback_async=self.helpers.nav_feedback_async,
            callback_finish_async=self.helpers.nav_finish_async,
        )


    async def enter_TELEOPERATING(self):
        self.helpers.teleoperation_response = None
        await self.app.ui.display_action_screen(
            **UI_CALL_TO_ACTION_TELEOPERATION,
            wait=False,
            callback=self.helpers.cb_teleoperation_ui_response
        )


    async def enter_TELEOPERATION_DONE(self):
        await self.app.ui.display_action_screen(
            **UI_CALL_TO_ACTION_TELEOPERATION_DONE,
            wait=False,
            callback=self.helpers.cb_teleoperation_ui_response
        )


    async def enter_EXIT_FROM_ELEVATOR(self):
        self.helpers.exit_elevator_id = None
        target_floor = self.app.get_current_target_floor_map_name()
        ARGS_EXIT_ELEVATOR['target_floor'] = target_floor
        await self.app.robot_skills.execute_skill(
            **ARGS_EXIT_ELEVATOR,
            callback_feedback_async=self.helpers.cb_exit_elevator_skill_feedback,
            callback_finish_async=self.helpers.cb_exit_elevator_skill_finish,
            wait=False,
        )
        

    async def enter_LOCALIZING(self):
        await self.app.ui.display_screen(**UI_SCREEN_LOCALIZING)


    async def enter_END(self):
        await self.app.ui.show_animation(**UI_SCREEN_NAV_TO_WAREHOUSE)


    async def aborted(self, error, msg):
        pass
