from .constants import *

from raya.enumerations import POSITION_UNIT, ANGLE_UNIT

elevator_1_max = [371, 1531, 1.5878862157515665]
elevator_1_min = [371, 1605, 1.5797524512953205]
elevator_2_max = [240, 1517, 1.5624154823821856]
elevator_2_min = [238, 1612, 1.5693645530871574]
elevator_3_max = [123, 1503, 1.5713002686320687]
elevator_3_min = [121, 1582, 1.5338153848607836]
unit_1 = [1277, 382, 0.009900601676800371]
unit_2 = [1473, 2124, 0.057483839596256914]
wait_elevator_r = [582, 1557, -3.1007792281373283]
wait_elevator_2 = [483, 1561, -3.1048970776125806]
wait_elevator_l = [588, 1622, -3.118875630383247]

ELEVATORS_ZONE_NAME = 'elevator_zone'

SELECTED_WAITING_ELEVATOR = wait_elevator_l

FLOOR_7_INFO = {
    'waiting_elevator': {
        'x': float(SELECTED_WAITING_ELEVATOR[0]),
        'y': float(SELECTED_WAITING_ELEVATOR[1]),
        'angle': float(SELECTED_WAITING_ELEVATOR[2]),
        'pos_unit': POSITION_UNIT.PIXELS,
        'ang_unit': ANGLE_UNIT.RADIANS,
        **NAVIGATION_OPTIONS_WITH_CART
    },
    'elevator': {
        '1': {
            'localization': {
                'outside_elevator': {
                    'divisions': 3,
                    'closest_point': {
                        'x': float(elevator_1_max[0]),
                        'y': float(elevator_1_max[1]),
                        'angle': float(elevator_1_max[2]),
                        'pos_unit': POSITION_UNIT.PIXELS,
                        'ang_unit': ANGLE_UNIT.RADIANS,
                        **NAVIGATION_OPTIONS_WITH_CART
                    },
                    'farthest_point': {
                        'x': float(elevator_1_min[0]),
                        'y': float(elevator_1_min[1]),
                        'angle': float(elevator_1_min[2]),
                        'pos_unit': POSITION_UNIT.PIXELS,
                        'ang_unit': ANGLE_UNIT.RADIANS,
                        **NAVIGATION_OPTIONS_WITH_CART
                    },
                }
            }
        },
        '2': {
            'localization': {
                'outside_elevator': {
                    'divisions': 3,
                    'closest_point': {
                        'x': float(elevator_2_max[0]),
                        'y': float(elevator_2_max[1]),
                        'angle': float(elevator_2_max[2]),
                        'pos_unit': POSITION_UNIT.PIXELS,
                        'ang_unit': ANGLE_UNIT.RADIANS,
                        **NAVIGATION_OPTIONS_WITH_CART
                    },
                    'farthest_point': {
                        'x': float(elevator_2_min[0]),
                        'y': float(elevator_2_min[1]),
                        'angle': float(elevator_2_min[2]),
                        'pos_unit': POSITION_UNIT.PIXELS,
                        'ang_unit': ANGLE_UNIT.RADIANS,
                        **NAVIGATION_OPTIONS_WITH_CART
                    },
                }
            }
        },
        '3': {
            'localization': {
                'outside_elevator': {
                    'divisions': 3,
                    'closest_point': {
                        'x': float(elevator_3_max[0]),
                        'y': float(elevator_3_max[1]),
                        'angle': float(elevator_3_max[2]),
                        'pos_unit': POSITION_UNIT.PIXELS,
                        'ang_unit': ANGLE_UNIT.RADIANS,
                        **NAVIGATION_OPTIONS_WITH_CART
                    },
                    'farthest_point': {
                        'x': float(elevator_3_min[0]),
                        'y': float(elevator_3_min[1]),
                        'angle': float(elevator_3_min[2]),
                        'pos_unit': POSITION_UNIT.PIXELS,
                        'ang_unit': ANGLE_UNIT.RADIANS,
                        **NAVIGATION_OPTIONS_WITH_CART
                    },
                }
            }
        },
    },
    'units': {
        'unit1' : '7E',
        'unit2' : '7W'
    },
}

FLOOR_07_ROUTES = {
    'elev_unit1': [
        {
            'name': 'Navigation to unit1',
            'type': 'nav_to_point',
            'points': [
                [803, 1589, -0.0],
                [1162, 1386, 1.5707963267948966],
                [1154, 915, 1.5487004759110516],
                unit_1
                ], ##CHECKED
            'nav_options': {
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            'teleoperator_if_fail': True,
        },
    ],
    'elev_unit2': [
        {
            'name': 'Navigation to unit2',
            'type': 'nav_to_point',
            'points': [
                [1031, 1581, 0.04345089539153084],
                unit_2
                ], ##CHECKED
            'nav_options': {
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            'teleoperator_if_fail': True,
        },
    ],
    
    'unit1_unit2': [
        {
            'name': 'Navigation to unit2',
            'type': 'nav_to_point',
            'points': [
                [1505, 658, -1.5111656136637273],
                [1386, 1219, 3.120319267565732],
                [1165, 1484, -1.5707963267948966],
                unit_2
                ], ##CHECKED
            'nav_options': {
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            'teleoperator_if_fail': True,
        },
    ],
    
    'unit1_elev': [
        {
            'name': 'Navigation to waiting elevator',
            'type': 'nav_to_point',
            'points': [
                [1509, 680, -1.5235342507942045],
                [1353, 1212, -3.0672617664221278],
                [984, 1571, -3.0356082956001935],
                SELECTED_WAITING_ELEVATOR
                ], ##CHECKED
            'nav_options': {
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            'teleoperator_if_fail': True,
        },
    ],
    'unit2_elev': [
        {
            'name': 'Navigation to waiting elevator',
            'type': 'nav_to_point',
            'points': [
                [1524, 1777, 1.5707963267948966],
                [1404, 1219, 3.1239474262986704],
                [991, 1581, 3.0656520173238984],
                SELECTED_WAITING_ELEVATOR
                ], ##CHECKED
            'nav_options': {
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            'teleoperator_if_fail': True,
        },
    ],
}