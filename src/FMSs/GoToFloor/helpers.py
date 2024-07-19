from src.FMSs.GoToCartPoint.helpers import Helpers as ParkCartHelpers
from src.app import RayaApplication
from src.static import *

class Helpers(ParkCartHelpers):

    def __init__(self, app: RayaApplication):     
        super().__init__(app)
        self.selected_elevator_ui = None
        self.teleoperation_response = None


    def cb_delivery_arrived_ui_response(self, response):
        self.selected_elevator_ui = response['selected_option']['id']


    def cb_teleoperation_ui_response(self, response):
        self.teleoperation_response = response


    def cb_set_map_feedback(self, feedback_code, feedback_msg):
        self.app.log.debug(f'set map feedback: {feedback_code} {feedback_msg}')


    def cb_set_map_finish(self, error, error_msg):
        if error != 0:
            self.app.log.error(f'set map finish: {error} {error_msg}')
        else:
            self.app.log.info('set map finish: success')


    async def get_elevator_entering_point(self):
        self.app.log.warn(f'self.selected_elevator {self.selected_elevator}')
        current_floor = self.app.get_current_floor_map_name()
        return FLOORS[current_floor]['elevator'][self.selected_elevator]['entering']

    
    async def get_elevator_leaving_point(self):
        self.app.log.warn(f'self.selected_elevator {self.selected_elevator}')
        target_floor = self.app.get_current_target_floor_map_name()
        return FLOORS[target_floor]['elevator'][self.selected_elevator]['leaving']


    async def get_elevator_localization_points(self):
        elevator_leaving_point = await self.get_elevator_leaving_point()
        result = {
            'x': elevator_leaving_point['x'],
            'y': elevator_leaving_point['y'],
            'angle': elevator_leaving_point['angle'],
        }
        return result
