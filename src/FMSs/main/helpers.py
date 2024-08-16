from raya.exceptions import *

from src.static.app_errors import *
from src.static import *

from src.FMSs.TakeCart import TakeCartFSM
from src.FMSs.LeaveCart import LeaveCartFSM
from src.FMSs.GoToFloor import GoToFloorFSM

from raya.enumerations import FLEET_UPDATE_STATUS

from src.static.constants import *
from src.FMSs.BaseAppFSM.helpers import CommonHelpers


class Helpers(CommonHelpers):

    def __init__(self, app):
        super().__init__(app=app)
        
        self.fsm_take_cart = TakeCartFSM(
            name='TakeCartFSM', 
            log_transitions=True
        )
        self.fsm_leave_cart = LeaveCartFSM(
            name='LeaveCartFSM', 
            log_transitions=True
        )
        self.fsm_go_to_floor = GoToFloorFSM(
            name='GoToFloorFSM', 
            log_transitions=True
        )
        self.selected_option_delivery_ui = None


    async def change_costmap_to_point(self, 
            initial_point: str, 
            final_point: str
        ):
        initial_name = initial_point
        final_name = final_point
        default_costmap_name = COST_MAPS_CONFIG['default_costmap_name']

        try:
            format = COST_MAPS_CONFIG['costmap_format']
            costmap_name = format.replace('[initial_point]', initial_name)
            costmap_name = costmap_name.replace('[final_point]', final_name)
            await self.app.nav.change_costmap(costmap_name=costmap_name)
            self.app.log.debug((
                f'Costmap changed to: {costmap_name}, '
                f'initial_point: {initial_point}, '
                f'final_point: {final_point}'
            ))
        except RayaNavFileNotFound:
            self.app.log.error((
                f'Costmap file \'{costmap_name}\' not found, '
                f'setting default costmap \'{default_costmap_name}\''
            ))
            try:
                await self.app.nav.change_costmap(
                    costmap_name=default_costmap_name
                )
            except RayaCommandTimeout:
                self.app.log.error(f'Costmap change timeout')
        except RayaCommandTimeout:
            self.app.log.error(f'Costmap change timeout')


    async def check_if_robot_in_warehouse_floor(self):
        result = await self.app.nav.get_status()
        is_localized = result['localized']
        map_name = result['map_name']
        map_name_warehouse = WAREHOUSE_MAP_NAME
        if is_localized and map_name == map_name_warehouse:
            self.app.log.warn((
                    f'current_map: {map_name}, '
                    f'map_name_warehouse: {map_name_warehouse}.'
                ))
            self.app.log.warn(
                'The robot is in the warehouse_floor'
            )
            return True
        return False


    async def check_if_robot_in_delivery_floor(self):
        result = await self.app.nav.get_status()
        is_localized = result['localized']
        map_name = result['map_name']
        package_map_name = self.current_package['map_name']
        if is_localized and map_name == package_map_name:    
            self.app.log.warn((
                    f'current_map: {map_name}, '
                    f'package_map_name: {package_map_name}.'
                ))
            self.app.log.warn(
                'The robot is in the same floor as the delivery_point '
            )
            return True
        return False


    async def task_to_notify(self):
        while True:
            await self.app.ui.display_choice_selector(
                    **self.app.delivery_options(),
                    wait=False,
                    callback=self.cb_delivery_arrived_ui_response
                )
            # TODO: add audio saying it arrived
            
            await self.app.sleep(TIME_BEETWEEN_NOTIFICATIONS_PACKAGE_ARRIVED)
            
            self.log.debug('The user didn\'t select any option, calling him....')
            user_id = self.current_package['user_id']
            try:
                await self.app.fleet.request_user_action(
                    request_type='call',
                    request_args=FLEET_CALL_MESSAGE,
                    user_id=user_id,
                    timeout=30.0,
                    wait=False,
                    callback=lambda: None
                )
            except RayaFleetTimeout:
                self.app.log.error('User didn\'t answer the call')


    def cb_delivery_arrived_ui_response(self, response):
        self.selected_option_delivery_ui = response['selected_option']


    async def notify_order_arrived(self):
        await self.app.fleet.update_app_status(
                status=FLEET_UPDATE_STATUS.WARNING,
                message=(
                    f'The package {self.index_package + 1} '
                    'has arrived at the delivery point.'
                )
            )

    