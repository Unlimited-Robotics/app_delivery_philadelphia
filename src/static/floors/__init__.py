import math

from raya.enumerations import POSITION_UNIT, ANGLE_UNIT

from .basement import *
from .floor_02 import *
from .floor_07 import *


NAVIGATION_OPTIONS_WITH_CART = {
    'options': {
        'behavior_tree': 'replan_if_needed_long_footprint'
    }
}

def rotate_180(nav_point):
    if nav_point['ang_unit'] == ANGLE_UNIT.RADIANS:
        new_angle = nav_point['angle'] + math.pi
        # Ensure the angle is within the range [-pi, pi]
        if new_angle > math.pi:
            new_angle -= 2 * math.pi
    elif nav_point['ang_unit'] == ANGLE_UNIT.DEGREES:
        new_angle = nav_point['angle'] + 180
        # Ensure the angle is within the range [-180, 180]
        if new_angle > 180:
            new_angle -= 360
    else:
        raise ValueError("Unsupported angle unit")
    
    return {
        **nav_point,
        'angle': new_angle,
    }
