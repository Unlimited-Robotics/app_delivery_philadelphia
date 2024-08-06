from raya.exceptions import RayaNavLocationNotFound, RayaNavZoneNotFound
from raya.exceptions import RayaCommandAlreadyRunning
from raya.enumerations import FLEET_UPDATE_STATUS
from raya.tools.fsm import RayaFSMAborted

from src.app import RayaApplication
from src.static import *

from .helpers import Helpers
from .errors import *
from src.FMSs.BaseAppFSM.transitions import CommonTransitions


class Transitions(CommonTransitions):

    def __init__(self, app: RayaApplication, helpers: Helpers):
        super().__init__(app=app, helpers=helpers)
        self.app = app
        self.helpers = helpers


    async def SETUP_ACTIONS(self):
        if not await self.helpers.check_if_robot_in_warehouse_floor():
            self.app.log.error('Robot is not in warehouse floor')
            self.abort(*ERR_COULD_NOT_LOCALIZE)
        
        if not await self.app.nav.is_localized():
            self.abort(*ERR_COULD_NOT_LOCALIZE)

        try:
            await self.helpers.get_home_position()
            self.app.log.debug('Home position obtained')
            self.app.log.debug(f'Home position: {self.helpers.home_location}')
        except RayaNavLocationNotFound:
            self.app.log.error((
                'Could not get home position from navigation, '
                'check if the location exist in the navigation map.'
            ))
            self.abort(*ERR_COULD_NOT_GET_HOME_POSITION)
        
        try:
            await self.app.nav.get_zones_list(map_name=WAREHOUSE_MAP_NAME)
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
            self.helpers.set_state_wrapper(
                    new_state='REQUEST_FOR_HELP',
                    last_state='GO_TO_CART_POINT',
                    transitions=self
                )
        else:
            if self.helpers.fsm_go_to_cart_point.has_finished() and \
                self.helpers.fsm_go_to_cart_point.was_successful():
                self.set_state('NAV_TO_FLOOR')


    async def NAV_TO_WAITING_ELEVATOR(self):
        
        if self.app.nav.is_navigating():
            await self.app.custom_animation(
                **LEDS_NAVIGATING_TO_DELIVERY_POINT,
                wait=True
            )
        
        if not self.app.nav.is_navigating():
            nav_error = self.app.nav.get_last_result()
            if nav_error[0] == 0:
                self.set_state('NAV_TO_FLOOR')
            else:
                self.helpers.set_state_wrapper(
                    new_state='REQUEST_FOR_HELP',
                    last_state='NAV_TO_WAITING_ELEVATOR',
                    transitions=self
                )

    
    async def NAV_TO_FLOOR(self):
        try:
            await self.helpers.fsm_go_to_floor.raise_last_execution_exception()
        except RayaFSMAborted:
            self.app.log.error('FSM Aborted')
            self.helpers.set_state_wrapper(
                    new_state='REQUEST_FOR_HELP',
                    last_state='NAV_TO_FLOOR',
                    transitions=self
                )
        else:
            if self.helpers.fsm_go_to_floor.has_finished() and \
                self.helpers.fsm_go_to_floor.was_successful():
                self.set_state('NAV_TO_DELIVERY_POINT')


    async def NAV_TO_DELIVERY_POINT(self):
        if self.app.nav.is_navigating():
            await self.app.custom_animation(
                **LEDS_NAVIGATING_TO_DELIVERY_POINT,
                wait=True
            )
        
        if not self.app.nav.is_navigating():
            nav_error = self.app.nav.get_last_result()
            if nav_error[0] == 0:
                self.set_state('NOTIFY_ORDER_ARRIVED')
            else:
                self.helpers.set_state_wrapper(
                    new_state='REQUEST_FOR_HELP',
                    last_state='NAV_TO_DELIVERY_POINT',
                    transitions=self
                )


    async def NOTIFY_ORDER_ARRIVED(self):
        self.set_state('WAIT_FOR_UI_CONFIRMATION')


    async def WAIT_FOR_UI_CONFIRMATION(self):
        if self.helpers.selected_option_delivery_ui is not None:
            await self.app.custom_animation(**LEDS_WAITING_FOR_DELIVERY_RESPONSE)
            selected_option = self.helpers.selected_option_delivery_ui
            self.app.log.warn(f'User selected: {selected_option}')
            await self.app.custom_cancel_sound()
            await self.app.fleet.update_app_status(
                status=FLEET_UPDATE_STATUS.INFO,
                message=FLEET_PACKAGE_CONFIRM_USING_UI,
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


    async def PACKAGE_DELIVERED(self):
        await self.app.sleep(5)
        self.set_state('CHECK_IF_MORE_PACKAGES')


    async def PACKAGE_NOT_DELIVERED(self):
        await self.app.sleep(5)
        self.set_state('CHECK_IF_MORE_PACKAGES')

    
    async def CHECK_IF_MORE_PACKAGES(self):
        if await self.helpers.check_if_more_packages():
            last_package = self.helpers.current_package['name']
            await self.helpers.set_next_package()
            await self.helpers.change_costmap_to_point(
                initial_point=last_package,
                final_point=self.helpers.current_package['name'],
            )
            if await self.helpers.check_if_robot_in_delivery_floor():
                self.set_state('NAV_TO_DELIVERY_POINT')
            else:
                self.set_state('NAV_TO_WAITING_ELEVATOR')
        else:
            self.set_state('NAV_TO_WAITING_ELEVATOR_TO_WAREHOUSE')


    async def NAV_TO_WAITING_ELEVATOR_TO_WAREHOUSE(self):
        if await self.helpers.check_if_robot_in_warehouse_floor():
            self.set_state('RETURN_TO_WAREHOUSE_ENTRANCE')
        
        if self.app.nav.is_navigating():
            await self.app.custom_animation(
                **LEDS_NAVIGATING_TO_DELIVERY_POINT,
                wait=True
            )
        
        if not self.app.nav.is_navigating():
            nav_error = self.app.nav.get_last_result()
            if nav_error[0] == 0:
                self.set_state('NAV_TO_WAREHOUSE_FLOOR')
            else:
                self.helpers.set_state_wrapper(
                    new_state='REQUEST_FOR_HELP',
                    last_state='NAV_TO_WAITING_ELEVATOR_TO_WAREHOUSE',
                    transitions=self
                )


    async def NAV_TO_WAREHOUSE_FLOOR(self):
        try:
            await self.helpers.fsm_go_to_floor.raise_last_execution_exception()
        except RayaFSMAborted:
            self.app.log.error('FSM Aborted')
            self.helpers.set_state_wrapper(
                    new_state='REQUEST_FOR_HELP',
                    last_state='NAV_TO_WAREHOUSE_FLOOR',
                    transitions=self
                )
        else:
            if self.helpers.fsm_go_to_floor.has_finished() and \
                self.helpers.fsm_go_to_floor.was_successful():
                self.set_state('PARK_CART')


    async def PARK_CART(self):
        try:
            await self.helpers.fsm_park_cart.raise_last_execution_exception()
        except RayaFSMAborted:
            self.app.log.error('FSM Aborted')
            self.helpers.set_state_wrapper(
                    new_state='REQUEST_FOR_HELP',
                    last_state='PARK_CART',
                    transitions=self
                )
        else:
            if self.helpers.fsm_park_cart.has_finished() and \
                self.helpers.fsm_park_cart.was_successful():
                self.set_state('END')


    async def NOTIFY_ALL_PACKAGES_STATUS(self):
        self.set_state('END')
    

    async def END(self):
        pass
