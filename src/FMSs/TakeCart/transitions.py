from raya.enumerations import SKILL_STATE

from src.static import *

from .helpers import Helpers
from .errors import *
from src.FMSs.BaseAppFSM.transitions import CommonTransitions

class Transitions(CommonTransitions):

    def __init__(self, app, helpers: Helpers):
        super().__init__(app=app, helpers=helpers)
        self.helpers: Helpers
        self.attach_fails = 0


    async def GO_TO_CART_POINT(self):
        result = await self.app.skill_nav_steps.wait_main()
        self.app.log.warn(f'skill_template result: {result}')
        self.set_state('APPROACH_TO_CART')

    
    async def APPROACH_TO_CART(self):
        if self.helpers.is_approach_done():
            if self.helpers.was_approach_success():
                self.set_state('ATTACH_TO_CART')
            else:
                self.attach_fails+=1
                self.set_state('GO_TO_CART_POINT')


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
                self.helpers.retry_step(
                    transitions=self,
                    last_state='ATTACH_TO_CART',
                )
        elif state == SKILL_STATE.ERROR_FINISHING:
            try:
                await self.app.skill_att2cart.wait_finish()
            except Exception as e:
                self.app.log.error(
                    f'Error while waiting finish for ATTACH_TO_CART: {e}'
                )
            finally:
                self.helpers.retry_step(
                    transitions=self,
                    last_state='ATTACH_TO_CART',
                )      
        elif state == SKILL_STATE.FINISHED:
            result_finish = await self.app.skill_att2cart.wait_finish()
            self.app.log.debug(
                f'ATTACH_TO_CART result_finish: {result_finish}'
            )
            await self.app.set_gary_footprint(
                footprint=GARY_SELECTED_CART_FOOTPRINT
            )
            self.set_state('END')


    async def GO_TO_ELEVATOR(self):
        result = await self.app.skill_nav_steps.wait_main()
        self.app.log.warn(f'skill_template result: {result}')
        self.set_state('END')

    
    async def END(self):
        self.app.log.info('Task finished successfully')
