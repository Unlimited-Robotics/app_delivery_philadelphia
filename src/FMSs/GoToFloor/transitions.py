import time
from raya.exceptions import RayaNavLocalizationRejected

from src.app import RayaApplication
from src.static import *

from .helpers import Helpers
from .errors import *
from src.FMSs.BaseAppFSM.transitions import CommonTransitions


class Transitions(CommonTransitions):

    def __init__(self, app: RayaApplication, helpers: Helpers):
        super().__init__(app=app, helpers=helpers)
        self.app = app
        self.helpers = helpers


    async def SELECT_ELEVATOR(self):
        if self.helpers.selected_elevator_ui is not None:
            selected_option = self.helpers.selected_elevator_ui
            self.app.log.warn(f'User selected: {selected_option}')
            self.helpers.selected_elevator = str(selected_option)
            self.set_state('NAV_TO_ELEVATOR')


    async def NAV_TO_ELEVATOR(self):
        if not self.app.nav.is_navigating():
            nav_error = self.app.nav.get_last_result()
            if nav_error[0] == 0:
                self.set_state('TELEOPERATING')
            else:
                self.helpers.set_state_wrapper(
                    new_state='REQUEST_FOR_HELP',
                    last_state='SELECT_ELEVATOR',
                    transitions=self
                )

    
    async def TELEOPERATING(self):
        self.set_state('CHANGE_MAP')


    async def CHANGE_MAP(self):
        start_time = time.time()
        try:
            await self.app.nav.set_map(
                map_name=self.helpers.current_package['map_name'],
                wait_localization=False,
                wait=True,
                callback_feedback=self.helpers.cb_set_map_feedback,
                callback_finish=self.helpers.cb_set_map_finish
            )
        except Exception as e:
            self.app.log.error(f'Error changing map: {e}')
            self.helpers.set_state_wrapper(
                new_state='REQUEST_FOR_HELP',
                last_state='TELEOPERATING',
                transitions=self
            )
        end_time = time.time()
        self.app.log.warn(f'Change map time: {end_time - start_time}')
        self.set_state('TELEOPERATION_DONE')

    
    async def TELEOPERATION_DONE(self):
        if self.helpers.teleoperation_response is not None:
            if 'action' in self.helpers.teleoperation_response.keys():
                action = self.helpers.teleoperation_response['action']
                if action == 'button_clicked':
                    self.set_state('SELECT_EXIT_FROM_ELEVATOR_NUMBER')


    async def SELECT_EXIT_FROM_ELEVATOR_NUMBER(self):
        if self.helpers.selected_elevator_ui is not None:
            selected_option = self.helpers.selected_elevator_ui
            self.app.log.warn(f'User selected: {selected_option}')
            self.helpers.selected_elevator = str(selected_option)
            self.set_state('LOCALIZING')
        
    
    async def LOCALIZING(self):
        localizing_point = await self.helpers.get_elevator_localization_points()
        try:
            result = await self.app.nav.set_current_pose(
                **localizing_point,
                wait=True
            )
            self.app.log.warn(f'Localizing result: {result}')
            self.app.current_target_floor_reached()
            self.set_state('END')
        except RayaNavLocalizationRejected as e:
            self.app.log.error(f'Error localizing: {e}')
            self.helpers.set_state_wrapper(
                new_state='REQUEST_FOR_HELP',
                last_state='SELECT_EXIT_FROM_ELEVATOR_NUMBER',
                transitions=self
            )

        
    async def END(self):
        pass
