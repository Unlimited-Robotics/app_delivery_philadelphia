import time

from src.static.constants import *
from src.app import RayaApplication
from src.static.leds import *
from src.static.sound import *
from raya.exceptions import RayaCommandAlreadyRunning
from src.static.constants import NAV_WAREHOUSE_ZONE_NAME

class Helpers:

    def __init__(self, app: RayaApplication):        
        self.app = app


    async def check_if_inside_zone(self):
        return await self.app.nav.is_in_zone(zone_name=NAV_WAREHOUSE_ZONE_NAME)


    def start_timer(self):
        self.start_time = time.time()


    def check_timer(self, time_to_check):
        self.app.log.debug(f'check_timer: {time.time() - self.start_time} >= {time_to_check}')
        return time.time() - self.start_time >= time_to_check


    async def check_for_chest_button(self):
        sensors_data = self.app.sensors.get_all_sensors_values()
        button_chest = sensors_data['chest_button']
        if button_chest!=0:
            await self.app.sound.play_sound(name='success', wait=True)
            return True
        return False


    async def nav_feedback_async(self, code, msg, distance_to_goal, speed):
        self.app.log.debug(
            f'nav_feedback_async: {code}, {msg}, {distance_to_goal}, {speed}'
        )
        if code == 9:
            await self.gary_play_audio(
                audio=SOUND_OBSTACLE_DETECTED,
                animation_head_leds=LEDS_NOTIFY_OBSTACLE
            )


    async def nav_feedback_door_async(self, code, msg, distance, speed):
        self.app.log.debug(
            'nav_feedback_door_async: '
            f'{code}, {msg}, {distance}, {speed}'
        )
        if code == 9:
            if not self.check_timer(TIME_PASSING_THROUGH_DOOR):
                self.app.log.warn('Obstacle detected, the door is closed')
                await self.app.nav.cancel_navigation()
            await self.gary_play_audio(
                audio=SOUND_OBSTACLE_DETECTED,
                animation_head_leds=LEDS_NOTIFY_OBSTACLE
            )

        
    async def nav_finish_async(self, code, msg):
        self.app.log.debug(
            f'nav_finish_async: {code}, {msg}'
        )
        

    async def gary_play_audio(self, 
            audio: dict, 
            animation_head_leds: dict = LEDS_WAIT_FOR_BUTTON_CHEST_HEAD,
            wait=False
        ):
        try:
            if not self.app.sound.is_playing():
                await self.app.leds.turn_off_group(group='head')
                await self.app.sound.play_sound(
                    **audio,
                    wait=False,
                    callback_finish=self.sound_finish_callback
                )
            else:
                await self.app.leds.animation(
                    **animation_head_leds, 
                    wait=False
                )
            
            if wait:
                await self.app.leds.animation(
                    **animation_head_leds, 
                    wait=False
                )
                while self.app.sound.is_playing():
                    await self.app.sleep(0.5)
                await self.app.leds.turn_off_group(group='head')
        except RayaCommandAlreadyRunning:
            pass


    def sound_finish_callback(self, code, msg):
        self.app.log.debug(
            f'sound_finish_callback: {code}, {msg}'
        )

