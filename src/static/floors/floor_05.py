from .constants import *

from raya.enumerations import POSITION_UNIT, ANGLE_UNIT

elevator_1_max = [384, 1689, 1.6762368348216912]
elevator_1_min = [388, 1733, 1.6757300052367001]
elevator_2_max = [247, 1699, 1.6742096945405425]
elevator_2_min = [251, 1745, 1.6753295322006552]
elevator_3_max = [120, 1709, 1.6776399015749166]
elevator_3_min = [126, 1755, 1.6883030633155542]
unit_1 = [1199, 524, 0.14196073504728196]
unit_2 = [1356, 2197, 0.11940024681964291]
wait_elevator_l = [594, 1681, -3.0491927318206917]
wait_elevator_r = [614, 1742, -3.0591033391988316]

ELEVATORS_ZONE_NAME = 'elevator_zone'

SELECTED_WAITING_ELEVATOR = wait_elevator_r

FLOOR_5_INFO = {
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
        'unit1' : '5E',
        'unit2' : '5W'
    },
}

FLOOR_05_ROUTES = {
    'elev_unit1': [
        {
            'name': 'Navigation to unit1',
            'type': 'nav_to_point',
            'points': [
                    [798, 1693, 0.033600794415993215],
                    [1146, 1441, 1.5978167759821613],
                    [1112, 967, 1.6217077082512161],
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
                    [833, 1704, 0.06079455587478892],
                    [1181, 1846, -1.4950792874545444],
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
                    [1425, 795, -1.4501726582147938],
                    [1349, 1276, -2.9658543569044262],
                    [1143, 1487, -1.5072456553694393],
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
                    [1433, 634, -1.5291537476963082],
                    [1456, 1001, -1.4341531643038095],
                    [1345, 1280, -2.984990776607778],
                    [1005, 1678, -3.07100306377092],                    
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
                    [1532, 1704, 1.6819245794930706],
                    [1357, 1257, -2.9829373914033916],
                    [963, 1670, -2.9832651527813634],                 
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