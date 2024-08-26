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
        tag_visible = await self.helpers.tag_door_visible(
            default_tag=self.helpers._fsm.step.tags_ids[0]
        )
        if not tag_visible:
            if self._door_was_close == True:
                self.app.log.debug(
                    'The door is open, navigating through it...'
                )
                SOUND_THANKS_DOOR_AUDIO['name'] = \
                    self.helpers._fsm.step.sound_thanks_door_name
                LEDS_DOOR_OPENED['animation'] = \
                    self.helpers._fsm.step.leds_door_open_animation
                await self.helpers.gary_play_audio_predefined(
                    audio=SOUND_THANKS_DOOR_AUDIO,
                    animation_head_leds=LEDS_DOOR_OPENED,
                )
                self._door_was_close = False
                self.log.debug('Before the door delay!')
                await self.app.sleep(
                        self.helpers._fsm.step.delay_after_door_opened
                    )
                self.log.debug('After the door delay!')
            self.set_state('NAVIGATE_THROUGH_DOOR')
        else:
            if self._door_was_close == False:
                self.app.log.debug(
                    'The door is closed, waiting for it to open'
                )
                SOUND_OPEN_DOOR_REQUEST['name'] = self.helpers._fsm.step.sound_open_door_name
                await self.helpers.gary_play_audio_predefined(
                    audio=SOUND_OPEN_DOOR_REQUEST,
                )
                try:
                    await self.app.ui.show_animation(
                        **self.helpers._fsm.step.custom_ui_screen,
                        dont_save_last_ui=True
                    )
                except FileNotFoundError as e:
                    self.log.error(f'Error showing animation: {e}')
                self._door_was_close = True

    
    async def NAVIGATE_THROUGH_DOOR(self):
        if await self.app.nav.is_in_zone(
                zone_name=self.helpers._fsm.step.zone_name
            ) != self.helpers.withinInitialZone:
            self.log.debug('Robot left/enter the zone, ending skill...')
            self.set_state('END')
        
        if not self.app.nav.is_navigating():
            nav_error = self.helpers.get_last_result()
            if nav_error[0] == 0:
                self.set_state('END')
            elif await self.helpers.tag_door_visible(
                default_tag=self.helpers._fsm.step.tags_ids[0]
            ):
                self.log.debug('The navigation failed, waiting for the door to open...')
                self.set_state('WAIT_FOR_DOOR_OPEN')
            else:
                self.log.error(f'Navigation error: \'{nav_error}\'')
                self.set_state('NAVIGATE_THROUGH_DOOR_FAILED')


    async def NAVIGATE_THROUGH_DOOR_FAILED(self):
        self.set_state('NAVIGATE_THROUGH_DOOR')


    async def END(self):
        await super().END()
