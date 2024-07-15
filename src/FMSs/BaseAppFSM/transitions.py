from raya.tools.fsm import BaseTransitions
from raya.exceptions import RayaFleetTimeout
from raya.enumerations import FLEET_UPDATE_STATUS, SKILL_STATE
from raya.tools.fsm import RayaFSMAborted

from src.app import RayaApplication
from src.static import *

from .helpers import Helpers
from src.FMSs.main.errors import *


class CommonTransitions(BaseTransitions):

    def __init__(self, app: RayaApplication, helpers: Helpers):
        super().__init__()
        self.app = app
        self.helpers = helpers
    
    
    async def REQUEST_FOR_HELP(self):
        # TODO: remove
        # self.set_state('WAIT_FOR_HELP')
        try:
            response = await self.app.fleet.request_action(
                title='Request for Help',
                message='I need help, please come to my location.',
                timeout=TIMEOUT_REQUEST_FOR_HELP
            )
            response = response['data']
            await self.app.fleet.update_app_status(
                status=FLEET_UPDATE_STATUS.WARNING,
                message=f'{FLEET_RESPONSE_TO_REQUEST_FOR_HELP} {response}'
            )
        except RayaFleetTimeout:
            await self.app.fleet.update_app_status(
                    status=FLEET_UPDATE_STATUS.WARNING,
                    message=FLEET_TIMEOUT_REQUEST_FOR_HELP
                )
        self.set_state('WAIT_FOR_HELP')


    async def WAIT_FOR_HELP(self):
        response = await self.app.ui.display_choice_selector(
            **UI_SCREEN_WAIT_FOR_HELP_SELECTOR,
            wait=True
        )
        text = (
            'Gary recieved help, and the option selected was: '
            f'{response["selected_option"]}'
        )
        await self.app.fleet.update_app_status(
            status=FLEET_UPDATE_STATUS.WARNING,
            message=text
        )
        self.app.log.warn(f'User selected: {response}')
        selected_option = response['selected_option']
        if selected_option['id'] == 1:
            self.set_state('RELEASE_CART')
        elif selected_option['id'] == 2:
            await self.app.sleep(1)
            self.set_state(self.helpers.get_last_failed_state())

    
    async def RELEASE_CART(self):
        self.app.log.warn('Releasing cart...')
        state = self.app.skill_detach.get_execution_state()
        
        if state == SKILL_STATE.EXECUTED:
            result_main = await self.app.skill_detach.wait_main()
            self.app.log.debug(f'DETACH_TO_CART result_main: {result_main}')
        elif state == SKILL_STATE.ERROR_EXECUTING:
            try:
                await self.app.skill_detach.wait_main()
            except Exception as e:
                self.app.log.error(
                    f'Error while waiting main for DETACH_TO_CART: {e}'
                )
            finally:
                self.abort(*ERR_COULD_NOT_DETACH_CART)
        elif state == SKILL_STATE.ERROR_FINISHING:
            try:
                await self.app.skill_detach.wait_finish()
            except Exception as e:
                self.app.log.error(
                    f'Error while waiting finish for DETACH_TO_CART: {e}'
                )
            finally:
                self.abort(*ERR_COULD_NOT_DETACH_CART)        
        elif state == SKILL_STATE.FINISHED:
            result_finish = await self.app.skill_detach.wait_finish()
            self.app.log.debug(
                f'DETACH_TO_CART result_finish: {result_finish}'
            )
            await self.app.set_gary_footprint(
                footprint=GARY_FOOTPRINT
            )
        self.abort(*ERR_NAVIGATION_ABORTED_BY_USER)


class Transitions(CommonTransitions):
    
    def __init__(self, app: RayaApplication, helpers: Helpers):
        super().__init__()
        self.app = app
        self.helpers = helpers
