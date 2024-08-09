import typing
if typing.TYPE_CHECKING:
    from src.app import RayaApplication
    from . import ManualDoorFSM

import datetime

from raya.exceptions import RayaFleetTimeout

from ..AutomaticDoor import Helpers as AutomaticDoorHelpers
from .errors import *
from .constants import *


class Helpers(AutomaticDoorHelpers):

    def __init__(self, app: 'RayaApplication'):
        super().__init__(app=app)
        self._fsm: ManualDoorFSM = None
        self.__door_open_timeout = datetime.datetime.now()
        self.task_timer_call_for_help = 'timer_call_for_help'


    async def start_door_close_timeout(self):
        self.__door_open_timeout = datetime.datetime.now()


    async def check_door_close_timeout(self):
        if self.__door_open_timeout - datetime.datetime.now() > \
                datetime.timedelta(seconds=DOOR_CLOSE_TIMEOUT):
            return True
        return False


    async def call_task(self):
        await self.app.sleep(TIME_BEFORE_FIRST_CALL)
        while True:
            request_args = dict()
            request_args['message'] = FLEET_CALL_MESSAGE
            user = self._fsm.step.phone_call_user_id
            self.log.warn(f'Calling the user \'{user}\'...')
            try:
                await self.app.fleet.request_user_action(
                        request_type='call',
                        user_id=user,
                        wait=True,
                        timeout=1.0,
                        request_args=request_args,
                    )
            except RayaFleetTimeout:
                pass

            await self.app.sleep(TIME_BEETWEEN_CALLS)
            self.log.debug((
                'Calling again... '
                f'after {TIME_BEETWEEN_CALLS} seconds.'
            ))


    async def nav_feedback_async(self, code, msg, distance, speed):
        self.log.debug(
            'nav_feedback_async: '
            f'{code}, {msg}, {distance}, {speed}'
        )


    async def nav_finish_async(self, code, msg):
        self.log.debug(
            f'nav_finish_async: {code}, {msg}'
        )
