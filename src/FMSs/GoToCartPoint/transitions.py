from raya.enumerations import SKILL_STATE
from raya.exceptions import RayaSkillAborted

from src.app import RayaApplication
from src.static import *

from .helpers import Helpers
from .errors import *
from src.FMSs.BaseAppFSM.transitions import CommonTransitions

class Transitions(CommonTransitions):

    def __init__(self, app: RayaApplication, helpers: Helpers):
        super().__init__(app=app, helpers=helpers)
        self.app = app
        self.helpers = helpers


    async def CHECK_IF_INSIDE_ZONE(self):
        if await self.helpers.check_if_inside_zone():
            self.set_state('GO_TO_HOME_LOCATION')
        # TODO: if not inside zone, go to home using the door


    async def GO_TO_HOME_LOCATION(self):
        if not self.app.nav.is_navigating():
            nav_error = self.app.nav.get_last_result()
            if nav_error[0] == 0:
                try:
                    await self.app.motion.move_linear(
                        **MOTION_HOME_BACKWARD,
                        wait=True,
                    )
                except Exception:
                    pass
                self.set_state('GO_TO_CART_POINT')
            else:
                self.helpers.set_state_wrapper(
                    new_state='REQUEST_FOR_HELP',
                    last_state='GO_TO_HOME_LOCATION',
                    transitions=self
                )


    async def GO_TO_CART_POINT(self):
        if not self.app.nav.is_navigating():
            nav_error = self.app.nav.get_last_result()
            if nav_error[0] == 0:
                if self.app.enable_attach:
                    self.set_state('ATTACH_TO_CART')
            else:
                self.helpers.set_state_wrapper(
                    new_state='REQUEST_FOR_HELP',
                    last_state='GO_TO_CART_POINT',
                    transitions=self
                )


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
                self.helpers.set_state_wrapper(
                    new_state='REQUEST_FOR_HELP',
                    last_state='ATTACH_TO_CART',
                    transitions=self
                )
        elif state == SKILL_STATE.ERROR_FINISHING:
            try:
                await self.app.skill_att2cart.wait_finish()
            except Exception as e:
                self.app.log.error(
                    f'Error while waiting finish for ATTACH_TO_CART: {e}'
                )
            finally:
                self.helpers.set_state_wrapper(
                    new_state='REQUEST_FOR_HELP',
                    last_state='GO_TO_CART_POINT',
                    transitions=self
                )      
        elif state == SKILL_STATE.FINISHED:
            result_finish = await self.app.skill_att2cart.wait_finish()
            self.app.log.debug(
                f'ATTACH_TO_CART result_finish: {result_finish}'
            )
            await self.app.set_gary_footprint(
                footprint=GARY_SELECTED_CART_FOOTPRINT
            )
            self.set_state('GO_TO_ELEVATOR')


    async def GO_TO_ELEVATOR(self):
        try:
            result = await self.app.skill_nav_steps.wait_main()
            self.app.log.warn(f'skill_template result: {result}')

        except RayaSkillAborted as e:
            self.app.log.error((
                'Skill aborted with '
                f'Error code: \'{e.error_code}\', '
                f'Error msg: \'{e.error_msg}\'.'
            ))
            self.helpers.set_state_wrapper(
                new_state='REQUEST_FOR_HELP',
                last_state='GO_TO_ELEVATOR',
                transitions=self
            )
        self.set_state('END')

    
    async def END(self):
        self.app.log.info('Task finished successfully')
