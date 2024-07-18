from copy import copy
from src.FMSs.BaseAppFSM.actions import CommonAction
from raya.enumerations import POSITION_UNIT, ANGLE_UNIT, FLEET_UPDATE_STATUS
from raya.exceptions import RayaCommandAlreadyRunning

from src.app import RayaApplication
from src.static import *

from .helpers import Helpers


class Actions(CommonAction):

    def __init__(self, app: RayaApplication, helpers: Helpers):
        super().__init__(app=app,helpers=helpers)
        self.app = app
        self.helpers = helpers


    async def enter_SETUP_ACTIONS(self):
        await self.app.fleet.update_app_status(
                status=FLEET_UPDATE_STATUS.INFO,
                message=FLEET_CHECK_IF_LOCALIZED
            )
        await self.app.ui.display_screen(**UI_SCREEN_LOCALIZING)
        map_name = WAREHOUSE_MAP_NAME
        self.app.log.warn(f'Setting map: {map_name}')
        await self.app.nav.set_map(map_name=map_name)


    async def enter_GO_TO_CART_POINT(self):
        await self.app.fleet.update_app_status(
            status=FLEET_UPDATE_STATUS.INFO,
            message=FLEET_STATUS_GOING_TO_CART_POINT
        )
        self.helpers.fsm_go_to_cart_point.restart()
        await self.helpers.fsm_go_to_cart_point.run_in_background()


    async def enter_NAV_TO_WAITING_ELEVATOR(self):
        point = await self.helpers.get_elevator_waiting_point()
        copy_ui_screen = copy(UI_SCREEN_NAV_TO_PACKAGE_POINT)
        # TODO: replace map name with location name
        current_package_location_name = self.helpers.current_package['map_name']
        message = copy_ui_screen['title'].replace(
            '[department_name]', 
            current_package_location_name
        )
        copy_ui_screen['title'] = message
        await self.app.ui.show_animation(**copy_ui_screen)
        await self.app.fleet.update_app_status(
                status=FLEET_UPDATE_STATUS.INFO,
                message=copy_ui_screen['title']
            )
        if not self.app.nav.is_navigating():
            await self.app.nav.navigate_to_position(
                **point,
                callback_feedback_async=self.helpers.nav_feedback_async,
                callback_finish_async=self.helpers.nav_finish_async,
            )


    async def leave_NAV_TO_WAITING_ELEVATOR(self):
        await self.app.custome_turn_off_leds()


    async def enter_NAV_TO_FLOOR(self):
        self.app.current_target_floor_map_name = \
            self.helpers.current_package['map_name'].split('__')[1]
        self.helpers.fsm_go_to_floor.restart()
        await self.helpers.fsm_go_to_floor.run_in_background()


    async def enter_NAV_TO_DELIVERY_POINT(self):
        point = await self.helpers.get_current_package_point()
        copy_ui_screen = copy(UI_SCREEN_NAV_TO_PACKAGE_POINT)
        # TODO: replace map name with location name
        current_package_location_name = self.helpers.current_package['map_name']
        message = copy_ui_screen['title'].replace(
            '[department_name]', 
            current_package_location_name
        )
        copy_ui_screen['title'] = message
        await self.app.ui.show_animation(**copy_ui_screen)
        await self.app.fleet.update_app_status(
                status=FLEET_UPDATE_STATUS.INFO,
                message=copy_ui_screen['title']
            )
        if not self.app.nav.is_navigating():
            await self.app.nav.navigate_to_position(
                **point,
                callback_feedback_async=self.helpers.nav_feedback_async,
                callback_finish_async=self.helpers.nav_finish_async,
            )


    async def enter_NOTIFY_ORDER_ARRIVED(self):
        await self.helpers.notify_order_arrived()


    async def leave_NOTIFY_ORDER_ARRIVED(self):
        await self.app.custome_turn_off_leds()


    async def enter_WAIT_FOR_UI_CONFIRMATION(self):
        self.helpers.selected_option_delivery_ui = None
        await self.app.leds.animation(**LEDS_WAITING_FOR_DELIVERY_RESPONSE)
        await self.app.ui.display_choice_selector(
                **UI_SCREEN_OPTIONS_DELIVERY_ARRIVED,
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
        await self.app.custom_cancel_sound()
        # TODO: remove this
        # await self.app.motion.rotate(angle=-90.0, angular_speed=45.0, wait=True, enable_obstacles=False)
        await self.app.custome_turn_off_leds()


    async def enter_PACKAGE_DELIVERED(self):
        await self.app.fleet.update_app_status(
            status=FLEET_UPDATE_STATUS.SUCCESS,
            message=(
                f'The package {self.helpers.index_package + 1} '
                'was delivered successfully.'
            )
        )
        await self.app.ui.display_screen(
            **UI_SCREEN_DELIVERING_SUCCESS
        )


    async def leave_PACKAGE_DELIVERED(self):
        await self.app.custome_turn_off_leds()


    async def enter_PACKAGE_NOT_DELIVERED(self):
        await self.app.fleet.update_app_status(
                status=FLEET_UPDATE_STATUS.ERROR,
                message=(
                    f'The package {self.helpers.index_package + 1} '
                    'was not delivered.'
                )
            )
        await self.app.ui.display_screen(**UI_PACKAGE_NOT_DELIVERED)


    async def leave_PACKAGE_NOT_DELIVERED(self):
        await self.app.custom_cancel_sound()
        await self.app.custome_turn_off_leds()


    async def enter_NAV_TO_WAREHOUSE_FLOOR(self):
        self.app.current_target_floor_map_name = WAREHOUSE_FLOOR
        self.helpers.fsm_go_to_floor.restart()
        await self.helpers.fsm_go_to_floor.run_in_background()


    async def enter_RETURN_TO_WAREHOUSE_ENTRANCE(self):
        await self.app.fleet.update_app_status(
                status=FLEET_UPDATE_STATUS.INFO,
                message=FLEET_RETURNING_TO_WAREHOUSE
            )
        await self.app.ui.show_animation(**UI_SCREEN_NAV_TO_WAREHOUSE)
        await self.app.nav.navigate_to_position(
                **NAV_WAREHOUSE_ENTRANCE,
                callback_feedback_async=self.helpers.nav_feedback_async,
                callback_finish_async=self.helpers.nav_finish_async,
            )


    async def leave_RETURN_TO_WAREHOUSE_ENTRANCE(self):
        await self.app.custome_turn_off_leds()


    async def enter_PARK_CART(self):
        await self.app.fleet.update_app_status(
                status=FLEET_UPDATE_STATUS.INFO,
                message=FLEET_PARKING_CART
            )
        self.helpers.fsm_park_cart.restart()
        await self.helpers.fsm_park_cart.run_in_background()


    async def enter_GO_TO_HOME_LOCATION(self):
        await self.app.fleet.update_app_status(
                status=FLEET_UPDATE_STATUS.INFO,
                message=FLEET_GOING_TO_HOME_LOCATION
            )
        home = await self.helpers.get_home_position()
        await self.app.nav.navigate_to_position(
            **home,
            callback_feedback_async=self.helpers.nav_feedback_async,
            callback_finish_async=self.helpers.nav_finish_async,
            wait=False
        )


    async def enter_NOTIFY_ALL_PACKAGES_STATUS(self):
        await self.app.fleet.update_app_status(
                status=FLEET_UPDATE_STATUS.INFO,
                message=FLEET_ALL_POINTS_REACHED
            )


    async def leave_NOTIFY_ALL_PACKAGES_STATUS(self):
        await self.app.custome_turn_off_leds()
