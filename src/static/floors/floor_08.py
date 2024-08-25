from .constants import *

from raya.enumerations import POSITION_UNIT, ANGLE_UNIT

elevator_1_max = [386, 1724, 1.7412574953071434]
elevator_1_min = [394, 1769, 1.7434466835096198]
elevator_2_max = [251, 1744, 1.7356976703348441]
elevator_2_min = [258, 1790, 1.7388816530056193]
elevator_3_max = [124, 1764, 1.7380196448684087]
elevator_3_min = [132, 1810, 1.739540979477121]
unit_1 = [1380, 2125, 0.21877036470607367]
unit_1_entrance = [975, 1709, 0.1535117858370453]
unit_1_exit = [1566, 1749, 1.7434466835096198]
unit_2 = [1093, 446, 0.1539887578222113]
wait_elevator_l = [629, 1769, -2.997770086985672]
wait_elevator_r = [591, 1703, -2.9689923334600166]

UNIT_1_ZONE_NAME = 'unit1'
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


FLOOR_8_FLOOR = {
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
        'unit1' : '8W',
        'unit2' : '8E'
    },
}

FLOOR_08_ROUTES = {
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
            'teleoperator_if_fail': True,
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
            **UNIT_1_DOOR_OPTIONS
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
            'teleoperator_if_fail': True,
        },
    ],
    'elev_unit2': [
        {
            'name': 'Navigation to unit2',
            'type': 'nav_to_point',
            'points': [
                    [977, 1677, 0.11942892601833845],
                    [1119, 1352, 1.7214322350920823],
                    [1040, 898, 1.788350445928905],
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
            'teleoperator_if_fail': True,
        },
        {
            'name': 'Door unit1 exit',
            'type': 'automatic_door',
            'after_door_point': {
                'x': float(unit_2[0]),
                'y': float(unit_2[1]),
                'angle': float(unit_2[2]),
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            **UNIT_1_DOOR_TAGS['exit'],
            **UNIT_1_DOOR_OPTIONS
        },
        {
            'name': 'Navigation to unit2',
            'type': 'nav_to_point',
            'points': [
                    [1539, 1722, 1.7277231956406733],
                    [1302, 1260, -2.9186924212614174],
                    [1044, 940, 1.7252174463907024],
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
            'teleoperator_if_fail': True,
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
            **UNIT_1_DOOR_OPTIONS
        },
        {
            'name': 'Navigation to waiting elevator',
            'type': 'nav_to_point',
            'points': [
                    [1539, 1710, 1.7311717707708474],
                    [1273, 1260, -2.9219785284131934],
                    [977, 1660, -2.9501671720644502],
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
                    [1360, 715, -1.3530645877693281],
                    [1310, 1248, -2.961096893127758],
                    [977, 1664, -2.945204142744898],
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
