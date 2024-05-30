from raya.tools.fsm import BaseTransitions
from raya.exceptions import RayaFleetTimeout

from src.app import RayaApplication
from src.static.app_errors import *
from src.static.constants import *
from src.static.fleet import *
from src.static.leds import *
from src.static.sound import *
from .helpers import Helpers
from .errors import *
from .constants import *
from raya.exceptions import RayaFleetTimeout, RayaTaskAlreadyRunning
from raya.enumerations import FLEET_UPDATE_STATUS
from src.static.ui import *
from raya.tools.fsm import RayaFSMAborted

class Transitions(BaseTransitions):

    def __init__(self, app: RayaApplication, helpers: Helpers):
        super().__init__()
        self.app = app
        self.helpers = helpers


    async def SETUP_ACTIONS(self):
        if await self.app.nav.is_localized():
            self.set_state('GO_TO_CART_POINT')
        else:
            self.abort(*ERR_COULD_NOT_LOCALIZE)


    async def GO_TO_CART_POINT(self):
        try:
            await self.helpers.fsm_go_to_cart_point.raise_last_execution_exception()
        except RayaFSMAborted:
            self.app.log.error('FSM Aborted')
            self.helpers.set_last_failed_state('GO_TO_CART_POINT')
            self.set_state('REQUEST_FOR_HELP')
        else:
            if self.helpers.fsm_go_to_cart_point.has_finished() and \
                self.helpers.fsm_go_to_cart_point.was_successful():
                self.set_state('NAV_TO_DELIVERY_POINT')


    async def NAV_TO_DELIVERY_POINT(self):
        if not self.app.nav.is_navigating():
            nav_error = self.app.nav.get_last_result()
            if nav_error[0] == 0:
                self.set_state('NOTIFY_ORDER_ARRIVED')
            else:
                self.helpers.set_last_failed_state('NAV_TO_DELIVERY_POINT')
                self.set_state('REQUEST_FOR_HELP')


    async def NOTIFY_ORDER_ARRIVED(self):
        self.set_state('WAIT_FOR_CHEST_CONFIRMATION')


    async def WAIT_FOR_CHEST_CONFIRMATION(self):
        await self.helpers.gary_play_audio(
            audio=SOUND_WAIT_FOR_CHEST_BUTTON,
            animation_head_leds=LEDS_WAIT_FOR_BUTTON_CHEST_HEAD,
        )
        
        if await self.helpers.check_for_chest_button(): 
            await self.app.sleep(TIME_TO_WAIT_AFTER_BUTTON_PRESS)
            self.set_state('PACKAGE_DELIVERED')


    async def PACKAGE_DELIVERED(self):
        self.set_state('CHECK_IF_MORE_PACKAGES')


    async def PACKAGE_NOT_DELIVERED(self):
        self.set_state('CHECK_IF_MORE_PACKAGES')

    
    async def CHECK_IF_MORE_PACKAGES(self):
        if await self.helpers.check_if_more_packages():
            await self.helpers.set_next_package()
            self.set_state('NAV_TO_DELIVERY_POINT')
        else:
            self.set_state('RETURN_TO_WAREHOUSE_ENTRANCE')


    async def RETURN_TO_WAREHOUSE_ENTRANCE(self):
        if not self.app.nav.is_navigating():
            nav_error = self.app.nav.get_last_result()
            if nav_error[0] == 0:
                self.set_state('PARK_CART')
            else:
                self.helpers.set_last_failed_state('RETURN_TO_WAREHOUSE_ENTRANCE')
                self.set_state('REQUEST_FOR_HELP')


    async def PARK_CART(self):
        try:
            await self.helpers.fsm_go_to_cart_point.raise_last_execution_exception()
        except RayaFSMAborted:
            self.app.log.error('FSM Aborted')
            self.helpers.set_last_failed_state('PARK_CART')
            self.set_state('REQUEST_FOR_HELP')
        else:
            if self.helpers.fsm_park_cart.has_finished() and \
                self.helpers.fsm_park_cart.was_successful():
                self.set_state('NOTIFY_ALL_PACKAGES_STATUS')

    
    async def NOTIFY_ALL_PACKAGES_STATUS(self):
        self.set_state('END')
    

    async def END(self):
        pass

    # REQUEST_FOR_HELP STATES
    
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
            text = f'Fleet responded to the request for help, with {response}'
            await self.app.fleet.update_app_status(
                status=FLEET_UPDATE_STATUS.WARNING,
                message=text
            )
        except RayaFleetTimeout:
            text = ('\'RayaFleetTimeout\' reached, operator did not respond '
                    'to the request for help.')
            await self.app.fleet.update_app_status(
                    status=FLEET_UPDATE_STATUS.WARNING,
                    message=text
                )
        self.set_state('WAIT_FOR_HELP')


    async def WAIT_FOR_HELP(self):
        try:
            self.app.create_task(
                name='task_to_wait_for_help', 
                afunc=self.helpers.task_to_wait_for_help
            )
        except RayaTaskAlreadyRunning:
            self.app.log.warn('task \'task_to_wait_for_help\' already running')
        else:
            response = await self.app.ui.display_choice_selector(
                **UI_SCREEN_WAIT_FOR_HELP_SELECTOR,
                wait=True
            )
            self.app.log.warn(f'User selected: {response}')
            selected_option = response['selected_option']
            if selected_option['name'] == 'Abort App 🚫':
                self.set_state('RELEASE_CART')
            elif selected_option['name'] == 'Continue 🚶‍♂️':
                await self.app.sleep(1)
                self.set_state(self.helpers.get_last_failed_state())

    
    async def RELEASE_CART(self):
        self.app.log.warn('Releasing cart...')
        self.abort(*ERR_NAVIGATION_ABORTED_BY_USER)
