from raya.tools.fsm import BaseTransitions
from raya.enumerations import SKILL_STATE

from src.app import RayaApplication
from src.static.constants import *
from src.static.leds import *
from src.static.sound import *

from .helpers import Helpers
from .errors import *

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
                self.set_state('GO_TO_HOME_LOCATION')
            else:
                self.abort(*ERR_COULD_NOT_NAV_TO_WAREHOUSE)


    async def GO_TO_HOME_LOCATION(self):
        if not self.app.nav.is_navigating():
            nav_error = self.app.nav.get_last_result()
            if nav_error[0] == 0:
                self.set_state('GO_TO_CART_POINT')
            else:
                self.abort(*ERR_COULD_NOT_NAV_TO_HOME)

    
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
                if self.app.enable_attach:
                    self.set_state('ATTACH_TO_CART')
                else:
                    self.set_state('WAIT_FOR_LOAD_PACKAGE')
            else:
                self.abort(*ERR_COULD_NOT_NAV_TO_CART)


    async def ATTACH_TO_CART(self):
        state = self.app.skill_att2cart.get_execution_state()
        
        if state == SKILL_STATE.EXECUTED:
            result_main = await self.app.skill_att2cart.wait_main()
            self.app.log.debug(f'ATTACH_TO_CART result_main: {result_main}')
        elif state == SKILL_STATE.ERROR_EXECUTING:
            try:
                await self.app.skill_att2cart.wait_main()
            except Exception as e:
                self.app.log.error(
                    f'Error while waiting main for ATTACH_TO_CART: {e}'
                )
            finally:
                self.abort(*ERR_COULD_NOT_ATTACH_TO_CART)
        elif state == SKILL_STATE.ERROR_FINISHING:
            try:
                await self.app.skill_att2cart.wait_finish()
            except Exception as e:
                self.app.log.error(
                    f'Error while waiting finish for ATTACH_TO_CART: {e}'
                )
            finally:
                self.abort(*ERR_COULD_NOT_ATTACH_TO_CART)        
        elif state == SKILL_STATE.FINISHED:
            result_finish = await self.app.skill_att2cart.wait_finish()
            self.app.log.debug(
                f'ATTACH_TO_CART result_finish: {result_finish}'
            )
            self.set_state('GO_TO_WAREHOUSE_EXIT')


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
