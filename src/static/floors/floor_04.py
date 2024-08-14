from .constants import *

from raya.enumerations import POSITION_UNIT, ANGLE_UNIT

elevator_1_max = [571, 1605, 1.53673564194864]
elevator_1_min = [570, 1654, 1.54432953875892]
elevator_2_max = [432, 1591, 1.5627812375203876]
elevator_2_mi = [431, 1648, 1.5582898456773373]
elevator_2_min = [431, 1648, 1.5578435379679467]
elevator_3_max = [305, 1589, 1.538400902247487]
elevator_3_min = [305, 1644, 1.5460022054648714]
unit_1 = [1394, 1704, -3.1159257403094367]
unit_2 = [1518, 496, -0.034326290763845885]
unit_3_entrance = [1824, 2100, -1.5685361217325895]
unit_3 = [1805, 2727, -1.5685361217325895]
unit_3_exit = [1018, 2326, 1.5685361217325895]
wait_elevator_l = [780, 1694, 3.1159257403094367]
wait_elevator_r = [744, 1632, 3.089958415405998]

UNIT1_ZONE_NAME = 'unit1'
UNIT2_ZONE_NAME = 'unit2'
UNIT3_ZONE_NAME = 'unit3'
ELEVATORS_ZONE_NAME = 'elevator_zone'

SELECTED_WAITING_ELEVATOR = wait_elevator_l

FLOOR__04 = {
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
        'unit1' : '4BURN',
        'unit2' : '4E',
        'unit3' : '4W'
    },
}

FLOOR_04_ROUTES = {
    'elev_unit1': [
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
            'point' : {
                'x': float(unit_2[0]),
                'y': float(unit_2[1]),
                'angle': float(unit_2[2]),
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            'teleoperator_if_fail': True,
        },
    ],
    'elev_unit3': [
        {
            'name': 'Navigation to unit3 entrance',
            'type': 'nav_to_point',
            'point' : {
                'x': float(unit_3_entrance[0]),
                'y': float(unit_3_entrance[1]),
                'angle': float(unit_3_entrance[2]),
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            'teleoperator_if_fail': True,
        },
        {
            'name': 'Automatic door unit3 entrance',
            'type': 'automatic_door',
            'zone_name': UNIT3_ZONE_NAME,
            'after_door_point': {
                'x': float(unit_3[0]),
                'y': float(unit_3[1]),
                'angle': float(unit_3[2]),
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            'tags_ids': [25],
            'tags_sizes': [0.12],
        },
        {
            'name': 'Navigation to unit3',
            'type': 'nav_to_point',
            'point' : {
                'x': float(unit_3[0]),
                'y': float(unit_3[1]),
                'angle': float(unit_3[2]),
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
            'point' : {
                'x': float(unit_2[0]),
                'y': float(unit_2[1]),
                'angle': float(unit_2[2]),
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            'teleoperator_if_fail': True,
        },
    ],
    'unit1_unit3': [
        {
            'name': 'Navigation to unit3 entrance',
            'type': 'nav_to_point',
            'point' : {
                'x': float(unit_3_entrance[0]),
                'y': float(unit_3_entrance[1]),
                'angle': float(unit_3_entrance[2]),
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            'teleoperator_if_fail': True,
        },
        {
            'name': 'Automatic door unit3 entrance',
            'type': 'automatic_door',
            'zone_name': UNIT3_ZONE_NAME,
            'after_door_point': {
                'x': float(unit_3[0]),
                'y': float(unit_3[1]),
                'angle': float(unit_3[2]),
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            'tags_ids': [25],
            'tags_sizes': [0.12],
        },
        {
            'name': 'Navigation to unit3',
            'type': 'nav_to_point',
            'point' : {
                'x': float(unit_3[0]),
                'y': float(unit_3[1]),
                'angle': float(unit_3[2]),
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            'teleoperator_if_fail': True,
        },
    ],
    
    'unit2_unit3': [
        {
            'name': 'Navigation to unit3 entrance',
            'type': 'nav_to_point',
            'point' : {
                'x': float(unit_3_entrance[0]),
                'y': float(unit_3_entrance[1]),
                'angle': float(unit_3_entrance[2]),
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            'teleoperator_if_fail': True,
        },
        {
            'name': 'Automatic door unit3 entrance',
            'type': 'automatic_door',
            'zone_name': UNIT3_ZONE_NAME,
            'after_door_point': {
                'x': float(unit_3[0]),
                'y': float(unit_3[1]),
                'angle': float(unit_3[2]),
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            'tags_ids': [25],
            'tags_sizes': [0.12],
        },
        {
            'name': 'Navigation to unit3',
            'type': 'nav_to_point',
            'point' : {
                'x': float(unit_3[0]),
                'y': float(unit_3[1]),
                'angle': float(unit_3[2]),
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            'teleoperator_if_fail': True,
        },],
    
    'unit1_elev': [
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
            'teleoperator_if_fail': True,
        },
    ],
    'unit2_elev': [
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
            'teleoperator_if_fail': True,
        },
    ],
    'unit3_elev': [
        {
            'name': 'Teleoperation to leave the unit',
            'type': 'teleoperation',
        },
        {
            'name': 'Navigation to unit3 exit',
            'type': 'nav_to_point',
            'point' : {
                'x': float(unit_3_exit[0]),
                'y': float(unit_3_exit[1]),
                'angle': float(unit_3_exit[2]),
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            'teleoperator_if_fail': True,
        },
        {
            'name': 'Automatic door unit3 entrance',
            'type': 'automatic_door',
            'zone_name': UNIT3_ZONE_NAME,
            'after_door_point': {
                'x': float(SELECTED_WAITING_ELEVATOR[0]),
                'y': float(SELECTED_WAITING_ELEVATOR[0]),
                'angle': float(SELECTED_WAITING_ELEVATOR[0]),
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            'tags_ids': [25],
            'tags_sizes': [0.12],
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
            'teleoperator_if_fail': True,
        },
    ],
}
