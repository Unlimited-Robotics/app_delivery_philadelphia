from copy import deepcopy
from src.FMSs.BaseAppFSM.actions import CommonAction
from raya.enumerations import FLEET_UPDATE_STATUS, POSITION_UNIT, ANGLE_UNIT

from src.static import *
from .helpers import Helpers

class Actions(CommonAction):

    def __init__(self, app, helpers: Helpers):
        super().__init__(app=app, helpers=helpers)
        self.helpers: Helpers


    async def enter_GO_TO_CART_POINT(self):
        await self.app.set_gary_footprint(
            footprint=GARY_FOOTPRINT
        )
        cart_location = await self.helpers.get_cart_load_point()
        self.app.log.debug(f'navigate_to_position {cart_location}')
        
        cart_steps = deepcopy(BASEMENT_ROUTES['go_to_parking_cart_point'])
        cart_steps[0]['point'] = cart_location
        execute_args = {
            'steps': cart_steps
        }
        await self.app.skill_nav_steps.execute_main(
            execute_args=execute_args,
            callback_done=self.helpers.cb_skill_done,
            callback_feedback=self.helpers.cb_skill_feedback,
            wait=False
        )


    async def enter_APPROACH_TO_CART(self):
        await self.app.fleet.update_app_status(
            status=FLEET_UPDATE_STATUS.INFO,
            message=FLEET_ROBOT_ATTACHING_TO_CART
        )
        self.helpers.approach_error_code = None
        await self.app.robot_skills.execute_skill(
            **EXECUTION_ARG_APPROACH_SKILL,
            callback_finish=self.helpers.cb_finish_approach_skill,
            callback_feedback=self.helpers.cb_feedback_approach_skill,
            wait=False,
        )


    async def enter_ATTACH_TO_CART_EXEC(self):
        print('enter_ATTACH_TO_CART_EXEC')
        await self.app.skill_att2cart.execute_main(
            execute_args=EXECUTION_ARG_ATTACH_SKILL,
            callback_done=self.helpers.cb_skill_attach_done,
            callback_feedback=self.helpers.cb_skill_attach_feedback,
            wait=False
        )

    
    async def enter_ATTACH_TO_CART_FINISH(self):
        print('enter_ATTACH_TO_CART_FINISH')
        await self.app.skill_att2cart.execute_finish(
            callback_done=self.helpers.cb_skill_attach_done,
            callback_feedback=self.helpers.cb_skill_attach_feedback,
            wait=False
        )
        

    async def enter_GO_TO_ELEVATOR(self):

        await self.app.set_gary_footprint(
            footprint=GARY_SELECTED_CART_FOOTPRINT
        )
        
        current_package = self.helpers.get_current_package()
                
        copy_ui_screen = deepcopy(UI_SCREEN_NAV_TO_PACKAGE_POINT)
        message = copy_ui_screen['title'].replace(
            '[department_name]', 
            current_package['name']
        )
        copy_ui_screen['title'] = message
        # TODO add ui screen for elevator
        await self.app.ui.show_animation(**copy_ui_screen)
        
        execute_args = {
            'args': {
                'CSR_OWNER_USER_ID': self.app.selected_parking['user_id']
            },
            'steps': BASEMENT_ROUTES['go_to_elevators_after_attach']
        }
        await self.app.skill_nav_steps.execute_main(
            execute_args=execute_args,
            callback_done=self.helpers.cb_skill_done,
            callback_feedback=self.helpers.cb_skill_feedback,
            wait=False
        )


    async def aborted(self, error, msg):
        pass
