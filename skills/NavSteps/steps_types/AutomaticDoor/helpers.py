import typing
if typing.TYPE_CHECKING:
    from src.app import RayaApplication
    from . import AutomaticDoorFSM

import datetime

import numpy as np
import tf_transformations

from raya.handlers.cv.detectors.tags_detector_handler import \
                                                            TagsDetectorHandler
from raya.exceptions import RayaFleetTimeout

from ..CommonType import CommonHelpers

from .errors import *
from .constants import *


class Helpers(CommonHelpers):

    def __init__(self, app: 'RayaApplication'):
        super().__init__(app=app)
        self._fsm: AutomaticDoorFSM
        
        self.__detectors = dict()
        self.__tags = dict()
        self.__readyDetectorFlag = False
        self.withinInitialZone = False
        
        self.__door_open_timeout = datetime.datetime.now()
        self.task_timer_call_for_help = 'timer_call_for_help'


    async def start_door_close_timeout(self):
        self.__door_open_timeout = datetime.datetime.now()


    async def check_door_close_timeout(self):
        if self.__door_open_timeout - datetime.datetime.now() > \
                datetime.timedelta(seconds=self._fsm.step.door_close_timeout):
            return True
        return False


    async def call_task(self):
        await self.app.sleep(self._fsm.step.time_before_first_call)
        self.log.warn('Starting to call the user...')
        while True:
            user = self._fsm.step.phone_call_user_id
            self.log.warn(f'Calling the user \'{user}\'...')
            FLEET_REQUEST_USER_ACTION['request_args']['message'] = \
                self._fsm.step.fleet_call_message
            try:
                await self.app.fleet.request_user_action(
                        user_id=user,
                        wait=True,
                        **FLEET_REQUEST_USER_ACTION,
                    )
            except RayaFleetTimeout:
                pass

            await self.app.sleep(self._fsm.step.time_beetween_calls)
            self.log.debug((
                'Calling again... '
                f'after {self._fsm.step.time_beetween_calls} seconds.'
            ))


    async def enable_cameras(self):
        self.log.debug('Enabling cameras')
        for camera in CAMERAS_DETECTING_DOOR:
            await self.app.cameras.enable_camera(camera_name=camera)
    
    
    async def disable_cameras(self):
        self.log.debug('Disabling cameras')
        for camera in CAMERAS_DETECTING_DOOR:
            await self.app.cameras.disable_camera(camera_name=camera)


    async def _enable_door_detection(self):
        await self.__reset_door_tags_values()

        if len(self.__detectors.keys()) > 0:
            self.log.error('Detectors already enabled')
            return

        # models
        self.log.debug('Enabling models')
        self.__detectors = dict()
        for camera in CAMERAS_DETECTING_DOOR:
            detector: TagsDetectorHandler = await self.app.cv.enable_model(
                **self._fsm.step._model,
                source=camera,
            )
            self.__detectors[camera] = detector
        
        # detectors listener
        self.log.debug('Enabling detectors listener')
        for detector_index in self.__detectors:
            detector: TagsDetectorHandler = self.__detectors[detector_index]
            detector.set_img_predictions_callback(
                callback=self._door_state_tag_listener,
                as_dict=True,
                call_without_predictions=True,
                cameras_controller=self.app.cameras
            )


    async def _disable_door_detection(self):
        # models
        self.log.debug('Disabling models')
        for detector in self.__detectors:
            await self.app.cv.disable_model(model_obj=self.__detectors[detector])
        await self.__reset_door_tags_values()


    async def __reset_door_tags_values(self):
        self.__readyDetectorFlag = False
        for tag in self._fsm.step._door_tags[f'tag{self._fsm.step.tags_family}']:
            self.__tags[tag] = {
                'visible': False,
                'last_time': datetime.datetime.min,
            }

    def get_tag_info_rotation(self, tag):
        orientation = tag["pose_base_link"].pose.orientation
        quat = [0,0,0,0]
        quat[0] = orientation.x
        quat[1] = orientation.y
        quat[2] = orientation.z
        quat[3] = orientation.w
        orientation = tf_transformations.euler_from_quaternion(quat)
        orientation = np.rad2deg(orientation)
        yaw_offset = 180.0
        orientation[2] += yaw_offset

        # Normalize the yaw value to be within the range -180 to 180 degrees
        if orientation[2] > 180:
            orientation[2] -= 360
        elif orientation[2] < -180:
            orientation[2] += 360
        return orientation


    def _door_state_tag_listener(self, detections, image):
        if self.__readyDetectorFlag is False:
            self.__readyDetectorFlag = True
        
        if detections:
            for tag in detections:
                tag_id = tag['tag_id']
                orientation = self.get_tag_info_rotation(tag=tag)
                            
                if tag_id in self._fsm.step._door_tags[f'tag{self._fsm.step.tags_family}']:
                    if abs(orientation[2]) < self._fsm.step.range_degrees_tag_visible:
                        # self.log.debug((
                        #     f'Tag {tag_id} detected within range '
                        #     f'yaw:{orientation[2]:.2f}'
                        # ))
                        self.__tags[tag_id] = {
                            'visible': True,
                            'last_time': datetime.datetime.now(),
                        }


    async def tag_door_visible(self, default_tag: int = -1):
        if default_tag != -1:
            last = self.__tags[default_tag]['last_time']
            now = datetime.datetime.now()
            delta = now - last 
            # self.log.debug(f'delta {delta}')
            return delta < datetime.timedelta(
                seconds=self._fsm.step.door_tag_timeout
            )
    
        # Check if any of the tags is visible
        # if any([self._tags[tag]['last_time'] == True for tag in self._fsm.step.tags_ids]):
        #     return True

        return False


    async def detector_ready(self):
        return self.__readyDetectorFlag

    
    async def nav_feedback_async(self, code, msg, distance, speed):
        await super().nav_feedback_async(
            code=code, 
            msg=msg, 
            distance=distance, 
            speed=speed
        )


    async def nav_finish_async(self, code, msg):
        await super().nav_finish_async(code=code, msg=msg)
