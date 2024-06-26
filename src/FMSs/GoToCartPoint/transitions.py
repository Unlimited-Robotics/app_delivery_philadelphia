from raya.tools.fsm import BaseTransitions
from src.app import RayaApplication
from .helpers import Helpers
from .errors import *
from src.static.constants import *

from src.static.leds import *
from src.static.sound import *

class Transitions(BaseTransitions):

    def __init__(self, app: RayaApplication, helpers: Helpers):
        super().__init__()
        self.app = app
        self.helpers = helpers


    async def CHECK_IF_INSIDE_ZONE(self):
        # TODO: remove
        # self.abort(*ERR_COULD_NOT_LOCALIZE)
        if await self.helpers.check_if_inside_zone():
            self.set_state('GO_TO_CART_POINT')
        else:
            self.set_state('GO_TO_WAREHOUSE_ENTRANCE')

    
    async def GO_TO_WAREHOUSE_ENTRANCE(self):
        if not self.app.nav.is_navigating():
            nav_error = self.app.nav.get_last_result()
            if nav_error[0] == 0:
                self.set_state('ENTER_WAREHOUSE')
            else:
                self.abort(*ERR_COULD_NOT_NAV_TO_WAREHOUSE)

    
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
            await self.app.sound.cancel_all_sounds()
            await self.helpers.gary_play_audio(
                audio=SOUND_STEP_ASIDE,
                wait=True,
            )
            await self.app.sleep(TIME_TO_WAIT_AFTER_BUTTON_PRESS)
            self.set_state('ENTER_WAREHOUSE')


    async def GO_TO_CART_POINT(self):
        if not self.app.nav.is_navigating():
            nav_error = self.app.nav.get_last_result()
            if nav_error[0] == 0:
                self.set_state('WAIT_FOR_LOAD_PACKAGE')
            else:
                self.abort(*ERR_COULD_NOT_NAV_TO_CART)

    
    async def WAIT_FOR_LOAD_PACKAGE(self):
        await self.helpers.gary_play_audio(
            audio=SOUND_WAIT_FOR_CHEST_BUTTON,
        )
        
        if await self.helpers.check_for_chest_button():
            self.app.log.info('Package loaded')
            await self.app.sound.cancel_all_sounds()
            await self.helpers.gary_play_audio(
                audio=SOUND_STEP_ASIDE,
                wait=True,
            )
            await self.app.sleep(TIME_TO_WAIT_AFTER_BUTTON_PRESS)
            self.set_state('GO_TO_WAREHOUSE_EXIT')

    
    async def GO_TO_WAREHOUSE_EXIT(self):
        if not self.app.nav.is_navigating():
            nav_error = self.app.nav.get_last_result()
            if nav_error[0] == 0:
                self.set_state('LEAVE_WAREHOUSE')
            else:
                self.abort(*ERR_COULD_NOT_NAV_TO_WAREHOUSE_EXIT)

    
    async def LEAVE_WAREHOUSE(self):
        if self.app.nav.is_navigating() and \
            await self.helpers.check_if_inside_zone() == True:
                self.set_state('END')
        
        if not self.app.nav.is_navigating():
            nav_error = self.app.nav.get_last_result()
            # 18 the nav was canceled
            if nav_error[0] == 18:
                self.set_state('WAIT_FOR_BUTTON_EXITING')
            elif nav_error[0] == 0:
                self.set_state('END')
            else:
                self.abort(*ERR_COULD_NOT_NAV_TO_WAREHOUSE)


    async def WAIT_FOR_BUTTON_EXITING(self):
        await self.helpers.gary_play_audio(
            audio=SOUND_WAIT_FOR_CHEST_BUTTON,
        )
        
        if await self.helpers.check_for_chest_button():
            await self.app.sound.cancel_all_sounds()
            await self.helpers.gary_play_audio(
                audio=SOUND_STEP_ASIDE,
                wait=True,
            )
            await self.app.sleep(TIME_TO_WAIT_AFTER_BUTTON_PRESS)
            self.set_state('LEAVE_WAREHOUSE')
