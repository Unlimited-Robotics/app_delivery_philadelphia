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
        
        try:
            await self.app.leds.animation(**LEDS_WAITING_FOR_USER_INPUT, wait=False)
        except Exception as e:
            self.log.error(f'animation exception {type(e)}')


    async def enter_NAV_TO_ELEVATOR(self):
        await self.helpers.show_navigating_to_floor()
        
        elevator_point = await self.helpers.get_entry_point_to_elevator()

        # await self.app.ui.show_last_animation()

        try:
            await self.app.leds.animation(**LEDS_NAVIGATING, wait=False)
        except Exception as e:
            self.log.error(f'animation exception {type(e)}')
        
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
        if not self.app.only_ui:
            await self.app.skill_nav_steps.execute_main(
                execute_args=execute_args,
                callback_done=self.helpers.cb_nav_skill_done,
                callback_feedback=self.helpers.cb_nav_skill_feedback,
                wait=False
            )
        else:
            self.app.create_timer('fake_nav', 5.0)
        


    async def enter_TELEOPERATING(self):
        self.helpers.teleoperation_response = None
        await self.app.ui.show_animation(
                **UI_SCREEN_TELEOPERATION,
                dont_save_last_ui=True,
            )
        try:
            await self.app.leds.animation(**LEDS_BEING_TELEOPERATED, wait=False)
        except Exception as e:
            self.log.error(f'animation exception {type(e)}')


    async def enter_CHANGE_MAP(self):
        if self.app.only_ui:
            self.app.create_timer('fake_change_map', 5.0)


    async def enter_EXIT_FROM_ELEVATOR(self):
        self.helpers.try_rotate_localization_points = False
        # await self.helpers.show_navigating_to_floor()
        await self.app.ui.show_last_animation()
        try:
            await self.app.leds.animation(**LEDS_NAVIGATING, wait=False)
        except Exception as e:
            self.log.error(f'animation exception {type(e)}')
        
        self.helpers.exit_elevator_id = None
        target_floor = self.helpers.get_current_target_floor_number()
        ARGS_EXIT_ELEVATOR['target_floor'] = target_floor

        if not self.app.only_ui:
            await self.app.robot_skills.execute_skill(
                **ARGS_EXIT_ELEVATOR,
                callback_feedback_async=self.helpers.cb_exit_elevator_skill_feedback,
                callback_finish_async=self.helpers.cb_exit_elevator_skill_finish,
                wait=False,
            )
        else:
            self.app.create_timer('fake_exit_elevator', 5.0)
    

    async def leave_EXIT_FROM_ELEVATOR(self):
        if self.app.only_ui:
            self.helpers.first_fake_localize_try = True
        

    async def enter_LOCALIZING(self):
        await self.app.ui.display_screen(**UI_SCREEN_LOCALIZING)
        try:
            await self.app.leds.animation(**LEDS_LOCALIZING, wait=False)
        except Exception as e:
            self.log.error(f'animation exception {type(e)}')
        if self.app.only_ui:
            self.app.create_timer('fake_localizing', 5.0)

    
    async def leave_LOCALIZING(self):
        if self.app.only_ui:
            self.helpers.first_fake_localize_try = False


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
            dont_save_last_ui=False
        )


    async def aborted(self, error, msg):
        pass
