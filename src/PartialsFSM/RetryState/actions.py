import typing
if typing.TYPE_CHECKING:
    from src.app import RayaApplication

from ..CommonFSM import CommonActions
from .helpers import Helpers
from .constants import *


class Actions(CommonActions):
    
    def __init__(self, app: 'RayaApplication', helpers: Helpers):
        super().__init__(app=app, helpers=helpers)
        self.helpers: Helpers


    async def REQUEST_FOR_HELP_to_CONTINUE(self):
        self.helpers.increase_retry_counter()


    async def enter_WAIT_FOR_HELP(self):  
        await self.app.ui.display_choice_selector(
            **UI_SCREEN_WAIT_FOR_HELP_SELECTOR,
            wait=False,
            async_callback=self.helpers.display_choice_selector_callback,
            dont_save_last_ui=True
        )
        self.helpers.start_timer_teleoperator()


    async def leave_WAIT_FOR_HELP(self):
        self.helpers._ui_response_wait_for_help = None
        await self.helpers.custom_turn_off_leds()


    async def WAIT_FOR_HELP_to_CONTINUE(self):
        self.helpers.reset_retry_counter()


    async def enter_ABORT(self):
        self.log.error('Aborting the App')


    async def aborted(self, error, msg):
        pass