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
            self.log.info('is_approach_done')
            if self.helpers.was_approach_success():
                self.set_state('ATTACH_TO_CART_EXEC')
            else:
                self.attach_fails+=1
                self.set_state('GO_TO_CART_POINT')


    async def ATTACH_TO_CART_EXEC(self):
        state = self.app.skill_att2cart.get_execution_state()
        self.log.info(state)
        if state == SKILL_STATE.EXECUTED:
            self.set_state('ATTACH_TO_CART_FINISH')
        elif state == SKILL_STATE.ERROR_EXECUTING:
            self.attach_fails+=1
            self.set_state('GO_TO_CART_POINT')

    
    async def ATTACH_TO_CART_FINISH(self):
        state = self.app.skill_att2cart.get_execution_state()
        self.log.info(state)
        if state == SKILL_STATE.FINISHED:
            self.set_state('GO_TO_ELEVATOR')
        elif state == SKILL_STATE.ERROR_FINISHING:
            self.attach_fails+=1
            self.set_state('GO_TO_CART_POINT')


    async def GO_TO_ELEVATOR(self):
        result = await self.app.skill_nav_steps.wait_main()
        self.app.log.warn(f'skill_template result: {result}')
        self.set_state('END')

    
    async def END(self):
        self.app.log.info('Task finished successfully')
