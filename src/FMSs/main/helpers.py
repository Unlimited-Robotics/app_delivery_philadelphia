from raya.exceptions import *
from raya.tools.fsm import FSM
from raya.handlers.cv.detectors.tags_detector_handler import \
                                                            TagsDetectorHandler

from src.app import RayaApplication
from src.static.app_errors import *
from src.static import *

from src.FMSs.GoToCartPoint import GoToCartPointFSM
from src.FMSs.ParkCart import ParkCartFSM
from raya.enumerations import FLEET_UPDATE_STATUS
from src.static.constants import *

from time import time
import datetime

class CommonHelpers:
    
    def __init__(self, app: RayaApplication):        
        self.app = app
        self.detectors = dict()
        self._tags = dict()
        self.task_timer_name = 'timer_tag_door'
        self.last_ui: callable = None
        self.__obstacle_tries = 0
        self.__navigating_tries = 0


    async def get_home_position(self):
        self.home_location = await self.app.nav.get_location(
            location_name = NAV_HOME_POSITION_NAME,
            map_name = NAV_WAREHOUSE_MAP_NAME,
            pos_unit = POSITION_UNIT.PIXELS,
        )
        home = {
            'x': self.home_location[0],
            'y': self.home_location[1],
            'angle': self.home_location[2],
            'options': {
                'behavior_tree': 'replan_if_needed_with_footprint',
            }
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
            if self.__navigating_tries >= NAVIGATION_TRY_LIMIT:
                self.app.log.warn(
                        'Navigation tries limit reached, '
                        'resetting obstacle tries to 0'
                    )
                self.__obstacle_tries = 0
                await self.app.sound.cancel_all_sounds()

        elif code == 167:
            # obstacle detected
            self.__obstacle_tries += 1
            self.__navigating_tries = 0
            await self.app.ui.show_animation(**UI_SCREEN_OBSTACLE_DETECTED)

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
            await self.app.leds.turn_off_all()


    async def nav_finish_async(self, code, msg):
        self.app.log.debug(
            f'nav_finish_async: {code}, {msg}'
        )


    async def gary_play_audio(self, 
            audio: dict, 
            animation_head_leds: dict = LEDS_GARY_SPEAKING,
            wait: bool = False
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
                try:
                    await self.app.leds.animation(
                        **animation_head_leds, 
                        wait=False
                    )
                except RayaCommandAlreadyRunning:
                    pass
            
            if wait:
                try:
                    await self.app.leds.animation(
                        **animation_head_leds, 
                        wait=False
                    )
                except RayaCommandAlreadyRunning:
                    pass
                while self.app.sound.is_playing():
                    await self.app.sleep(0.5)
                await self.app.leds.turn_off_group(group='head')
        except RayaCommandAlreadyRunning:
            pass


    def sound_finish_callback(self, code, msg):
        pass


    async def _enable_door_detection(self, 
            wait: bool = False, 
            callback: callable = None
        ):
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
        # timers
        self.app.cancel_task(name=self.task_timer_name)        

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


class Helpers(CommonHelpers):

    def __init__(self, app: RayaApplication):        
        self.app = app
        super().__init__(app)
        
        self.index_package = 0
        self.current_package = self.app.locations[self.index_package]
        self.fsm_go_to_cart_point = GoToCartPointFSM(
            name='GoToCartPointFSM', 
            log_transitions=True
        )
        self.fsm_park_cart = ParkCartFSM(
            name='ParkCartFSM', 
            log_transitions=True
        )
        self._last_failed_state = ''
        self.selected_option_delivery_ui = None


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
        self.current_package = self.app.locations[self.index_package]


    async def task_to_notify(self):
        text = (
            f'This is a reminder that the package {self.index_package + 1} '
            'has arrived at the delivery point and hasn\'t been confirmed.'
        )
        while True:
            await self.app.fleet.update_app_status(
                status=FLEET_UPDATE_STATUS.WARNING,
                message=text
            )
            self.app.log.warn(text)
            await self.app.sleep(TIME_BEETWEEN_NOTIFICATIONS_PACKAGE_ARRIVED)


    async def task_to_wait_for_help(self):
        while True:
            await self.gary_play_audio(
                audio=SOUND_REQUEST_FOR_HELP,
                wait=True
            )
            await self.app.sleep(5)


    def set_last_failed_state(self, state: str):
        self._last_failed_state = state


    def get_last_failed_state(self):
        return self._last_failed_state


    def cb_delivery_arrived_ui_response(self, response):
        self.selected_option_delivery_ui = response['selected_option']

