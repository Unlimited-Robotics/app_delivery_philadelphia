from raya.tools.fsm import BaseTransitions
from raya.exceptions import RayaFleetTimeout, RayaTaskAlreadyRunning
from raya.exceptions import RayaNavLocationNotFound, RayaNavZoneNotFound
from raya.enumerations import FLEET_UPDATE_STATUS
from raya.tools.fsm import RayaFSMAborted

from src.app import RayaApplication
from src.static.app_errors import *
from src.static.constants import *
from src.static.fleet import *
from src.static.leds import *
from src.static.sound import *
from src.static.navigation import *
from src.static.constants import *
from src.static.ui import *
from .helpers import Helpers
from .errors import *


class Transitions(BaseTransitions):

    def __init__(self, app: RayaApplication, helpers: Helpers):
        super().__init__()
        self.app = app
        self.helpers = helpers


    async def SETUP_ACTIONS(self):
        if await self.app.nav.is_localized():
            self.abort(*ERR_COULD_NOT_LOCALIZE)
        
        try:
            await self.helpers.get_home_position()
        except RayaNavLocationNotFound:
            self.app.log.error((
                'Could not get home position from navigation, '
                'check if the location exist in the navigation map.'
            ))
            self.abort(*ERR_COULD_NOT_GET_HOME_POSITION)
        
        try:
            await self.app.nav.get_zones_list(map_name=NAV_WAREHOUSE_MAP_NAME)
        except RayaNavZoneNotFound:
            self.app.log.error((
                'Could not get warehouse entrance position from navigation, '
                'check if the zone exist in the navigation map.'
            ))
            self.abort(*ERR_COULD_NOT_GET_WAREHOUSE_ZONE)
        
        self.set_state('GO_TO_CART_POINT')


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
            audio=SOUND_PACKAGE_DELIVER_ARRIVE,
            animation_head_leds=LEDS_WAIT_FOR_BUTTON_CHEST_HEAD,
        )
        
        if self.helpers.selected_option_delivery_ui is not None:
            selected_option = self.helpers.selected_option_delivery_ui
            self.app.log.warn(f'User selected: {selected_option}')
            await self.app.sound.cancel_all_sounds()
            await self.helpers.gary_play_audio(
                audio=SOUND_STEP_ASIDE,
                wait=True,
            )
            # Only id 1 is considered as a successful delivery
            # UI_SCREEN_OPTIONS_DELIVERY_ARRIVED
            if selected_option['id'] == 1:
                await self.app.fleet.update_app_status(
                    status=FLEET_UPDATE_STATUS.SUCCESS,
                    message=f'Package status:{selected_option["name"]}',
                )
                self.set_state('PACKAGE_DELIVERED')
            else:
                await self.app.fleet.update_app_status(
                    status=FLEET_UPDATE_STATUS.ERROR,
                    message=f'Package status: {selected_option["name"]}',
                )
                self.set_state('PACKAGE_NOT_DELIVERED')
        
        if await self.helpers.check_for_chest_button():
            await self.app.sound.cancel_all_sounds()
            await self.helpers.gary_play_audio(
                audio=SOUND_STEP_ASIDE,
                wait=True,
            )
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
            await self.helpers.fsm_park_cart.raise_last_execution_exception()
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
            if selected_option['id'] == 1:
                self.set_state('RELEASE_CART')
            elif selected_option['id'] == 2:
                await self.app.sleep(1)
                self.set_state(self.helpers.get_last_failed_state())

    
    async def RELEASE_CART(self):
        self.app.log.warn('Releasing cart...')
        self.abort(*ERR_NAVIGATION_ABORTED_BY_USER)
