from raya.tools.fsm import BaseActions
from raya.enumerations import FLEET_UPDATE_STATUS

from src.app import RayaApplication
from src.static.navigation import *
from src.static.ui import *
from src.static.constants import *
from src.static.fleet import *
from src.static.leds import *
from src.static.sound import *
from .helpers import Helpers
from raya.enumerations import POSITION_UNIT, ANGLE_UNIT


class Actions(BaseActions):

    def __init__(self, app: RayaApplication, helpers: Helpers):
        super().__init__()
        self.app = app
        self.helpers = helpers


    async def enter_SETUP_ACTIONS(self):
        await self.app.fleet.update_app_status(
                status=FLEET_UPDATE_STATUS.INFO,
                message='Checking if robot is localized'
            )
        await self.app.ui.display_screen(**UI_SCREEN_LOCALIZING)
        await self.app.nav.set_map(NAV_WAREHOUSE_MAP_NAME)


    async def enter_GO_TO_CART_POINT(self):
        await self.helpers.fsm_go_to_cart_point.run_in_background()


    async def enter_NAV_TO_DELIVERY_POINT(self):
        package , floor = self.helpers.current_package
        point = {
            'x': package[0],
            'y': package[1],
            'angle': package[2],
            'pos_unit': POSITION_UNIT.PIXELS, 
            'ang_unit': ANGLE_UNIT.DEGREES,
        }
        text = (   
            f'Delivering package {self.helpers.index_package + 1} '
            f'of {len(self.app.locations)}'
        )
        UI_SCREEN_NAV_TO_PACKAGE_FLOOR['subtitle'] = text
        await self.app.ui.display_screen(**UI_SCREEN_NAV_TO_PACKAGE_FLOOR)
        await self.app.fleet.update_app_status(
                status=FLEET_UPDATE_STATUS.INFO,
                message=text
            )
        await self.app.nav.navigate_to_position(
            **point,
            callback_feedback_async=self.helpers.nav_feedback_async,
            callback_finish_async=self.helpers.nav_finish_async,
        )


    async def enter_NOTIFY_ORDER_ARRIVED(self):
        await self.app.fleet.update_app_status(
                status=FLEET_UPDATE_STATUS.WARNING,
                message=(
                    f'The package {self.helpers.index_package + 1} '
                    'has arrived at the delivery point.'
                )
            )
        
        await self.app.leds.animation(
            **LEDS_NOTIFY_ORDER_ARRIVED, 
            wait=False
        )
        await self.app.sound.play_sound(
            **SOUND_NOTIFY_ORDER_ARRIVED,
            wait=True,
        )
        await self.app.leds.turn_off_all()


    async def enter_WAIT_FOR_CHEST_CONFIRMATION(self):
        await self.app.ui.display_screen(**UI_SCREEN_DELIVERING_ARRIVE)


    async def exit_WAIT_FOR_CHEST_CONFIRMATION(self):
        await self.app.sound.cancel_all_sounds()
        await self.app.leds.turn_off_all()


    async def WAIT_FOR_CHEST_CONFIRMATION_to_PACKAGE_DELIVERED(self):
        await self.app.fleet.update_app_status(
                status=FLEET_UPDATE_STATUS.SUCCESS,
                message=(
                    f'The package {self.helpers.index_package + 1} '
                    'was delivered successfully.'
                )
            )

    
    async def enter_PACKAGE_DELIVERED(self):
        await self.app.ui.display_screen(
            **UI_SCREEN_DELIVERING_CONFIRMATION_ON_FLEET
        )


    async def enter_PACKAGE_NOT_DELIVERED(self):
        await self.app.fleet.update_app_status(
                status=FLEET_UPDATE_STATUS.ERROR,
                message=(
                    f'The package {self.helpers.index_package + 1} '
                    'was not delivered.'
                )
            )
        await self.app.ui.display_screen(**UI_PACKAGE_NOT_DELIVERED)


    async def enter_RETURN_TO_WAREHOUSE(self):
        await self.app.fleet.update_app_status(
                status=FLEET_UPDATE_STATUS.INFO,
                message=(
                    'All packages were delivered, '
                    'returning to the warehouse floor.'
                )
            )
        await self.app.ui.display_screen(**UI_SCREEN_NAV_TO_WAREHOUSE_RETURN)
        await self.app.leds.animation(
            **LEDS_ALL_PACKAGES_DELIVERED,
            wait=False
        )
        await self.app.sound.play_sound(
            **SOUND_ALL_PACKAGES_DELIVERED,
            wait=True,
        )
        await self.app.nav.navigate_to_position(
                **NAV_WAREHOUSE_ENTRANCE,
                callback_feedback_async=self.helpers.nav_feedback_async,
                callback_finish_async=self.helpers.nav_finish_async,
            )


    async def enter_GO_TO_RELEASE_POINT(self):
        await self.app.fleet.update_app_status(
                status=FLEET_UPDATE_STATUS.INFO,
                message='The robot is deattaching from the cart.'
            )
        await self.app.ui.display_screen(**UI_SCREEN_DEATTACHING_TO_CART)
        await self.app.nav.navigate_to_position(
                **NAV_CART_POINT,
                callback_feedback_async=self.helpers.nav_feedback_async,
                callback_finish_async=self.helpers.nav_finish_async,
            )


    async def enter_NOTIFY_ALL_PACKAGES_STATUS(self):
        await self.app.fleet.update_app_status(
                status=FLEET_UPDATE_STATUS.INFO,
                message='All packages were delivered successfully.'
            )
        await self.app.ui.display_screen(**UI_SCREEN_DELIVERING_SUCESS)
        await self.app.sound.play_sound(name='success', wait=True)


    async def enter_REQUEST_FOR_HELP(self):
        await self.app.fleet.update_app_status(
                status=FLEET_UPDATE_STATUS.ERROR,
                message='Gary needs help.'
        )
        await self.app.ui.display_screen(**UI_SCREEN_GARY_NEEDS_HELP)
        await self.app.sound.play_sound(name='error')


    async def enter_WAIT_FOR_CHEST_BY_OPERATOR(self):
        await self.app.fleet.update_app_status(
                status=FLEET_UPDATE_STATUS.INFO,
                message='Waiting for operator.'
        )
        await self.app.ui.display_screen(**UI_SCREEN_GARY_NEEDS_HELP_TO_CONTINUE)


    async def enter_RELEASE_CART(self):
        await self.app.ui.display_screen(**UI_SCREEN_RELEASE_CART)

    
    async def aborted(self, error, msg):
        await self.app.fleet.update_app_status(
                status=FLEET_UPDATE_STATUS.ERROR,
                message=f'The App was aborted, error [{error}]: {msg}'
            )
        await self.app.ui.display_screen(
                subtitle=f'ERROR {error}: {msg}',
                **UI_SCREEN_FAILED
            )
        await self.app.sound.play_sound(name='error')
