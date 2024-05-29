from raya.exceptions import *
from raya.tools.fsm import FSM

from src.app import RayaApplication
from src.static.app_errors import *
from src.static.navigation import *
from src.static.leds import *
from src.static.sound import *

from src.FMSs.GoToCartPoint import GoToCartPointFSM


class Helpers:

    def __init__(self, app: RayaApplication):        
        self.app = app
        self.index_package = 0
        self.current_package = (
            self.app.locations[self.index_package], 
            self.app.floor[self.index_package]
        )
        self.fsm_go_to_cart_point = GoToCartPointFSM(
            name='GoToCartPoint', 
            log_transitions=True
        )


    async def check_for_chest_button(self):
        sensors_data = self.app.sensors.get_all_sensors_values()
        button_chest = sensors_data['chest_button']
        if button_chest!=0:
            await self.app.sound.play_sound(name='success', wait=True)
            return True
        return False


    async def check_if_robot_in_warehouse_floor(self):
        result = await self.app.nav.get_status()
        is_localized = result['localized']
        map_name = result['map_name']
        if is_localized and map_name == NAV_WAREHOUSE_MAP_NAME:
            return True
        return False


    async def check_if_robot_in_delivery_floor(self):
        result = await self.app.nav.get_status()
        is_localized = result['localized']
        map_name = result['map_name']
        if is_localized and map_name == self.current_package[1]:
            return True
        return False


    async def check_if_more_packages(self):
        return self.index_package < len(self.app.locations) - 1


    async def set_next_package(self):
        self.index_package += 1
        self.current_package = (
            self.app.locations[self.index_package], 
            self.app.floor[self.index_package]
        )


    async def nav_feedback_async(self, code, msg, distance, speed):
        self.app.log.debug(
            'nav_feedback_async: '
            f'{code}, {msg}, {distance}, {speed}'
        )
        if code == 9:
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
            wait: bool = False
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
