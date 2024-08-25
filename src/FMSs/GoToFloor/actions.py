from copy import deepcopy

from src.FMSs.BaseAppFSM.actions import CommonAction

from src.static import *

from .helpers import Helpers

class Actions(CommonAction):

    def __init__(self, app, helpers: Helpers):
        super().__init__(app=app, helpers=helpers)
        self.helpers: Helpers


    async def enter_SELECT_ELEVATOR(self):
        self.helpers.selected_elevator_ui = None
        copy_ui_screen = deepcopy(UI_SCREEN_OPTIONS_ELEVATOR_ENTERING)
        floor = self.helpers.get_current_target_floor_number()
        
        message = copy_ui_screen['title'].replace(
            '[floor]', floor
        )
        copy_ui_screen['title'] = message
        
        await self.app.ui.display_choice_selector(
            **copy_ui_screen,
            wait=False,
            callback=self.helpers.cb_delivery_arrived_ui_response,
            dont_save_last_ui=False,
        )


    async def enter_NAV_TO_ELEVATOR(self):
        await self.helpers.show_navigating_to_floor()
        
        elevator_point = await self.helpers.get_entry_point_to_elevator()

        await self.app.ui.show_last_animation()
        
        execute_args = {
            'steps': [
                {
                    'name': 'Navigation to elevator',
                    'type': 'nav_to_point',
                    'point' : elevator_point,
                    'teleoperator_if_fail': False,
                },
            ]
        }
        await self.app.skill_nav_steps.execute_main(
            execute_args=execute_args,
            callback_done=self.helpers.cb_nav_skill_done,
            callback_feedback=self.helpers.cb_nav_skill_feedback,
            wait=False
        )
        


    async def enter_TELEOPERATING(self):
        self.helpers.teleoperation_response = None
        await self.app.ui.show_animation(
                **UI_SCREEN_TELEOPERATION,
                dont_save_last_ui=True,
            )


    async def enter_EXIT_FROM_ELEVATOR(self):
        self.helpers.try_rotate_localization_points = False
        await self.helpers.show_navigating_to_floor()
        
        self.helpers.exit_elevator_id = None
        target_floor = self.helpers.get_current_target_floor_number()
        ARGS_EXIT_ELEVATOR['target_floor'] = target_floor
        await self.app.robot_skills.execute_skill(
            **ARGS_EXIT_ELEVATOR,
            callback_feedback_async=self.helpers.cb_exit_elevator_skill_feedback,
            callback_finish_async=self.helpers.cb_exit_elevator_skill_finish,
            wait=False,
        )
        

    async def enter_LOCALIZING(self):
        await self.app.ui.display_screen(**UI_SCREEN_LOCALIZING)


    async def enter_TELEOPERATE_TO_LOCALIZE(self):
        self.helpers._ui_response_wait_for_help = None
        self.log.warn(
            'The localization points are going to be rotated 180 degrees !!!!'
        )
        self.helpers.try_rotate_localization_points = True
        await self.app.ui.display_action_screen(
            **UI_CALL_TO_ACTION_TELEOPERATION_DONE,
            wait=False,
            async_callback=self.helpers.ui_action_screen_callback,
            dont_save_last_ui=True
        )


    async def aborted(self, error, msg):
        pass
