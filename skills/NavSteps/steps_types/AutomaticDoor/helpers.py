import typing
if typing.TYPE_CHECKING:
    from src.app import RayaApplication
    from . import AutomaticDoorFSM

import datetime

from raya.handlers.cv.detectors.tags_detector_handler import \
                                                            TagsDetectorHandler
from raya.exceptions import RayaTaskNotRunning

from ..CommonType import CommonHelpers

from .errors import *
from .constants import *


class Helpers(CommonHelpers):

    def __init__(self, app: 'RayaApplication'):
        super().__init__(app=app)
        self._fsm: AutomaticDoorFSM
        
        self.detectors = dict()
        self._tags = dict()
        self.task_timer_name = 'timer_tag_door'
        self.detector_is_ready = False
        self.is_inside_initial_zone = False


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

        if len(self.detectors.keys()) > 0:
            self.log.error('Detectors already enabled')
            return
        
        # timers
        self.log.debug('Enabling timers')
        self.app.create_task(
            name=self.task_timer_name,
            afunc=self.timer_reset_tags_values
        )

        # models
        self.log.debug('Enabling models')
        self.detectors = dict()
        for camera in CAMERAS_DETECTING_DOOR:
            detector: TagsDetectorHandler = await self.app.cv.enable_model(
                **self._fsm.step._model,
                source=camera,
            )
            self.detectors[camera] = detector
        
        # detectors listener
        self.log.debug('Enabling detectors listener')
        for detector_index in self.detectors:
            detector: TagsDetectorHandler = self.detectors[detector_index]
            detector.set_img_predictions_callback(
                callback=self._door_state_tag_listener,
                as_dict=True,
                call_without_predictions=True,
                cameras_controller=self.app.cameras
            )


    async def _disable_door_detection(self):
        try:
            # timers
            self.app.cancel_task(name=self.task_timer_name)
        except RayaTaskNotRunning:
            pass

        # models
        # self.log.debug('Disabling models')
        # for detector in self.detectors:
        #     await self.app.cv.disable_model(model_obj=self.detectors[detector])
        await self.__reset_door_tags_values()


    async def __reset_door_tags_values(self):
        self.detector_is_ready = False
        for tag in self._fsm.step._door_tags[f'tag{self._fsm.step.tags_family}']:
            self._tags[tag] = {
                'visible': False,
                'last_time': datetime.datetime.min,
            }


    def _door_state_tag_listener(self, detections, image):
        if self.detector_is_ready is False:
            self.detector_is_ready = True
        
        if detections:
            for tag in detections:
                tag_id = tag['tag_id']
                if tag_id in self._fsm.step._door_tags[f'tag{self._fsm.step.tags_family}']:
                    self._tags[tag_id] = {
                        'visible': True,
                        'last_time': datetime.datetime.now(),
                    }


    async def timer_reset_tags_values(self):
        while True:
            for tag in self._fsm.step._door_tags[f'tag{self._fsm.step.tags_family}']:
                last_time = self._tags[tag]['last_time']
                current_time = datetime.datetime.now()
                if current_time - last_time >= \
                        datetime.timedelta(
                            seconds=DOOR_TAG_TIMEOUT
                        ):
                    self._tags[tag]['visible'] = False
            await self.app.sleep(DOOR_TAG_CALLBACK_TIMER)


    async def tag_door_visible(self, default_tag: int = -1):
        if default_tag != -1:
            return self._tags[default_tag]['visible']
    
        # Check if any of the tags is visible
        if any([self._tags[tag]['visible'] == True for tag in self._fsm.step.tags_ids]):
            return True

        return False


    async def detector_ready(self):
        return self.detector_is_ready

    
    async def nav_feedback_async(self, code, msg, distance, speed):
        self.log.debug(
            'nav_feedback_async: '
            f'{code}, {msg}, {distance}, {speed}'
        )


    async def nav_finish_async(self, code, msg):
        self.log.debug(
            f'nav_finish_async: {code}, {msg}'
        )
