from src.FMSs.GoToCartPoint.helpers import Helpers as ParkCartHelpers
from src.app import RayaApplication
from src.static import *

class Helpers(ParkCartHelpers):

    def __init__(self, app: RayaApplication):     
        super().__init__(app)
        self.selected_elevator_ui = None
        self.teleoperation_response = None
        self.exit_elevator_id = None


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


    async def cb_exit_elevator_skill_finish(self, 
            finish_code, 
            finish_msg, 
            elevator_id: str
        ):
        self.app.log.debug((
            'cb_exit_elevator_skill_finish: '
            f'\t finish_code:{finish_code} '
            f'\t finish_msg:{finish_msg} '
            f'\t elevator_id:{elevator_id} '
        ))
        self.exit_elevator_id = str(elevator_id)


    async def cb_exit_elevator_skill_feedback(self, 
            feedback_code, feedback_msg
        ):
        self.app.log.debug((
            f'cb_exit_elevator_skill_feedback: {feedback_code} {feedback_msg}'
        ))


    async def get_entry_point_to_elevator(self):
        self.app.log.warn(f'self.selected_elevator {self.selected_elevator}')
        current_floor = self.app.get_current_floor_map_name()
        result = FLOORS[current_floor]['elevator'][self.selected_elevator]['entry_point']
        self.app.log.warn(f'point: {result}')
        return result

    
    async def get_elevator_leaving_point(self):
        self.app.log.warn(f'self.exit_elevator_id {self.exit_elevator_id}')
        target_floor = self.app.get_current_target_floor_map_name()
        result = FLOORS[target_floor]['elevator'][self.selected_elevator]
        self.app.log.warn(f'point: {result}')
        return result


    async def get_elevator_localization_points(self, inside_elevator=False):
        elevator = await self.get_elevator_leaving_point()
        result = []
        if inside_elevator:
            elevator_inside = elevator['localization']['inside_elevator']
            point = {
                'x': float(elevator_inside['x']),
                'y': float(elevator_inside['y']),
                'angle': float(elevator_inside['angle']),
                'pos_unit': elevator_inside['pos_unit'],
                'ang_unit': elevator_inside['ang_unit']
            }
            result.append(point)
        else:
            elevator_localization_info = elevator['localization']
            list_points = self.generate_divided_points(elevator_localization_info)
            result = list_points

        self.app.log.warn(f'points: {result}')
        return result


    def interpolate_points(self, point_a, point_b, divisions):
        """
        Generate intermediate points between two points based on the number of divisions.

        Args:
            point_a (dict): The starting point with keys 'x', 'y', 'angle', 'pos_unit', 'ang_unit'.
            point_b (dict): The ending point with keys 'x', 'y', 'angle', 'pos_unit', 'ang_unit'.
            divisions (int): Number of divisions to create between the points.

        Returns:
            list: A list of dictionaries representing the interpolated points.
        """
        points = []
        for i in range(divisions + 1):
            fraction = i / divisions
            interpolated_point = {
                'x': point_a['x'] + fraction * (point_b['x'] - point_a['x']),
                'y': point_a['y'] + fraction * (point_b['y'] - point_a['y']),
                'angle': point_a['angle'] + fraction * (point_b['angle'] - point_a['angle']),
                'pos_unit': point_a['pos_unit'],
                'ang_unit': point_a['ang_unit'],
            }
            if point_a['pos_unit'] == POSITION_UNIT.PIXELS:
                interpolated_point['x'] = round(interpolated_point['x'])
                interpolated_point['y'] = round(interpolated_point['y'])
            
            interpolated_point['x'] = float(interpolated_point['x'])
            interpolated_point['y'] = float(interpolated_point['y'])
            interpolated_point['angle'] = float(interpolated_point['angle'])
            points.append(interpolated_point)
        return points


    def generate_midpoints(self, localization):
        """
        Generate midpoints of each division based on the localization dictionary.

        Args:
            localization (dict): The localization dictionary.

        Returns:
            list: A list of dictionaries representing the midpoints.
        """
        divisions = localization['outside_elevator']['divisions']
        point_a = localization['outside_elevator']['closest_point']
        point_b = localization['outside_elevator']['farthest_point']
        
        divided_points = self.interpolate_points(point_a, point_b, divisions)
        midpoints = []
        
        for i in range(len(divided_points) - 1):
            midpoint = {
                'x': (divided_points[i]['x'] + divided_points[i + 1]['x']) / 2,
                'y': (divided_points[i]['y'] + divided_points[i + 1]['y']) / 2,
                'angle': (divided_points[i]['angle'] + divided_points[i + 1]['angle']) / 2,
                'pos_unit': divided_points[i]['pos_unit'],
                'ang_unit': divided_points[i]['ang_unit'],
            }
            if divided_points[i]['pos_unit'] == POSITION_UNIT.PIXELS:
                midpoint['x'] = round(midpoint['x'])
                midpoint['y'] = round(midpoint['y'])
                
            midpoint['x'] = float(midpoint['x'])
            midpoint['y'] = float(midpoint['y'])
            midpoint['angle'] = float(midpoint['angle'])
            midpoints.append(midpoint)
        
        return midpoints


    def generate_divided_points(self, localization):
        """
        Generate divided points based on the localization dictionary.

        Args:
            localization (dict): The localization dictionary.

        Returns:
            dict: A dictionary with the interpolated points.
        """
        divisions = localization['outside_elevator']['divisions']
        point_a = localization['outside_elevator']['closest_point']
        point_b = localization['outside_elevator']['farthest_point']
        
        divided_points = self.interpolate_points(point_a, point_b, divisions)
        return divided_points
