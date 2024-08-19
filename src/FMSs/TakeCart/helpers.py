from src.FMSs.BaseAppFSM.helpers import CommonHelpers

from src.static.constants import *
from src.static.leds import *
from src.static.sound import *
from src.static.constants import NAV_WAREHOUSE_ZONE_NAME

class Helpers(CommonHelpers):

    def __init__(self, app):
        super().__init__(app=app)


    async def check_if_inside_zone(self):
        result = await self.app.nav.is_in_zone(zone_name=NAV_WAREHOUSE_ZONE_NAME)
        return result
        

    async def cb_skill_done(self, exception, result):
        self.app.log.debug(
            f'Callback skill done: '
            f'Result: \'{result}\'.'
        )


    async def cb_skill_feedback(self, feedback):
        self.app.log.debug(
            f'Callback Feedback: \'{feedback}\''
        )
