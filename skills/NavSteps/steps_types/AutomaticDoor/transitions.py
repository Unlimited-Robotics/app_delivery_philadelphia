import typing
if typing.TYPE_CHECKING:
    from src.app import RayaApplication

from ..CommonType import CommonTransitions

from .errors import *
from .constants import *
from .helpers import Helpers


class Transitions(CommonTransitions):

    def __init__(self, app: 'RayaApplication', helpers: Helpers):
        super().__init__(app=app, helpers=helpers)
        self.helpers: Helpers
        self._door_was_close = False


    async def SETUP(self):
        if await self.helpers.detector_ready():
            self.set_state('WAIT_FOR_DOOR_OPEN')
        else:
            self.log.debug('Detector not ready, waiting...')

        
    async def WAIT_FOR_DOOR_OPEN(self):
        tag_visible = await self.helpers.tag_door_visible()
        if not tag_visible:
            if self._door_was_close == True:
                self.app.log.debug('The door is open, Entering the warehouse')
                await self.helpers.custom_cancel_sound()
                await self.helpers.custom_turn_off_leds()
                await self.helpers.gary_play_audio(
                    audio=SOUND_OPEN_DOOR_THANKS,
                    animation_head_leds=LEDS_DOOR_OPENED,
                    wait=True,
                )
                self._door_was_close = False
                # TODO: set last correct ui screen
            self.set_state('NAVIGATE_THROUGH_DOOR')
        else:
            if self._door_was_close == False:
                self.app.log.debug('The door is closed, waiting for it to open')
                try:
                    await self.app.ui.show_animation(
                        **UI_SCREEN_WAIT_FOR_DOOR_OPEN
                    )
                except FileNotFoundError as e:
                    self.log.error(f'Error showing animation: {e}')
                self._door_was_close = True
            else:
                await self.helpers.gary_play_audio(
                    audio=SOUND_OPEN_DOOR_REQUEST,
                )

    
    async def NAVIGATE_THROUGH_DOOR(self):
        if await self.app.nav.is_in_zone(
                zone_name=self.helpers._fsm.step.zone_name
            ) != self.helpers.is_inside_initial_zone:
            # if robot leaves or enters the zone, the skill ends
            self.log.debug('Robot left/enter the zone, ending skill...')
            self.set_state('END')
        
        if not self.app.nav.is_navigating():
            nav_error = self.app.nav.get_last_result()
            # 18 nav was canceled 
            # 116 nav could compute a path
            if nav_error[0] == 0:
                self.set_state('END')
            elif nav_error[0] == 116 and await self.helpers.tag_door_visible():
                self.set_state('WAIT_FOR_DOOR_OPEN')
            else:
                self.log.error(f'Navigation error: \'{nav_error}\'')
                self.set_state('NAVIGATE_THROUGH_DOOR_FAILED')


    async def NAVIGATE_THROUGH_DOOR_FAILED(self):
        self.set_state('NAVIGATE_THROUGH_DOOR')


    async def END(self):
        await super().END()
