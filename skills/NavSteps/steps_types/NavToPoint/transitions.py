import typing
import time
if typing.TYPE_CHECKING:
    from src.app import RayaApplication

# from ..CommonType import CommonTransitions
from ...PartialsFSM.RetryState import Transitions as RetryTransitions

from .errors import *
from .constants import *
from .helpers import Helpers


class Transitions(RetryTransitions):

    def __init__(self, app: 'RayaApplication', helpers: Helpers):
        RetryTransitions.__init__(self=self, app=app, helpers=helpers)
        self.helpers: Helpers


    async def SETUP(self):
        self.set_state('NAVIGATING_TO_POINT')


    async def NAVIGATING_TO_POINT(self):
        if self.app.nav.is_navigating():
            if not self.helpers._fsm.step.partial_navigation:
                return
            
            if len(self.helpers._fsm.step.points) == 1:
                return
            
            if self.helpers.remaining_distance == -1:
                return

            if (self.helpers.remaining_distance < \
                    self.helpers._fsm.step.finish_when_distance_less_than
                ):

                self.log.warn((
                    'Distance to point is less than '
                    f'{self.helpers._fsm.step.finish_when_distance_less_than}'
                    ', finishing step'
                ))
                self.set_state('PARTIAL_NAVIGATION_REACHED')
        
        nav_error = self.helpers.get_last_result()
        if nav_error[0] == -1:
            return
        self.log.error(f'nav_error_code: {nav_error}')
        if nav_error[0] == 0:
            if len(self.helpers._fsm.step.points) == 1:
                await self.app.ui.show_last_animation()
                self.set_state('END')
            else:
                self.set_state('PARTIAL_NAVIGATION_REACHED')
        else:
            self.set_state('NAVIGATING_TO_POINT_FAILED')


    async def PARTIAL_NAVIGATION_REACHED(self):
        self.helpers._fsm.step.points.pop(0)
        self.set_state('NAVIGATING_TO_POINT')


    async def NAVIGATING_TO_POINT_FAILED(self):
        if self.helpers._fsm.step.teleoperator_if_fail:
            self.helpers.retry_step(
                last_state='NAVIGATING_TO_POINT',
                timeout=self.helpers._fsm.step.teleoperator_timeout,
                transitions=self,
            )
        else: 
            self.set_state('NAVIGATING_TO_POINT')
