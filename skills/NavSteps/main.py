from typing import Union, List

from raya.skills import RayaFSMSkill
from raya.tools.fsm import RayaFSMAborted, FSM

from raya.controllers.navigation_controller import NavigationController

from .steps_types import *
from .constants import *
from .errors import *


class SkillNavSteps(RayaFSMSkill):

    DEFAULT_SETUP_ARGS = {

    }
    
    REQUIRED_SETUP_ARGS = {
        
    }
    
    DEFAULT_EXECUTE_ARGS = {
        
    }
    
    REQUIRED_EXECUTE_ARGS = {
        'steps',
    }
    
###############################################################################
###########################    FSM states     #################################
###############################################################################

    STATES = [
        'SETUP_STEPS',
        'EXECUTE_STEPS',
        'CLEANUP_STEPS',
        'END',
    ]

    INITIAL_STATE = 'SETUP_STEPS'

    END_STATES = [
        'END'
    ]
    
    STATES_TIMEOUTS = {}


###############################################################################
###########################   SKILL METHODS   #################################
###############################################################################


    async def setup(self):
        self.nav:NavigationController = \
            await self.enable_controller('navigation')
        self._steps: List[Union[NavToPoint, ManualDoor,AutomaticDoor]] = []

    
    async def finish(self):
        await self.send_feedback('RayaSkill.finish')


###############################################################################
##########################      HELPERS      ##################################
###############################################################################

###############################################################################
#########################      ACTIONS       ##################################
###############################################################################
    
    
    async def enter_SETUP_STEPS(self):
        for step in self.execute_args['steps']:
            step_name = step.get('name')
            step_type = step.pop('type')
            
            self.log.warn((
                f'Initializing step... Name:\'{step_name}\', '
                f'Type \'{step_type}\''
            ))
            if step_type == NAV_TO_POINT_TYPE_NAME:
                nav_to_point_step = NavToPoint(**step)
                self._steps.append(nav_to_point_step)
            elif step_type == MANUAL_DOOR_TYPE_NAME:
                manual_door = ManualDoor(**step)
                self._steps.append(manual_door)
            elif step_type == AUTOMATIC_DOOR_TYPE_NAME:
                automatic_door = AutomaticDoor(**step)
                self._steps.append(automatic_door)
            elif step_type == TEST_TYPE_NAME:
                test = CommonType(
                    name=step.get('name')
                )
                self._steps.append(test)
            else:
                self.log.error((
                    f'step... Name:\'{step_name}\', '
                    f'Type \'{step_type}\' not valid'
                ))
                self.abort(*ERROR_STEP_NOT_VALID)

            self.log.debug(f'Step \'{step_name}\' initialized successfully')
        self.log.debug('All steps initialized successfully')


    async def enter_EXECUTE_STEPS(self):
        pass


###############################################################################
#########################    TRASITIONS      ##################################
###############################################################################

    async def transition_from_SETUP_STEPS(self):
        self.set_state('EXECUTE_STEPS')
        

    async def transition_from_EXECUTE_STEPS(self):
        for step in self._steps:
            self.log.warn(f'Running step \'{step.name}\'')
            try:
                await step.fsm.run_and_await()
            except RayaFSMAborted as error:
                self.log.error((
                    f'Step \'{step.name}\' Aborted with '
                    f'Error code: \'{error.error_code}\' '
                    f'Error msg: \'{error.error_msg}\''
                ))
                self.abort(error.error_code, error.error_msg)
        self.set_state('CLEANUP_STEPS')


    async def transition_from_CLEANUP_STEPS(self):
        self.log.debug('Cleaning up...')
        for step in self._steps:
            FSM.registered_fsms.remove(step.name)
            del step
        
        self._steps=[]
        self.set_state('END')
