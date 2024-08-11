import typing
if typing.TYPE_CHECKING:
    from src.app import RayaApplication
    
from raya.exceptions import *
from src.PartialsFSM.RetryState import Helpers as RetryHelpers

from src.static.app_errors import *
from src.static import *
from src.static.constants import *


class CommonHelpers(RetryHelpers):
    
    def __init__(self, app: 'RayaApplication'):
        super().__init__(app=app)
        
        self.index_package = 0
        self.current_package = self.app.locations[self.index_package]
        
        self.__obstacle_tries = 0
        self.__navigating_tries = 0
        
        self.last_ui: callable = None

        self.selected_elevator = None


    async def get_elevator_waiting_point(self):
        current_floor = self.app.get_current_floor_map_name()
        point = FLOORS[current_floor]['waiting_elevator']
        self.app.log.debug(f'Waiting elevator point: {point}')
        return point


    async def check_if_more_packages(self):
        return self.index_package < len(self.app.locations) - 1


    async def set_next_package(self):
        self.index_package += 1
        self.current_package = self.app.locations[self.index_package]


    async def get_current_package_point(self):
        package = self.current_package
        point = {
            'x': float(package['x']),
            'y': float(package['y']),
            'angle': float(package['angle']),
            'pos_unit': POSITION_UNIT.PIXELS, 
            'ang_unit': ANGLE_UNIT.DEGREES,
            **NAVIGATION_OPTIONS_WITH_CART
        }
        self.app.log.debug(f'Package point: {point}')
        return point


    async def get_cart_load_point(self):
        cart = self.app.cart_location
        cart = {
            'x': float(cart['x']),
            'y': float(cart['y']),
            'angle': float(cart['angle']),
            **NAV_CART_LOAD_POINT_OPTIONS
        }
        return cart


    async def get_home_position(self):
        self.home_location = await self.app.nav.get_location(
            location_name = NAV_HOME_POSITION_NAME,
            map_name = WAREHOUSE_MAP_NAME,
            pos_unit = POSITION_UNIT.PIXELS,
        )
        home = {
            'x': self.home_location[0],
            'y': self.home_location[1],
            'angle': self.home_location[2],
            **NAVIGATION_OPTIONS_WITHOUT_CART
        }
        return home

  
    async def nav_feedback_async(self, code, msg, distance, speed):
        self.app.log.debug(
            'nav_feedback_async: '
            f'{code}, {msg}, {distance}, {speed}'
        )

        # if code == 30:
        #     # navigating
        #     self.__navigating_tries += 1
        #     if self.__navigating_tries >= NAVIGATION_TRY_LIMIT and \
        #             self.__obstacle_tries != 0:
        #         self.app.log.warn(
        #                 'Navigation tries limit reached, '
        #                 'resetting obstacle tries to 0'
        #             )
        #         self.__obstacle_tries = 0
        #         await self.custom_turn_off_leds()
        #         await self.custom_cancel_sound()

        # elif code == 167:
        #     # obstacle detected
        #     self.__obstacle_tries += 1
        #     self.__navigating_tries = 0
        #     # await self.app.ui.show_animation(**UI_SCREEN_OBSTACLE_DETECTED)

        # elif code == 9:
        #     if self.__obstacle_tries >= OBSTACLE_DETECTION_THRESHOLDS[1]:
        #         self.app.log.error(
        #             'Obstacle detected more than' 
        #             f' {OBSTACLE_DETECTION_THRESHOLDS[1]} times'
        #         )
        #         await self.gary_play_audio(
        #             audio=SOUNDS_OBSTACLES_DETECTED[1],
        #             animation_head_leds=LEDS_NOTIFY_OBSTACLE,
        #         )
        #     elif self.__obstacle_tries >= OBSTACLE_DETECTION_THRESHOLDS[0]:
        #         self.app.log.error(
        #             'Obstacle detected more than '
        #             f'{OBSTACLE_DETECTION_THRESHOLDS[0]} times'
        #         )
        #         await self.gary_play_audio(
        #             audio=SOUNDS_OBSTACLES_DETECTED[0],
        #             animation_head_leds=LEDS_NOTIFY_OBSTACLE
        #         )
        
        # if not self.app.sound.is_playing():
        #     await self.custom_turn_off_leds()


    async def nav_finish_async(self, code, msg):
        self.app.log.debug(
            f'nav_finish_async: {code}, {msg}'
        )


    async def cb_skill_attach_done(self, exception, result):
        self.app.log.info(f'cb_skill_attach_done, result: {result}')
        if exception is None:
            await self.app.skill_att2cart.execute_finish()
        else: 
            self.app.log.warn(
                    'error occured while attaching, exception type: '
                    f'{type(exception)} {exception}'
                )


    async def cb_skill_attach_feedback(self, feedback):
        self.app.log.info(feedback)
        

    async def cb_skill_detach_done(self, exception, result):
        self.app.log.info(f'cb_skill_detach_done, result: {result}')
        if exception is None:
            await self.app.skill_detach.execute_finish()
        else: 
            self.app.log.warn(
                'error occured while attaching, exception type: '
                f'{type(exception)} {exception}'
            )


    async def cb_skill_dettach_feedback(self, feedback):
        self.app.log.info(feedback)


    async def gary_play_audio(self, 
            audio: dict, 
            animation_head_leds: dict = LEDS_GARY_SPEAKING,
            wait: bool = False
        ):
        try:
            if not self.app.sound.is_playing():
                await self.custom_turn_off_leds(group='head')
                await self.app.sleep(DELAY_BEETWEEN_SOUND_LOOP)
                await self.app.sound.play_sound(
                    **audio,
                    wait=False,
                    callback_finish=self.sound_finish_callback
                )
            else:
                await self.custom_animation(
                    **animation_head_leds, 
                    wait=False
                )
            if wait:
                await self.custom_animation(
                    **animation_head_leds, 
                    wait=False
                )
                while self.app.sound.is_playing():
                    await self.app.sleep(0.5)
                await self.custom_turn_off_leds(group='head')
        except RayaCommandAlreadyRunning:
            pass
        except RayaCommandTimeout:
            pass


    def sound_finish_callback(self, code, msg):
        pass
