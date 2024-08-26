import typing
if typing.TYPE_CHECKING:
    from src.app import RayaApplication

from ..CommonType import CommonActions

from .errors import *
from .constants import *
from .helpers import Helpers


class Actions(CommonActions):

    def __init__(self, app: 'RayaApplication', helpers: Helpers):
        super().__init__(app=app, helpers=helpers)
        self.helpers: Helpers
    
    
    async def enter_SETUP(self):
        pass
    
    
    async def enter_TELEOPERATION(self):
        # TODO: Request teleoperation
        await self.app.ui.display_action_screen(
            **UI_CALL_TO_ACTION_TELEOPERATION_DONE,
            wait=False,
            callback=self.helpers.cb_teleoperation_ui_response,
            dont_save_last_ui=True
        )


    async def enter_END(self):
        await self.app.ui.show_last_animation()
