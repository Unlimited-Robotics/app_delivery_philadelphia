import typing
if typing.TYPE_CHECKING:
    from src.app import RayaApplication

from ..CommonFSM import CommonTransitions

from .helpers import Helpers
from .constants import *


class Transitions(CommonTransitions):

    def __init__(self, app: 'RayaApplication', helpers: Helpers):
        super().__init__(app=app, helpers=helpers)
        self.helpers: Helpers
    
    
    async def REQUEST_FOR_HELP(self):
        if not self.helpers.max_retry_reached():
            self.set_state('CONTINUE')
        else:
            self.set_state('WAIT_FOR_HELP')


    async def WAIT_FOR_HELP(self):
        if self.helpers.check_teleoperator_timeout():
            # TODO: Add a new state to handle the timeout
            self.log.warn('Timeout reached for teleoperator')
            self.abort(*ERR_TELEOPERATOR_TIMEOUT)
        
        if self.helpers._ui_response_wait_for_help is None:
            return
        
        response = self.helpers._ui_response_wait_for_help
        self.log.warn(f'User selected: {response}')
        if 'selected_option' not in response:
            return

        selected_option = response['selected_option']
        options = UI_SCREEN_WAIT_FOR_HELP_SELECTOR['data']
        if selected_option['name'] == options[0]['name']:
            self.set_state('ABORT')
        elif selected_option['name'] == options[1]['name']:
            await self.app.sleep(TIME_TO_WAIT_AFTER_CONTINUE)
            self.set_state('CONTINUE')


    async def CONTINUE(self):
        await self.app.sleep(1)
        self.set_state(self.helpers._get_last_failed_state())

    
    async def ABORT(self):
        self.abort(*ERR_APP_ABORTED)

