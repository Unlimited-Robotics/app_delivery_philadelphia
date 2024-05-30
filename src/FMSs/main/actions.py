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
from src.static.constants import *
from raya.enumerations import POSITION_UNIT, ANGLE_UNIT
from raya.exceptions import RayaCommandAlreadyRunning, RayaTaskAlreadyRunning

class Actions(BaseActions):

    def __init__(self, app: RayaApplication, helpers: Helpers):
        super().__init__()
        self.app = app
        self.helpers = helpers


    async def enter_SETUP_ACTIONS(self):
        await self.app.fleet.update_app_status(
                status=FLEET_UPDATE_STATUS.INFO,
                message=FLEET_CHECK_IF_LOCALIZED
            )
        await self.app.ui.display_screen(**UI_SCREEN_LOCALIZING)
        await self.app.nav.set_map(NAV_WAREHOUSE_MAP_NAME)


    async def enter_GO_TO_CART_POINT(self):
        await self.app.fleet.update_app_status(
            **FLEET_STATUS_GOING_TO_CART_POINT
            )
        self.helpers.fsm_go_to_cart_point.restart()
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
        await self.helpers.gary_play_audio(
            audio=SOUND_NOTIFY_ORDER_ARRIVED,
            wait=True
        )
        self.app.log.warn('NOTIFY_ORDER_ARRIVED')


    async def leave_NOTIFY_ORDER_ARRIVED(self):
        await self.app.sound.cancel_all_sounds()
        await self.app.leds.turn_off_all()


    async def enter_WAIT_FOR_CHEST_CONFIRMATION(self):
        await self.app.ui.display_screen(**UI_SCREEN_DELIVERING_ARRIVE)
        self.app.create_task(
            name='Notify Task',
            afunc=self.helpers.task_to_notify
        )
        try:
            await self.app.leds.animation(
                **LEDS_WAIT_FOR_BUTTON_CHEST_BUTTON,
                wait=True
            )
        except RayaCommandAlreadyRunning:
            pass


    async def leave_WAIT_FOR_CHEST_CONFIRMATION(self):
        self.app.cancel_task(
            name='Notify Task'
        )
        self.app.log.warn('task canceled')
        await self.app.sound.cancel_all_sounds()
        await self.app.leds.turn_off_all()


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
        await self.helpers.gary_play_audio(
            audio=SOUND_PACKAGE_DELIVERED,
            wait=True
        )


    async def leave_PACKAGE_DELIVERED(self):
        await self.app.sound.cancel_all_sounds()
        await self.app.leds.turn_off_all()


    async def enter_PACKAGE_NOT_DELIVERED(self):
        await self.app.fleet.update_app_status(
                status=FLEET_UPDATE_STATUS.ERROR,
                message=(
                    f'The package {self.helpers.index_package + 1} '
                    'was not delivered.'
                )
            )
        await self.app.ui.display_screen(**UI_PACKAGE_NOT_DELIVERED)
        await self.helpers.gary_play_audio(
            audio=SOUND_PACKAGE_NOT_CONFIRMED,
            wait=True
        )


    async def leave_PACKAGE_NOT_DELIVERED(self):
        await self.app.sound.cancel_all_sounds()
        await self.app.leds.turn_off_all()


    async def enter_RETURN_TO_WAREHOUSE_ENTRANCE(self):
        await self.app.fleet.update_app_status(
                status=FLEET_UPDATE_STATUS.INFO,
                message=FLEET_RETURNING_TO_WAREHOUSE
            )
        await self.app.ui.display_screen(**UI_SCREEN_NAV_TO_WAREHOUSE_RETURN)
        await self.app.nav.navigate_to_position(
                **NAV_WAREHOUSE_ENTRANCE,
                callback_feedback_async=self.helpers.nav_feedback_async,
                callback_finish_async=self.helpers.nav_finish_async,
            )
        await self.helpers.gary_play_audio(
            audio=SOUND_RETURNING_TO_WAREHOUSE,
            wait=True
        )


    async def leave_RETURN_TO_WAREHOUSE_ENTRANCE(self):
        await self.app.sound.cancel_all_sounds()
        await self.app.leds.turn_off_all()


    async def enter_PARK_CART(self):
        self.helpers.fsm_park_cart.restart()
        await self.helpers.fsm_park_cart.run_in_background()


    async def enter_NOTIFY_ALL_PACKAGES_STATUS(self):
        await self.app.fleet.update_app_status(
                status=FLEET_UPDATE_STATUS.INFO,
                message=FLEET_ALL_POINTS_REACHED
            )
        await self.app.ui.display_screen(**UI_SCREEN_ALL_PACKAGES_DONE)
        await self.helpers.gary_play_audio(
            audio=SOUND_ALL_POINTS_VISITED,
            wait=True
        )


    async def leave_NOTIFY_ALL_PACKAGES_STATUS(self):
        await self.app.sound.cancel_all_sounds()
        await self.app.leds.turn_off_all()

    
    async def aborted(self, error, msg):
        await self.app.fleet.update_app_status(
                status=FLEET_UPDATE_STATUS.ERROR,
                message=f'The App was aborted, error [{error}]: {msg}'
            )
        await self.app.ui.display_screen(
                subtitle=f'ERROR {error}: {msg}',
                **UI_SCREEN_FAILED
            )
        await self.app.sound.play_sound(name='attention')
    
    # REQUEST_FOR_HELP STATES
    
    async def enter_REQUEST_FOR_HELP(self):
        await self.app.fleet.update_app_status(
                status=FLEET_UPDATE_STATUS.WARNING,
                message=FLEET_REQUESTING_FOR_HELP
            )
        await self.app.ui.display_screen(**UI_SCREEN_REQUEST_FOR_HELP)     


    async def enter_WAIT_FOR_HELP(self):
        pass


    async def leave_WAIT_FOR_HELP(self):
        self.app.cancel_task(
            name='task_to_wait_for_help'
        )
        self.app.log.warn('task \'task_to_wait_for_help\' canceled')
        await self.app.sound.cancel_all_sounds()
        await self.app.leds.turn_off_all()


    async def enter_RELEASE_CART(self):
        await self.app.ui.display_screen(**UI_SCREEN_RELEASE_CART)
        await self.app.sleep(TIME_TO_RELEASE_CART)