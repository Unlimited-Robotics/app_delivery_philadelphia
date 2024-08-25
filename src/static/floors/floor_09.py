from .constants import *

from raya.enumerations import POSITION_UNIT, ANGLE_UNIT

elevator_1_max = [1424, 1554, 2.990714278230129]
elevator_1_min = [1467, 1556, 3.0082520300551625]
elevator_2_max = [1405, 1688, 3.0153722516842056]
elevator_2_min = [1449, 1694, 3.02441123374449]
elevator_3_max = [1384, 1812, 3.0182877231347853]
elevator_3_min = [1430, 1818, 3.013329959818549]
unit_1 = [486, 341, 1.420437911472327]
unit_1_entrance = [1114, 684, 3.0333829779761854]
unit_1_exit = [839, 707, -0.13392507686663685]
unit_2 = [2197, 826, -0.12503157755467742]
unit_2_entrance = [1719, 829, -0.13937460882026623]
unit_2_exit = [2001, 794, 3.0356756681280825]
wait_elevator_l = [1536, 1339, -1.6955799421014288]
wait_elevator_r = [1467, 1348, -1.729934305321282]

UNIT_1_ZONE_NAME = 'unit1'
UNIT_2_ZONE_NAME = 'unit2'
ELEVATORS_ZONE_NAME = 'elevator_zone'

SELECTED_WAITING_ELEVATOR = wait_elevator_l


UNIT_1_DOOR_TAGS = {
    'entrance' : {
        'tags_ids': [201],
        'tags_sizes': [0.10],
    },
    'exit' : {
        'tags_ids': [202],
        'tags_sizes': [0.10],
    },
}
UNIT_1_DOOR_OPTIONS = {
    'zone_name': UNIT_1_ZONE_NAME,
    'phone_call_user_id': '[unit1_user_id]',
}

UNIT_2_DOOR_TAGS = {
    'entrance' : {
        'tags_ids': [201],
        'tags_sizes': [0.10],
    },
    'exit' : {
        'tags_ids': [202],
        'tags_sizes': [0.10],
    },
}
UNIT_2_DOOR_OPTIONS = {
    'zone_name': UNIT_2_ZONE_NAME,
    'phone_call_user_id': '[unit2_user_id]',
}


FLOOR_9_FLOOR = {
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
        'unit1' : '9E',
        'unit2' : '9W'
    },
}

