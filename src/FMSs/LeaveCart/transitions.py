from raya.enumerations import SKILL_STATE, FLEET_UPDATE_STATUS

from src.app import RayaApplication
from src.static import *

from .helpers import Helpers
from .errors import *
from src.FMSs.BaseAppFSM.transitions import CommonTransitions


class Transitions(CommonTransitions):

    def __init__(self, app: RayaApplication, helpers: Helpers):
        super().__init__(app=app, helpers=helpers)
        self.helpers: Helpers


    async def GO_TO_DETACH_CART_POINT(self):
        result = await self.app.skill_nav_steps.wait_main()
        self.app.log.warn(f'skill_template result: {result}')
        self.set_state('DETACH_CART')


    async def DETACH_CART(self):
        state = self.app.skill_detach.get_execution_state()
        
        if state == SKILL_STATE.EXECUTED:
            result_main = await self.app.skill_detach.wait_main()
            self.app.log.debug(f'DETACH_TO_CART result_main: {result_main}')
        elif state == SKILL_STATE.ERROR_EXECUTING:
            try:
                await self.app.skill_detach.wait_main()
            except Exception as e:
                self.app.log.error(
                    f'Error while waiting main for DETACH_TO_CART: {e}'
                )
            finally:
                self.helpers.retry_step(
                    transitions=self,
                    last_state='DETACH_CART',
                )
        elif state == SKILL_STATE.ERROR_FINISHING:
            try:
                await self.app.skill_detach.wait_finish()
            except Exception as e:
                self.app.log.error(
                    f'Error while waiting finish for DETACH_TO_CART: {e}'
                )
            finally:
                self.helpers.retry_step(
                    transitions=self,
                    last_state='DETACH_CART',
                )    
        elif state == SKILL_STATE.FINISHED:
            result_finish = await self.app.skill_detach.wait_finish()
            self.app.log.debug(
                f'DETACH_TO_CART result_finish: {result_finish}'
            )
            await self.app.fleet.update_app_status(
                    status=FLEET_UPDATE_STATUS.INFO,
                    message=FLEET_CART_RELEASED
                )
            self.app.log.warn('Cart released...')
            self.set_state('GO_TO_HOME_LOCATION')


    async def GO_TO_HOME_LOCATION(self):
        result = await self.app.skill_nav_steps.wait_main()
        self.app.log.warn(f'skill_template result: {result}')
        try:
            await self.app.motion.move_linear(
                **MOTION_HOME_BACKWARD,
                wait=True,
            )
        except Exception:
            pass
        self.set_state('END')


    async def END(self):
        pass
