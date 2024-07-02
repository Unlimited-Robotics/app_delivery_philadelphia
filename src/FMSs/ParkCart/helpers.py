from src.FMSs.GoToCartPoint.helpers import Helpers as ParkCartHelpers
from src.app import RayaApplication


class Helpers(ParkCartHelpers):

    def __init__(self, app: RayaApplication):     
        super().__init__(app)


    async def cb_skill_detach_done(self, exception, result):
        self.app.log.info(f'cb_skill_detach_done, result: {result}')
        if exception is None:
            await self.app.skill_att2cart.execute_finish()
        else: 
            self.app.log.warn(
                'error occured while attaching, exception type: '
                f'{type(exception)} {exception}'
            )


    async def cb_skill_dettach_feedback(self, feedback):
        self.app.log.info(feedback)