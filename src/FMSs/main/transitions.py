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
        if self.helpers.fsm_go_to_cart_point.has_finished():
            if self.helpers.fsm_go_to_cart_point.was_successful():
                self.set_state('NAV_TO_DELIVERY_POINT')
            else:
                self.abort(*self.helpers.fsm_go_to_cart_point.get_error())


    async def NAV_TO_DELIVERY_POINT(self):
        if not self.app.nav.is_navigating():
            nav_error = self.app.nav.get_last_result()
            if nav_error[0] == 0:
                self.set_state('NOTIFY_ORDER_ARRIVED')
            else:
                self.abort(*ERR_COULD_NOT_NAV_TO_DELIVERY_POINT)


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
                self.abort(*ERR_COULD_NOT_NAV_TO_DELIVERY_POINT)


    async def PARK_CART(self):
        if self.helpers.fsm_park_cart.has_finished():
            if self.helpers.fsm_park_cart.was_successful():
                self.set_state('NOTIFY_ALL_PACKAGES_STATUS')
            else:
                self.abort(*self.helpers.fsm_park_cart.get_error())

    
    async def NOTIFY_ALL_PACKAGES_STATUS(self):
        self.set_state('END')
    

    async def END(self):
        pass
