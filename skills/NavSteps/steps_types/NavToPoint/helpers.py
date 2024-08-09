import typing
if typing.TYPE_CHECKING:
    from src.app import RayaApplication
    from . import NavToPointFSM

# from ..CommonType import CommonHelpers
from ...PartialsFSM.RetryState import Helpers as RetryHelpers

from .errors import *
from .constants import *


class Helpers(RetryHelpers):

    def __init__(self, app: 'RayaApplication'):
        RetryHelpers.__init__(self=self, app=app)
        self._fsm: NavToPointFSM = None
        
        self.__navigating_leds_on = False
        
        self.__obstacle_tries = 0
        self.__navigating_tries = 0


    async def nav_feedback_async(self, code, msg, distance, speed):
        self.log.debug(
            'nav_feedback_async: '
            f'{code}, {msg}, {distance}, {speed}'
        )
        
        if code == 6:
            # navigating
            if self.__navigating_tries >= NAVIGATION_TRY_LIMIT and \
                    self.__obstacle_tries != 0:
                self.log.warn(
                        'Navigation tries limit reached, '
                        'resetting obstacle tries to 0'
                    )
                self.__obstacle_tries = 0
                await self.custom_turn_off_leds()
                await self.custom_cancel_sound()
            
            if self.__navigating_leds_on is False:
                # TODO: play last correct ui
                await self.custom_animation(
                    **LEDS_NAVIGATING,
                    wait=False
                )
                self.__navigating_leds_on = True
            
            self.__navigating_tries += 1

        elif code == 7:
            # obstacle detected
            self.__obstacle_tries += 1
            self.__navigating_tries = 0
            
            self.__navigating_leds_on = False
            # await self.app.ui.show_animation(**UI_SCREEN_OBSTACLE_DETECTED)

        elif code == 9:
            if self.__obstacle_tries >= OBSTACLE_DETECTION_THRESHOLDS[1]:
                self.log.error(
                    'Obstacle detected more than' 
                    f' {OBSTACLE_DETECTION_THRESHOLDS[1]} times'
                )
                await self.gary_play_audio(
                    audio=SOUNDS_OBSTACLES_DETECTED[1],
                    animation_head_leds=LEDS_NOTIFY_OBSTACLE,
                )
            elif self.__obstacle_tries >= OBSTACLE_DETECTION_THRESHOLDS[0]:
                self.log.error(
                    'Obstacle detected more than '
                    f'{OBSTACLE_DETECTION_THRESHOLDS[0]} times'
                )
                await self.gary_play_audio(
                    audio=SOUNDS_OBSTACLES_DETECTED[0],
                    animation_head_leds=LEDS_NOTIFY_OBSTACLE
                )
        
            if not self.app.sound.is_playing():
                await self.custom_turn_off_leds()


    async def nav_finish_async(self, code, msg):
        self.log.debug(
            f'nav_finish_async: {code}, {msg}'
        )
        await self.custom_cancel_sound()
        await self.custom_turn_off_leds()
