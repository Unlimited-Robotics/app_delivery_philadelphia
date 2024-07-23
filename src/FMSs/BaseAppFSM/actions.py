from raya.tools.fsm import BaseActions
from raya.enumerations import FLEET_UPDATE_STATUS

from src.app import RayaApplication
from src.static import *

from .helpers import Helpers


class CommonAction(BaseActions):
    def __init__(self, app: RayaApplication, helpers: Helpers):
        super().__init__()
        self.app = app
        self.helpers = helpers

    # REQUEST_FOR_HELP STATES
        
    async def REQUEST_FOR_HELP_to_CONTINUE(self):
        self.helpers.increase_retry_counter()


    async def enter_WAIT_FOR_HELP(self):  
        await self.app.fleet.update_app_status(
            status=FLEET_UPDATE_STATUS.WARNING,
            message=FLEET_WAITING_FOR_HELP
        )


    async def WAIT_FOR_HELP_to_CONTINUE(self):
        self.helpers.reset_retry_counter()


    async def leave_WAIT_FOR_HELP(self):
        await self.app.custom_turn_off_leds()


    async def enter_RELEASE_CART(self):
        self.app.log.warn('Releasing cart...')
        await self.app.fleet.update_app_status(
                status=FLEET_UPDATE_STATUS.WARNING,
                message=FLEET_ABORT_APP_RELEASE_CART
            )
        await self.app.ui.display_screen(**UI_SCREEN_RELEASE_CART)
        await self.app.skill_detach.execute_main(
            execute_args=EXECUTION_ARG_DETACH_SKILL,
            callback_done=self.helpers.cb_skill_detach_done,
            callback_feedback=self.helpers.cb_skill_dettach_feedback,
            wait=False
        )


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
