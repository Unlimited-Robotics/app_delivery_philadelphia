import typing
if typing.TYPE_CHECKING:
    from src.app import RayaApplication
    
from copy import deepcopy    
from raya.exceptions import *
from src.PartialsFSM.RetryState import Helpers as RetryHelpers

from src.static.app_errors import *
from src.static import *
from src.static.constants import *


class CommonHelpers(RetryHelpers):
    
    def __init__(self, app: 'RayaApplication'):
        super().__init__(app=app)
        
        self.index_package = 0
        self.current_package = self.app.locations[self.index_package]
        
        self.__obstacle_tries = 0
        self.__navigating_tries = 0
        self.last_package = dict()
        self.last_package['name'] = self.app.default_last_package
        
        self.last_ui: callable = None

        self.selected_elevator = None


    async def get_elevator_waiting_point(self):
        current_floor = self.app.get_current_floor_map_name()
        point = FLOORS[current_floor]['waiting_elevator']
        self.app.log.debug(f'Waiting elevator point: {point}')
        return point


    async def check_if_more_packages(self):
        return self.index_package < len(self.app.locations) - 1


    async def set_next_package(self):
        self.last_package = self.app.locations[self.index_package]
        self.index_package += 1
        try:
            self.current_package = self.app.locations[self.index_package]
        except IndexError:
            self.current_package = self.last_package


    def get_current_package(self) -> dict:
        return self.current_package


    def get_last_package(self):
        return self.last_package


    async def get_cart_load_point(self):
        parking_location_name = deepcopy(NAV_PARKING_POSITION_NAME)
        parking_location_name = parking_location_name.replace(
            PARKING_SPOT_SUFFIX, 
            self.app.selected_parking
        )
        cart = await self.app.nav.get_location(
            location_name = parking_location_name,
            map_name = WAREHOUSE_MAP_NAME,
            pos_unit = POSITION_UNIT.PIXELS,
        )
        cart_point = {
            'x': float(cart[0]),
            'y': float(cart[1]),
            'angle': float(cart[2]),
            **NAV_CART_LOAD_POINT_OPTIONS
        }
        return cart_point


    async def get_home_position(self):
        home_location_name = deepcopy(NAV_HOME_POSITION_NAME)
        home_location_name = home_location_name.replace(
            PARKING_SPOT_SUFFIX, 
            self.app.selected_parking
        )
        
        home_location = await self.app.nav.get_location(
            location_name = home_location_name,
            map_name = WAREHOUSE_MAP_NAME,
            pos_unit = POSITION_UNIT.PIXELS,
        )
        home = {
            'x': float(home_location[0]),
            'y': float(home_location[1]),
            'angle': float(home_location[2]),
            **NAV_CART_LOAD_POINT_OPTIONS
        }
        self.log.debug(f'Home position: {home}')
        return home


    async def cb_skill_attach_done(self, exception, result):
        self.app.log.info(f'cb_skill_attach_done, result: {result}')
        if exception is None:
            await self.app.skill_att2cart.execute_finish()
        else: 
            self.app.log.warn(
                    'error occured while attaching, exception type: '
                    f'{type(exception)} {exception}'
                )


    async def cb_skill_attach_feedback(self, feedback):
        self.app.log.info(feedback)
        

    async def cb_skill_detach_done(self, exception, result):
        self.app.log.info(f'cb_skill_detach_done, result: {result}')
        if exception is None:
            await self.app.skill_detach.execute_finish()
        else: 
            self.app.log.warn(
                'error occured while attaching, exception type: '
                f'{type(exception)} {exception}'
            )


    async def cb_skill_dettach_feedback(self, feedback):
        self.app.log.info(feedback)


    def sound_finish_callback(self, code, msg):
        pass
