from src.PartialsFSM.RetryState import Actions as RetryActions

from raya.enumerations import FLEET_UPDATE_STATUS

from src.app import RayaApplication
from src.static import *

from .helpers import CommonHelpers


class CommonAction(RetryActions):

    def __init__(self, app: RayaApplication, helpers: CommonHelpers):
        super().__init__(app=app, helpers=helpers)
        self.helpers: CommonHelpers


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
