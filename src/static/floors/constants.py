from raya.enumerations import POSITION_UNIT, ANGLE_UNIT
import math

NAVIGATION_OPTIONS_WITHOUT_CART = {
    'options': {
        'behavior_tree': 'navigate_and_replan_if_needed'
    },
    'xy_tolerance': 0.05,
}

NAVIGATION_OPTIONS_WITH_CART = {
    'options': {
        'behavior_tree': 'nav_with_cart_restricted'
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
