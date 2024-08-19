import time
from raya.exceptions import RayaNavLocalizationRejected

from src.static import *

from .helpers import Helpers
from .errors import *
from src.FMSs.BaseAppFSM.transitions import CommonTransitions


class Transitions(CommonTransitions):

    def __init__(self, app, helpers: Helpers):
        super().__init__(app=app, helpers=helpers)
        self.helpers: Helpers


    async def SELECT_ELEVATOR(self):
        if self.helpers.selected_elevator_ui is not None:
            selected_option = self.helpers.selected_elevator_ui
            self.app.log.warn(f'User selected: {selected_option}')
            self.helpers.selected_elevator = str(selected_option)
            self.set_state('NAV_TO_ELEVATOR')


    async def NAV_TO_ELEVATOR(self):
        result = await self.app.skill_nav_steps.wait_main()
        self.app.log.warn(f'skill_template result: {result}')
        await self.app.sleep(TIME_TO_WAIT_AFTER_SELECTION_ELEVATOR)
        self.set_state('TELEOPERATING')

    
    async def TELEOPERATING(self):
        self.set_state('CHANGE_MAP')


    async def CHANGE_MAP(self):
        start_time = time.time()
        map_name = self.helpers.get_current_target_floor_map_name()
        self.log.warn(f'Changing map to: {map_name}')
        try:
            await self.app.nav.set_map(
                map_name=map_name,
                wait_localization=False,
                wait=True,
                callback_feedback=self.helpers.cb_set_map_feedback,
                callback_finish=self.helpers.cb_set_map_finish
            )
        except Exception as e:
            self.app.log.error(f'Error changing map: {e}')
            self.helpers.retry_step(
                transitions=self,
                last_state='TELEOPERATING',
            )
        end_time = time.time()
        self.app.log.warn(
            f'Change map \'{map_name}\' time: {end_time - start_time}'
        )
        self.set_state('TELEOPERATION_DONE')

    
    async def TELEOPERATION_DONE(self):
        self.set_state('EXIT_FROM_ELEVATOR')


    async def EXIT_FROM_ELEVATOR(self):
        if self.helpers.exit_elevator_id is not None:
            self.set_state('LOCALIZING')
        
    
    async def LOCALIZING(self):
        localizing_point = \
            await self.helpers.get_elevator_localization_points(
                rotate_180=self.helpers.try_rotate_localization_points
            )
        localization = False
        for point in localizing_point:
            try:
                self.app.log.debug(f'Localizing on point: {point}')
                await self.app.nav.set_current_pose(
                    **point,
                    wait=True
                )
                localization = True
                self.app.log.warn('Localized')
                self.helpers.current_target_floor_reached()
                self.set_state('END')
            except RayaNavLocalizationRejected as e:
                self.app.log.error(f'Error localizing: {e}')
        
        if localization is False:
            if self.helpers.try_rotate_localization_points:
                self.log.error(
                    'Localization failed, even after rotating 180 degrees'
                )
                self.log.error('Trying again...')
                self.helpers.retry_step(
                    transitions=self,
                    last_state='LOCALIZING',
                )
            else:
                self.set_state('TELEOPERATE_TO_LOCALIZE')


    async def TELEOPERATE_TO_LOCALIZE(self):
        if self.helpers._ui_response_wait_for_help is None:
            return
        
        response = self.helpers._ui_response_wait_for_help
        self.log.warn(f'User selected: {response}')

        if self.helpers._ui_response_wait_for_help is not None:
            if 'action' in self.helpers._ui_response_wait_for_help.keys():
                action = self.helpers._ui_response_wait_for_help['action']
                if action == 'button_clicked':
                    self.set_state('LOCALIZING')
