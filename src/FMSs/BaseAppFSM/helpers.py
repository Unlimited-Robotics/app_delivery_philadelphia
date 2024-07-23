from typing import NoReturn
from raya.exceptions import *
from raya.handlers.cv.detectors.tags_detector_handler import \
                                                            TagsDetectorHandler

from src.app import RayaApplication
from src.static.app_errors import *
from src.static import *
from src.static.constants import *

from time import time
import datetime


class CommonHelpers:
    
    def __init__(self, app: RayaApplication):        
        self.app = app
        self.index_package = 0
        self.current_package = self.app.locations[self.index_package]
        self.detectors = dict()
        self._tags = dict()
        self.task_timer_name = 'timer_tag_door'
        self.last_ui: callable = None
        self.__obstacle_tries = 0
        self.__navigating_tries = 0
        self._last_failed_state = ''
        self._last_failed_state_counter = 1

        self.selected_elevator = None


    def reset_retry_counter(self):
        self._last_failed_state_counter = 1


    def max_retry_reached(self):
        counter = self._last_failed_state_counter > \
            MAX_RETRY_COUNTER_REQUEST_FOR_HELP
        self.app.log.debug((
            f'current try: {self._last_failed_state_counter} '
            f'of {MAX_RETRY_COUNTER_REQUEST_FOR_HELP}'
        ))
        return counter


    def increase_retry_counter(self):
        self._last_failed_state_counter += 1


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

        if code == 30:
            # navigating
            self.__navigating_tries += 1
            if self.__navigating_tries >= NAVIGATION_TRY_LIMIT and \
                    self.__obstacle_tries != 0:
                self.app.log.warn(
                        'Navigation tries limit reached, '
                        'resetting obstacle tries to 0'
                    )
                self.__obstacle_tries = 0
                await self.app.custom_turn_off_leds()
                await self.app.custom_cancel_sound()

        elif code == 167:
            # obstacle detected
            self.__obstacle_tries += 1
            self.__navigating_tries = 0
            # await self.app.ui.show_animation(**UI_SCREEN_OBSTACLE_DETECTED)

        elif code == 9:
            if self.__obstacle_tries >= OBSTACLE_DETECTION_THRESHOLDS[1]:
                self.app.log.error(
                    'Obstacle detected more than' 
                    f' {OBSTACLE_DETECTION_THRESHOLDS[1]} times'
                )
                await self.gary_play_audio(
                    audio=SOUNDS_OBSTACLES_DETECTED[1],
                    animation_head_leds=LEDS_NOTIFY_OBSTACLE,
                )
            elif self.__obstacle_tries >= OBSTACLE_DETECTION_THRESHOLDS[0]:
                self.app.log.error(
                    'Obstacle detected more than '
                    f'{OBSTACLE_DETECTION_THRESHOLDS[0]} times'
                )
                await self.gary_play_audio(
                    audio=SOUNDS_OBSTACLES_DETECTED[0],
                    animation_head_leds=LEDS_NOTIFY_OBSTACLE
                )
        
        if not self.app.sound.is_playing():
            await self.app.custom_turn_off_leds()


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
                await self.app.custom_turn_off_leds(group='head')
                await self.app.sleep(DELAY_BEETWEEN_SOUND_LOOP)
                await self.app.sound.play_sound(
                    **audio,
                    wait=False,
                    callback_finish=self.sound_finish_callback
                )
            else:
                await self.app.custom_animation(
                    **animation_head_leds, 
                    wait=False
                )
            if wait:
                await self.app.custom_animation(
                    **animation_head_leds, 
                    wait=False
                )
                while self.app.sound.is_playing():
                    await self.app.sleep(0.5)
                await self.app.custom_turn_off_leds(group='head')
        except RayaCommandAlreadyRunning:
            pass


    def sound_finish_callback(self, code, msg):
        pass


    async def _enable_door_detection(self):
        await self.__reset_door_tags_values()

        if len(self.detectors.keys()) > 0:
            self.app.log.error('Detectors already enabled')
            return
        
        # timers
        self.app.log.debug('Enabling timers')
        self.app.create_task(
            name=self.task_timer_name,
            afunc=self.timer_reset_tags_values
        )

        # models
        self.app.log.debug('Enabling models')
        self.detectors = dict()
        for camera in CAMERAS_DETECTING_DOOR:
            detector: TagsDetectorHandler = await self.app.cv.enable_model(
                model='detector',type='tag',
                name='apriltags', 
                source=camera,
                model_params = DOOR_MODEL_PARAM
            )
            self.detectors[camera] = detector
        
        # detectors listener
        self.app.log.debug('Enabling detectors listener')
        for detector in self.detectors:
            self.detectors[detector].set_img_detections_callback(
                callback=self._door_state_tag_listener,
                as_dict=True,
                call_without_detections=True,
                cameras_controller=self.app.cameras
            )


    async def _disable_door_detection(self):
        try:
            # timers
            self.app.cancel_task(name=self.task_timer_name)
        except RayaTaskNotRunning:
            pass

        # models
        self.app.log.debug('Disabling models')
        for detector in self.detectors:
            await self.app.cv.disable_model(model_obj=self.detectors[detector])
        await self.__reset_door_tags_values()


    async def __reset_door_tags_values(self):
        for tag in DOOR_TAGS['tag36h11']:
            self._tags[tag] = {
                'visible': False,
                'last_time': datetime.datetime.min,
            }


    def _door_state_tag_listener(self, detections, image):
        if detections:
            for tag in detections:
                tag_id = tag['tag_id']
                if tag_id in DOOR_TAGS['tag36h11']:
                    self._tags[tag_id] = {
                        'visible': True,
                        'last_time': datetime.datetime.now(),
                    }


    async def timer_reset_tags_values(self):
        while True:
            for tag in DOOR_TAGS['tag36h11']:
                last_time = self._tags[tag]['last_time']
                current_time = datetime.datetime.now()
                if current_time - last_time >= \
                        datetime.timedelta(
                            seconds=DOOR_TAG_TIMEOUT
                        ):
                    self._tags[tag]['visible'] = False
            await self.app.sleep(DOOR_TAG_CALLBACK_TIMER)


    async def tag_door_visible(self, tag: int):
        return self._tags[tag]['visible']
    
    
    def __set_last_failed_state(self, state: str):
        if self._last_failed_state != state:
            self.reset_retry_counter()
        self._last_failed_state = state


    def _get_last_failed_state(self):
        return self._last_failed_state


    def set_state_wrapper(self,
            new_state:str,
            transitions, 
            last_state:str = ''
        ) -> NoReturn:
        if last_state != '':
            self.__set_last_failed_state(last_state)
        transitions.set_state(new_state)
        

class Helpers(CommonHelpers):
    def __init__(self, app: RayaApplication):
        self.app = app
        super().__init__(app)
        self.last_ui_result = None

