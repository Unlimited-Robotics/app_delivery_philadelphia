import time

from src.FMSs.BaseAppFSM.helpers import CommonHelpers

from src.static.constants import *
from src.static.leds import *
from src.static.sound import *
from src.static.constants import NAV_WAREHOUSE_ZONE_NAME

class Helpers(CommonHelpers):

    def __init__(self, app):
        super().__init__(app=app)
        self.approach_error_code = None
        self.log_fb_approach_control = {}


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


    def is_approach_done(self):
        return (self.approach_error_code is not None)


    def was_approach_success(self):
        return (self.approach_error_code==0)


    def cb_finish_approach_skill(self, error_code, error_msg, x_error, y_error, angle_error):
        self.approach_error_code = error_code
        if error_code != 0:
            self.app.log.error('Approach skill failed:')
            self.app.log.error(f'  error_code: {error_code}')
            self.app.log.error(f'  error_msg: {error_msg}')


    def cb_feedback_approach_skill(self, feedback_code, feedback_msg, x_error, y_error, angle_error):
        # Feedbacks:
        #   109: Obstacle detected
        # if feedback_code in [3]:
        #     if feedback_code not in self.log_fb_approach_control or \
        #         time.time()>(self.log_fb_approach_control[feedback_code] + LOG_MIN_PERIOD):
                self.app.log.warn('Approach skill warning:')
                self.app.log.warn(f'  feedback_code: {feedback_code}')
                self.app.log.warn(f'  feedback_msg: {feedback_msg}')
                # self.log_fb_approach_control[feedback_code] = time.time()
