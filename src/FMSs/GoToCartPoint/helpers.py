import time

from src.FMSs.main.helpers import CommonHelpers

from src.static.constants import *
from src.app import RayaApplication
from src.static.leds import *
from src.static.sound import *
from src.static.constants import NAV_WAREHOUSE_ZONE_NAME

class Helpers(CommonHelpers):

    def __init__(self, app: RayaApplication):
        super().__init__(app)
        self.app = app


    async def check_if_inside_zone(self):
        result = await self.app.nav.is_in_zone(zone_name=NAV_WAREHOUSE_ZONE_NAME)
        return result


    async def nav_feedback_wrapper(self, code, msg, distance, speed):
        # if await self.check_if_inside_zone():
        #     await self.nav_feedback_door_async(code, msg, distance, speed)
        await self.nav_feedback_async(code, msg, distance, speed)
