import time

from raya.exceptions import RayaCommandAlreadyRunning
from raya.exceptions import RayaListenerAlreadyCreated

from src.app import RayaApplication
from src.static.constants import *
from src.static.leds import *
from src.static.sound import *
from src.static.constants import NAV_WAREHOUSE_ZONE_NAME

class Helpers:

    def __init__(self, app: RayaApplication):        
        self.app = app
        try:
            self.chest_pressed = False
            self.app.sensors.create_threshold_listener(
                listener_name='chest_button_PARK_CART',
                callback_async=self.cb_chest_button,
                sensors_paths=CHEST_LISTENER_PATHS,
                lower_bound=1.0
            )
        except RayaListenerAlreadyCreated:
            pass


    async def check_if_inside_zone(self):
        return await self.app.nav.is_in_zone(zone_name=NAV_WAREHOUSE_ZONE_NAME)


    def start_timer(self):
        self.start_time = time.time()


    def check_timer(self, time_to_check):
        self.app.log.debug(f'check_timer: {time.time() - self.start_time} >= {time_to_check}')
        return time.time() - self.start_time >= time_to_check


    async def check_for_chest_button(self):
        if self.chest_pressed:
            self.chest_pressed = False
            return True
        return False


    async def cb_chest_button(self):
        if self.app.sensors.get_all_sensors_values()["chest_button"] != 0:
            await self.app.sound.play_sound(name='success', wait=True)
            self.chest_pressed = True


    async def nav_feedback_async(self, code, msg, distance_to_goal, speed):
        self.app.log.debug(
            f'nav_feedback_async: {code}, {msg}, {distance_to_goal}, {speed}'
        )
        if code == 9:
            await self.gary_play_audio(
                audio=SOUND_OBSTACLE_DETECTED,
                animation_head_leds=LEDS_NOTIFY_OBSTACLE
            )

        if not self.app.sound.is_playing():
            try:
                await self.app.leds.turn_off_all()
            except RayaCommandAlreadyRunning:
                pass


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
        
        if not self.app.sound.is_playing():
            try:
                await self.app.leds.turn_off_all()
            except RayaCommandAlreadyRunning:
                pass

        
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
                await self.app.sleep(DELAY_BEETWEEN_SOUND_LOOP)
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

    async def cb_skill_detach_done(self, exception, result):
        self.app.log.info(f'cb_skill_detach_done, result: {result}')
        if exception is None:
            await self.app.skill_att2cart.execute_finish()
        else: 
            self.app.log.warn(
                    'error occured while attaching, exception type: '
                    f'{type(exception)} {exception}'
                )


    async def cb_skill_attach_feedback(self, feedback):
        self.app.log.info(feedback)