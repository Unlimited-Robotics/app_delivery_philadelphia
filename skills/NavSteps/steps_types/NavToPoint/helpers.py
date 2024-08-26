import typing
if typing.TYPE_CHECKING:
    from src.app import RayaApplication
    from . import NavToPointFSM

import time

from raya.exceptions import RayaTaskAlreadyRunning

from ...PartialsFSM.RetryState import Helpers as RetryHelpers

from .errors import *
from .constants import *


class Helpers(RetryHelpers):

    def __init__(self, app: 'RayaApplication'):
        RetryHelpers.__init__(self=self, app=app)
        self._fsm: NavToPointFSM = None
        
        self.task_interaction_name = 'task_interaction'
        self.__obstacle_detected = False
        
        self.last_code = -1
        self.reset_last_nav()


    def reset_last_nav(self):
        self.listen_feedback = False
        self.moving = False
        self.remaining_distance = -1


    async def nav_feedback_async(self, code, msg, distance, speed):
        if code in [0, 1, 4]:
            self.listen_feedback = True
        if not self.listen_feedback:
            return
        
        await super().nav_feedback_async(
            code=code, 
            msg=msg, 
            distance=distance, 
            speed=speed
        )
        
        self.remaining_distance = distance
        
        if code in NAV_CODES_TRY_PLAN:
            self.moving = True
        
        if code in NAV_CODES_IS_NAVIGATING:
            # self.log.warn('self.__obstacle_detected (1) = False')
            self.__obstacle_detected = False

        if code in NAV_CODES_FINISH_NAV:
            # self.log.warn('self.__obstacle_detected (1.5) = False')
            self.__obstacle_detected = False

        if code in NAV_CODES_OBSTACLE_DETECTED:
            if self.moving:
                # self.log.warn('self.__obstacle_detected (2) = True')
                self.__obstacle_detected = True
                try:
                    self.app.create_task(
                        name=self.task_interaction_name,
                        afunc=self.task_nav_obstacle
                    )
                except RayaTaskAlreadyRunning:
                    pass


    async def nav_finish_async(self, code, msg):
        # self.log.warn('self.__obstacle_detected (3) = False')
        self.__obstacle_detected = False
        self.moving = False
        await super().nav_finish_async(code=code, msg=msg)
        await self.custom_turn_off_leds()


    async def task_nav_obstacle(self):
        
        self.log.warn('task created')
        
        one_clear_way_flag = False
        
        while self.__obstacle_detected:
            
            for _ in range(6): # 3 seconds
                await self.app.sleep(0.5)
                if not self.__obstacle_detected:
                    if not one_clear_way_flag:
                        self.log.warn('aborted')
                        return
                    break
            if not self.__obstacle_detected:
                self.log.warn('skipped')
                break
            
            self.log.warn('please clear the way')
            one_clear_way_flag = True
            await self.app.ui.show_animation(
                **self._fsm.step.custom_ui_screen_obstacle,
                dont_save_last_ui=True
            )
            await self.gary_play_audio_predefined(
                audio=SOUNDS_OBSTACLES_DETECTED[0],
                animation_head_leds=LEDS_NOTIFY_OBSTACLE,
                wait=True,
            )

        if self.moving:
            self.log.warn('thank you')
            await self.app.ui.show_last_animation()
            await self.gary_play_audio_predefined(
                    audio=SOUND_THANK_YOU,
                    animation_head_leds=LEDS_NAVIGATING,
                    wait=True,
                )
            await self.app.sleep(1.0)
