from copy import copy
from src.FMSs.BaseAppFSM.actions import CommonAction
from raya.enumerations import FLEET_UPDATE_STATUS

from src.static import *

from .helpers import Helpers


class Actions(CommonAction):

    def __init__(self, app, helpers: Helpers):
        super().__init__(app=app, helpers=helpers)
        self.app = app
        self.helpers: Helpers


    async def enter_SETUP_ACTIONS(self):
        await self.app.fleet.update_app_status(
                status=FLEET_UPDATE_STATUS.INFO,
                message=FLEET_CHECK_IF_LOCALIZED
            )
        await self.app.ui.display_screen(**UI_SCREEN_LOCALIZING)
        map_name = WAREHOUSE_MAP_NAME
        self.app.log.warn(f'Setting map: {map_name}')
        await self.app.nav.set_map(map_name=map_name)
        await self.helpers.change_costmap_to_point(
            initial_point='home',
            final_point='elev',
        )


    async def enter_GO_TO_CART_POINT(self):
        await self.app.ui.show_animation(**UI_SCREEN_NAVIGATING)
        await self.app.fleet.update_app_status(
            status=FLEET_UPDATE_STATUS.INFO,
            message=FLEET_STATUS_GOING_TO_CART_POINT
        )
        self.helpers.fsm_take_cart.restart()
        await self.helpers.fsm_take_cart.run_in_background()


    async def enter_NAV_TO_WAITING_ELEVATOR(self):
        current_package = self.helpers.get_current_package()
        last_package = self.helpers.get_last_package()
        
        floor = self.app.get_current_floor_map_name()
        last_unit = self.app.get_unit_name(
            package_point_name=last_package['name']
        )
        
        route = f'{last_unit}_elev'
        self.log.warn(f'route #{route}')
        
        copy_ui_screen = copy(UI_SCREEN_NAV_TO_PACKAGE_POINT)
        message = copy_ui_screen['title'].replace(
            '[department_name]', 
            current_package['name']
        )
        copy_ui_screen['title'] = message
        await self.app.ui.show_animation(**copy_ui_screen)
        await self.app.fleet.update_app_status(
                status=FLEET_UPDATE_STATUS.INFO,
                message=copy_ui_screen['title']
            )
        
        # TODO in case that the route is not found, it should be handled
        steps = copy(SKILL_NAVIGATION[floor][route])
        execute_args = {
            'steps': steps
        }
        await self.app.skill_nav_steps.execute_main(
            execute_args=execute_args,
            callback_done=self.helpers.cb_nav_skill_done,
            callback_feedback=self.helpers.cb_nav_skill_feedback,
            wait=False
        )


    async def enter_NAV_TO_FLOOR(self):
        current_package = self.helpers.get_current_package()
        self.app.current_target_floor_map_name = \
            current_package['map_name'].split('__')[1]
        self.helpers.fsm_go_to_floor.restart()
        await self.helpers.fsm_go_to_floor.run_in_background()


    async def leave_NAV_TO_FLOOR(self):
        current_package = self.helpers.get_current_package()
        current_unit = self.app.get_unit_name(current_package['name'])
        
        await self.helpers.change_costmap_to_point(
            initial_point='elev',
            final_point=current_unit,
        )


    async def enter_NAV_TO_DELIVERY_POINT(self):
        current_package = self.helpers.get_current_package()
        last_package = self.helpers.get_last_package()
        
        floor = self.app.get_current_floor_map_name()
        last_unit = self.app.get_unit_name(
            package_point_name=last_package['name']
        )
        current_unit = self.app.get_unit_name(
            package_point_name=current_package['name']
        )
        
        route = f'{last_unit}_{current_unit}'
        self.log.warn(f'route #{route}')
        
        copy_ui_screen = copy(UI_SCREEN_NAV_TO_PACKAGE_POINT)
        message = copy_ui_screen['title'].replace(
            '[department_name]', 
            current_package['name']
        )
        copy_ui_screen['title'] = message
        await self.app.ui.show_animation(**copy_ui_screen)
        await self.app.fleet.update_app_status(
                status=FLEET_UPDATE_STATUS.INFO,
                message=copy_ui_screen['title']
            )
        
        # TODO in case that the route is not found, it should be handled
        steps = copy(SKILL_NAVIGATION[floor][route])
        execute_args = {
            'steps': steps
        }
        await self.app.skill_nav_steps.execute_main(
            execute_args=execute_args,
            callback_done=self.helpers.cb_nav_skill_done,
            callback_feedback=self.helpers.cb_nav_skill_feedback,
            wait=False
        )


    async def enter_NOTIFY_ORDER_ARRIVED(self):
        await self.helpers.notify_order_arrived()


    async def leave_NOTIFY_ORDER_ARRIVED(self):
        await self.helpers.custom_turn_off_leds()


    async def enter_WAIT_FOR_UI_CONFIRMATION(self):
        self.helpers.selected_option_delivery_ui = None
        await self.helpers.custom_animation(**LEDS_WAITING_FOR_DELIVERY_RESPONSE)
        await self.app.ui.display_choice_selector(
                **self.app.delivery_options(),
                wait=False,
                callback=self.helpers.cb_delivery_arrived_ui_response
            )
        self.app.create_task(
            name='Notify Task',
            afunc=self.helpers.task_to_notify
        )
        await self.app.fleet.update_app_status(
            status=FLEET_UPDATE_STATUS.INFO,
            message=FLEET_WAIT_FOR_PACKAGE_CONFIRMATION
        )


    async def leave_WAIT_FOR_UI_CONFIRMATION(self):
        self.app.cancel_task(
            name='Notify Task'
        )
        self.app.log.warn('task canceled')
        await self.helpers.custom_cancel_sound()
        await self.helpers.custom_turn_off_leds()


    async def enter_PACKAGE_DELIVERED(self):
        await self.app.fleet.update_app_status(
            status=FLEET_UPDATE_STATUS.SUCCESS,
            message=(
                f'The package {self.helpers.index_package + 1} '
                'was delivered successfully.'
            )
        )
        await self.app.ui.show_animation(**UI_SCREEN_DELIVERING_SUCCESS)


    async def leave_PACKAGE_DELIVERED(self):
        await self.helpers.custom_turn_off_leds()


    async def enter_PACKAGE_NOT_DELIVERED(self):
        await self.app.fleet.update_app_status(
                status=FLEET_UPDATE_STATUS.ERROR,
                message=(
                    f'The package {self.helpers.index_package + 1} '
                    'was not delivered.'
                )
            )
        await self.app.ui.show_animation(**UI_SCREEN_DELIVERING_SUCCESS)


    async def leave_PACKAGE_NOT_DELIVERED(self):
        await self.helpers.custom_cancel_sound()
        await self.helpers.custom_turn_off_leds()


    async def enter_NAV_TO_WAITING_ELEVATOR_TO_WAREHOUSE(self):
        last_package = self.helpers.get_last_package()    
        floor = self.app.get_current_floor_map_name()
        last_unit = self.app.get_unit_name(
            package_point_name=last_package['name']
        )
        
        await self.app.ui.show_animation(**UI_SCREEN_NAVIGATING)
        await self.app.fleet.update_app_status(
                status=FLEET_UPDATE_STATUS.INFO,
                message=FLEET_GOING_TO_WAREHOUSE
            )
        
        route = f'{last_unit}_elev'
        self.log.warn(f'route #{route}')
        
        await self.helpers.change_costmap_to_point(
            initial_point=last_unit,
            final_point='elev',
        )
        steps = copy(SKILL_NAVIGATION[floor][route])
        execute_args = {
            'steps': steps
        }
        await self.app.skill_nav_steps.execute_main(
            execute_args=execute_args,
            callback_done=self.helpers.cb_nav_skill_done,
            callback_feedback=self.helpers.cb_nav_skill_feedback,
            wait=False
        )


    async def leave_NAV_TO_WAITING_ELEVATOR_TO_WAREHOUSE(self):
        await self.helpers.custom_turn_off_leds()


    async def enter_NAV_TO_WAREHOUSE_FLOOR(self):
        await self.app.ui.show_animation(**UI_SCREEN_NAVIGATING)
        self.app.current_target_floor_map_name = WAREHOUSE_FLOOR
        self.helpers.fsm_go_to_floor.restart()
        await self.helpers.fsm_go_to_floor.run_in_background()


    async def enter_PARK_CART(self):
        await self.app.ui.show_animation(**UI_SCREEN_NAVIGATING)
        await self.helpers.change_costmap_to_point(
            initial_point='elev',
            final_point='home',
        )
        await self.app.fleet.update_app_status(
                status=FLEET_UPDATE_STATUS.INFO,
                message=FLEET_PARKING_CART
            )
        self.helpers.fsm_leave_cart.restart()
        await self.helpers.fsm_leave_cart.run_in_background()
