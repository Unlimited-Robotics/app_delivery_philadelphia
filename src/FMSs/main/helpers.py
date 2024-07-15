from raya.exceptions import *

from src.app import RayaApplication
from src.static.app_errors import *
from src.static import *

from src.FMSs.GoToCartPoint import GoToCartPointFSM
from src.FMSs.ParkCart import ParkCartFSM
from raya.enumerations import FLEET_UPDATE_STATUS
from src.static.constants import *
from src.FMSs.BaseAppFSM.helpers import CommonHelpers


class Helpers(CommonHelpers):

    def __init__(self, app: RayaApplication):        
        self.app = app
        super().__init__(app)
        
        self.index_package = 0
        self.current_package = self.app.locations[self.index_package]
        self.fsm_go_to_cart_point = GoToCartPointFSM(
            name='GoToCartPointFSM', 
            log_transitions=True
        )
        self.fsm_park_cart = ParkCartFSM(
            name='ParkCartFSM', 
            log_transitions=True
        )
        self.selected_option_delivery_ui = None


    async def check_if_robot_in_warehouse_floor(self):
        result = await self.app.nav.get_status()
        is_localized = result['localized']
        map_name = result['map_name']
        if is_localized and map_name == NAV_WAREHOUSE_MAP_NAME:
            return True
        return False


    async def check_if_robot_in_delivery_floor(self):
        result = await self.app.nav.get_status()
        is_localized = result['localized']
        map_name = result['map_name']
        if is_localized and map_name == self.current_package[1]:
            return True
        return False


    async def check_if_more_packages(self):
        return self.index_package < len(self.app.locations) - 1


    async def set_next_package(self):
        self.index_package += 1
        self.current_package = self.app.locations[self.index_package]


    async def task_to_notify(self):
        text = (
            f'This is a reminder that the package {self.index_package + 1} '
            'has arrived at the delivery point and hasn\'t been confirmed.'
        )
        while True:
            await self.app.fleet.update_app_status(
                status=FLEET_UPDATE_STATUS.WARNING,
                message=text
            )
            self.app.log.warn(text)
            await self.app.sleep(TIME_BEETWEEN_NOTIFICATIONS_PACKAGE_ARRIVED)


    def cb_delivery_arrived_ui_response(self, response):
        self.selected_option_delivery_ui = response['selected_option']

