from raya.exceptions import RayaNavLocationNotFound, RayaNavZoneNotFound
from raya.enumerations import FLEET_UPDATE_STATUS
from raya.tools.fsm import RayaFSMAborted


from src.FMSs.BaseAppFSM.transitions import CommonTransitions
from src.static import *

from .helpers import Helpers
from .errors import *


class Transitions(CommonTransitions):

    def __init__(self, app, helpers: Helpers):
        super().__init__(app=app, helpers=helpers)
        self.helpers: Helpers 


    async def SETUP_ACTIONS(self):
        if not await self.helpers.check_if_robot_in_warehouse_floor():
            self.app.log.error('Robot is not in warehouse floor')
            self.abort(*ERR_COULD_NOT_LOCALIZE)
        
        if not await self.app.nav.is_localized():
            self.abort(*ERR_COULD_NOT_LOCALIZE)

        try:
            home_location = await self.helpers.get_home_position()
            self.app.log.debug('Home position obtained')
            self.app.log.debug(f'Home position: {home_location}')
        except RayaNavLocationNotFound:
            self.app.log.error((
                'Could not get home position from navigation, '
                'check if the location exist in the navigation map.'
            ))
            self.abort(*ERR_COULD_NOT_GET_HOME_LOCATION)
        
        try:
            cart_location = await self.helpers.get_cart_load_point()
            self.app.log.debug('Parking position obtained')
            self.app.log.debug(f'Parking position: {cart_location}')
        except RayaNavLocationNotFound:
            self.app.log.error((
                'Could not get Parking position from navigation, '
                'check if the location exist in the navigation map.'
            ))
            self.abort(*ERR_COULD_NOT_GET_PARKING_LOCATION)
        
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
        if self.helpers.fsm_take_cart.has_finished() and \
            self.helpers.fsm_take_cart.was_successful():
            self.set_state('NAV_TO_FLOOR')


    async def NAV_TO_WAITING_ELEVATOR(self):
        result = await self.app.skill_nav_steps.wait_main()
        self.app.log.warn(f'skill_template result: {result}')
        self.set_state('NAV_TO_FLOOR')

    
    async def NAV_TO_FLOOR(self):
        if self.helpers.fsm_go_to_floor.has_finished() and \
            self.helpers.fsm_go_to_floor.was_successful():
            self.set_state('NAV_TO_DELIVERY_POINT')


    async def NAV_TO_DELIVERY_POINT(self):
        result = await self.app.skill_nav_steps.wait_main()
        self.app.log.warn(f'skill_template result: {result}')
        self.set_state('NOTIFY_ORDER_ARRIVED')


    async def NOTIFY_ORDER_ARRIVED(self):
        self.set_state('WAIT_FOR_UI_CONFIRMATION')


    async def WAIT_FOR_UI_CONFIRMATION(self):
        if self.helpers.selected_option_delivery_ui is not None:
            await self.helpers.custom_animation(**LEDS_WAITING_FOR_DELIVERY_RESPONSE)
            selected_option = self.helpers.selected_option_delivery_ui
            self.app.log.warn(f'User selected: {selected_option}')
            await self.helpers.custom_cancel_sound()
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
            await self.helpers.set_next_package()
            
            last_package = self.helpers.get_last_package()
            current_package = self.helpers.get_current_package()
            
            last_unit = self.app.get_unit_name(
                package_point_name=last_package['name']
            )
            
            if await self.helpers.check_if_robot_in_delivery_floor():
                current_unit = self.app.get_unit_name(
                    package_point_name=current_package['name']
                )
                await self.helpers.change_costmap_to_point(
                    initial_point=last_unit,
                    final_point=current_unit,
                )
                self.set_state('NAV_TO_DELIVERY_POINT')
            else:
                await self.helpers.change_costmap_to_point(
                    initial_point=last_unit,
                    final_point='elev',
                )
                self.set_state('NAV_TO_WAITING_ELEVATOR')
        else:
            await self.helpers.set_next_package()
            self.set_state('NAV_TO_WAITING_ELEVATOR_TO_WAREHOUSE')


    async def NAV_TO_WAITING_ELEVATOR_TO_WAREHOUSE(self):
        if await self.helpers.check_if_robot_in_warehouse_floor():
            self.set_state('PARK_CART')
        
        result = await self.app.skill_nav_steps.wait_main()
        self.app.log.warn(f'skill_template result: {result}')
        self.set_state('NAV_TO_WAREHOUSE_FLOOR')


    async def NAV_TO_WAREHOUSE_FLOOR(self):
        if self.helpers.fsm_go_to_floor.has_finished() and \
            self.helpers.fsm_go_to_floor.was_successful():
            self.set_state('PARK_CART')


    async def PARK_CART(self):
        if self.helpers.fsm_leave_cart.has_finished() and \
            self.helpers.fsm_leave_cart.was_successful():
            self.set_state('END')
    

    async def END(self):
        pass