FLOOR_09_ROUTES = {
    'elev_unit1': [
        {
            'name': 'Navigation to unit1 entrance',
            'type': 'nav_to_point',
            'point' : {
                'x': float(unit_1_entrance[0]),
                'y': float(unit_1_entrance[1]),
                'angle': float(unit_1_entrance[2]),
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            'teleoperator_if_fail': False,
        },
        {
            'name': 'Door unit1 entrance',
            'type': 'automatic_door',
            'after_door_point': {
                'x': float(unit_1[0]),
                'y': float(unit_1[1]),
                'angle': float(unit_1[2]),
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            **UNIT_1_DOOR_TAGS['entrance'],
            **UNIT_1_DOOR_OPTIONS,
        },
        {
            'name': 'Navigation to unit1',
            'type': 'nav_to_point',
            'point' : {
                'x': float(unit_1[0]),
                'y': float(unit_1[1]),
                'angle': float(unit_1[2]),
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            'teleoperator_if_fail': False,
        },
    ],
    'elev_unit2': [
        {
            'name': 'Navigation to unit2 entrance',
            'type': 'nav_to_point',
            'point' : {
                'x': float(unit_2_entrance[0]),
                'y': float(unit_2_entrance[1]),
                'angle': float(unit_2_entrance[2]),
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            'teleoperator_if_fail': False,
        },
        {
            'name': 'Door unit2 entrance',
            'type': 'automatic_door',
            'after_door_point': {
                'x': float(unit_2[0]),
                'y': float(unit_2[1]),
                'angle': float(unit_2[2]),
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            **UNIT_2_DOOR_TAGS['entrance'],
            **UNIT_2_DOOR_OPTIONS,
        },
        {
            'name': 'Navigation to unit2',
            'type': 'nav_to_point',
            'point' : {
                'x': float(unit_2[0]),
                'y': float(unit_2[1]),
                'angle': float(unit_2[2]),
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            'teleoperator_if_fail': False,
        },
    ],
    
    'unit1_unit2': [
        {
            'name': 'Teleoperation to leave the unit',
            'type': 'teleoperation',
        },
        {
            'name': 'Navigation to unit1 exit',
            'type': 'nav_to_point',
            'point' : {
                'x': float(unit_1_exit[0]),
                'y': float(unit_1_exit[1]),
                'angle': float(unit_1_exit[2]),
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            'teleoperator_if_fail': False,
        },
        {
            'name': 'Door unit1 exit',
            'type': 'automatic_door',
            'after_door_point': {
                'x': float(unit_2_entrance[0]),
                'y': float(unit_2_entrance[1]),
                'angle': float(unit_2_entrance[2]),
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            **UNIT_1_DOOR_TAGS['exit'],
            **UNIT_1_DOOR_OPTIONS,
        },
        {
            'name': 'Navigation to unit2 entrance',
            'type': 'nav_to_point',
            'point' : {
                'x': float(unit_2_entrance[0]),
                'y': float(unit_2_entrance[1]),
                'angle': float(unit_2_entrance[2]),
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            'teleoperator_if_fail': False,
        },
        {
            'name': 'Door unit2 entrance',
            'type': 'automatic_door',
            'after_door_point': {
                'x': float(unit_2[0]),
                'y': float(unit_2[1]),
                'angle': float(unit_2_entrance[2]),
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            **UNIT_2_DOOR_TAGS['entrance'],
            **UNIT_2_DOOR_OPTIONS,
        },
        {
            'name': 'Navigation to unit2',
            'type': 'nav_to_point',
            'point' : {
                'x': float(unit_2[0]),
                'y': float(unit_2[1]),
                'angle': float(unit_2[2]),
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            'teleoperator_if_fail': False,
        },
    ],
    
    'unit1_elev': [
        {
            'name': 'Teleoperation to leave the unit',
            'type': 'teleoperation',
        },
        {
            'name': 'Navigation to unit1 exit',
            'type': 'nav_to_point',
            'point' : {
                'x': float(unit_1_exit[0]),
                'y': float(unit_1_entrance[1]),
                'angle': float(unit_1_entrance[2]),
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            'teleoperator_if_fail': False,
        },
        {
            'name': 'Door unit1 exit',
            'type': 'automatic_door',
            'after_door_point': {
                'x': float(SELECTED_WAITING_ELEVATOR[0]),
                'y': float(SELECTED_WAITING_ELEVATOR[1]),
                'angle': float(SELECTED_WAITING_ELEVATOR[2]),
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            **UNIT_1_DOOR_TAGS['exit'],
            **UNIT_1_DOOR_OPTIONS,
        },
        {
            'name': 'Navigation to waiting elevator',
            'type': 'nav_to_point',
            'point' : {
                'x': float(SELECTED_WAITING_ELEVATOR[0]),
                'y': float(SELECTED_WAITING_ELEVATOR[1]),
                'angle': float(SELECTED_WAITING_ELEVATOR[2]),
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            'teleoperator_if_fail': False,
        },
    ],
    'unit2_elev': [
        {
            'name': 'Teleoperation to leave the unit',
            'type': 'teleoperation',
        },
        {
            'name': 'Navigation to unit2 exit',
            'type': 'nav_to_point',
            'point' : {
                'x': float(unit_2_exit[0]),
                'y': float(unit_2_exit[1]),
                'angle': float(unit_2_exit[2]),
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            'teleoperator_if_fail': False,
        },
        {
            'name': 'Door unit2 exit',
            'type': 'automatic_door',
            'after_door_point': {
                'x': float(SELECTED_WAITING_ELEVATOR[0]),
                'y': float(SELECTED_WAITING_ELEVATOR[1]),
                'angle': float(SELECTED_WAITING_ELEVATOR[2]),
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            **UNIT_2_DOOR_TAGS['exit'],
            **UNIT_2_DOOR_OPTIONS,
        },
        {
            'name': 'Navigation to waiting elevator',
            'type': 'nav_to_point',
            'point' : {
                'x': float(SELECTED_WAITING_ELEVATOR[0]),
                'y': float(SELECTED_WAITING_ELEVATOR[1]),
                'angle': float(SELECTED_WAITING_ELEVATOR[2]),
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            'teleoperator_if_fail': False,
        },
    ],
}
