from raya.tools.fsm import BaseTransitions
from src.app import RayaApplication
from .helpers import Helpers
from .errors import *
from .constants import *

from src.static.leds import *
from src.static.sound import *

class Transitions(BaseTransitions):

    def __init__(self, app: RayaApplication, helpers: Helpers):
        super().__init__()
        self.app = app
        self.helpers = helpers


    async def CHECK_IF_INSIDE_ZONE(self):
        if await self.helpers.check_if_inside_zone():
            self.set_state('GO_TO_CART_POINT')
        else:
            self.set_state('ENTER_WAREHOUSE')
    
    
    async def ENTER_WAREHOUSE(self):
        if not self.app.nav.is_navigating():
            nav_error = self.app.nav.get_last_result()
            # 18 the nav was canceled
            if nav_error[0] == 18:
                self.set_state('WAIT_FOR_BUTTON_OPEN_ENTRANCE')
            elif nav_error[0] == 0:
                self.set_state('GO_TO_CART_POINT')
            else:
                self.abort(*ERR_COULD_NOT_NAV_TO_WAREHOUSE)

    
    async def WAIT_FOR_BUTTON_OPEN_ENTRANCE(self):
        await self.helpers.gary_play_audio(
            audio=SOUND_WAIT_FOR_CHEST_BUTTON,
        )
        
        if await self.helpers.check_for_chest_button():
            await self.app.sleep(TIME_TO_WAIT_AFTER_BUTTON_PRESS)
            self.set_state('ENTER_WAREHOUSE')


    async def GO_TO_CART_POINT(self):
        if not self.app.nav.is_navigating():
            nav_error = self.app.nav.get_last_result()
            if nav_error[0] == 0:
                self.set_state('WAIT_FOR_UNLOAD_PACKAGE')
            else:
                self.abort(*ERR_COULD_NOT_NAV_TO_CART)

    
    async def WAIT_FOR_UNLOAD_PACKAGE(self):
        await self.helpers.gary_play_audio(
            audio=SOUND_WAIT_FOR_CHEST_BUTTON,
        )
        
        if await self.helpers.check_for_chest_button():
            self.app.log.info('Package loaded')
            await self.app.sleep(TIME_TO_WAIT_AFTER_BUTTON_PRESS)
            self.set_state('END')