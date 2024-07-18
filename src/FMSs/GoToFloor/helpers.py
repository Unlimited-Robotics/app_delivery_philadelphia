from src.FMSs.GoToCartPoint.helpers import Helpers as ParkCartHelpers
from src.app import RayaApplication
from src.static import *

class Helpers(ParkCartHelpers):

    def __init__(self, app: RayaApplication):     
        super().__init__(app)
        self.selected_elevator_ui = None
        self.teleoperation_response = None


    def cb_delivery_arrived_ui_response(self, response):
        self.selected_elevator_ui = response['selected_option']


    def cb_teleoperation_ui_response(self, response):
        self.teleoperation_response = response


    def cb_set_map_feedback(self, feedback_code, feedback_msg):
        self.app.log.info(f'set map feedback: {feedback_code} {feedback_msg}')


    def cb_set_map_finish(self, error, error_msg):
        if error != 0:
            self.app.log.error(f'set map finish: {error} {error_msg}')
        else:
            self.app.log.info('set map finish: success')


    async def get_elevator_waiting_point(self):
        self.app.log.warn(f'self.selected_elevator_ui {self.selected_elevator_ui}')
        index_elevator = int(self.selected_elevator_ui['id'])
        return NAV_ELEVATOR_WAITING_POINT[index_elevator]

    
    async def get_elevator_leaving_point(self):
        self.app.log.warn(f'self.selected_elevator_ui {self.selected_elevator_ui}')
        index_elevator = int(self.selected_elevator_ui['id'])
        return NAV_ELEVATOR_LEAVING_POINT[index_elevator]


    async def get_elevator_localization_points(self):
        index_elevator = int(self.selected_elevator_ui['id'])
        result = {
            'x': NAV_ELEVATOR_LEAVING_POINT[index_elevator]['x'],
            'y': NAV_ELEVATOR_LEAVING_POINT[index_elevator]['y'],
            'angle': NAV_ELEVATOR_LEAVING_POINT[index_elevator]['angle'],
        }
        return result
