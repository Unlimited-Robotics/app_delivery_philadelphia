from .constants import *

from raya.enumerations import POSITION_UNIT, ANGLE_UNIT

elevator_1_max = [1503, 1650, 3.039086082060112]
elevator_1_min = [1548, 1655, 3.0434133891621333]
elevator_2_max = [1488, 1786, 3.0292446483202538]
elevator_2_min = [1534, 1791, 3.0282907445522356]
elevator_3_max = [1473, 1912, 3.011320817163363]
elevator_3_min = [1518, 1918, 3.008351497760936]
unit_1 = [519, 573, 1.4647285698774566]
unit_1_entrance = [1143, 784, 3.062089912421014]
unit_1_exit = [899, 823, -0.050289970665515694]
unit_2= [1895, 282, 1.4751746773080279]
unit_2_entrance= [1633, 669, -0.11852358247207816]
unit_2_exit= [1813, 488, -1.6529619614275535]
unit_3= [2020, 1022, -1.7124606234721582]
unit_3_entrance= [1880, 754, -0.1102226340696748]
unit_4= [3510, 1208, -1.6587789329529365]
unit_4_entrance= [3156, 909, -0.0853688682740938]
unit_4_exit= [3376, 877, 3.0305143762068605]
wait_elevator_l= [1632, 1399, -1.7295066315196583]
wait_elevator_r= [1542, 1457, -1.6905473579494434]
wait_manual_door= [1227, 1119, 1.4647285698774566]

FLOOR__02 = {
    'max_elevators': 3,
    'waiting_elevator': {
        'x': wait_elevator_l[0],
        'y': wait_elevator_l[1],
        'angle': wait_elevator_l[2],
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
                    },
                    'farthest_point': {
                        'x': float(elevator_1_min[0]),
                        'y': float(elevator_1_min[1]),
                        'angle': float(elevator_1_min[2]),
                        'pos_unit': POSITION_UNIT.PIXELS,
                        'ang_unit': ANGLE_UNIT.RADIANS,
                    },
                }
            },
            'entry_point': {
                'x': 393.0,
                'y': 2000.0,
                'angle': 1.8395248997063303,
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
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
                    },
                    'farthest_point': {
                        'x': float(elevator_2_min[0]),
                        'y': float(elevator_2_min[1]),
                        'angle': float(elevator_2_min[2]),
                        'pos_unit': POSITION_UNIT.PIXELS,
                        'ang_unit': ANGLE_UNIT.RADIANS,
                    },
                }
            },
            'entry_point': {
                'x': 262.0,
                'y': 2041.0,
                'angle': 1.8389119201724646,
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
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
                    },
                    'farthest_point': {
                        'x': float(elevator_3_min[0]),
                        'y': float(elevator_3_min[1]),
                        'angle': float(elevator_3_min[2]),
                        'pos_unit': POSITION_UNIT.PIXELS,
                        'ang_unit': ANGLE_UNIT.RADIANS,
                    },
                }
            },
            'entry_point': {
                'x': 134.0,
                'y': 2074.0,
                'angle': 1.8396149613713695,
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
        },
    },
    'units': {
        'unit1' : 'unit1',
        'unit2' : 'unit2',
        'unit3' : 'unit3',
        'unit4' : 'unit4',
    },
}

FLOOR_02_ROUTES = {
    'elev_unit1': [
        {
            'name': 'Automatic door unit1 entrance',
            'type': 'automatic_door',
            'after_door_point': {
                'x': float(unit_1_entrance[0]),
                'y': float(unit_1_entrance[1]),
                'angle': float(unit_1_entrance[2]),
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            'tags_ids': [25],
            'tags_sizes': [0.12],
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
            'name': 'Automatic door unit1 exit',
            'type': 'automatic_door',
            'after_door_point': {
                'x': float(unit_2_entrance[0]),
                'y': float(unit_2_entrance[1]),
                'angle': float(unit_2_entrance[2]),
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            'tags_ids': [25],
            'tags_sizes': [0.12],
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
            'teleoperator_if_fail': True,
        },
        {
            'name': 'Automatic door unit2 entrance',
            'type': 'automatic_door',
            'after_door_point': {
                'x': float(unit_2[0]),
                'y': float(unit_2[1]),
                'angle': float(unit_2[2]),
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            'tags_ids': [25],
            'tags_sizes': [0.12],
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
            'teleoperator_if_fail': True,
        },
    ],
    
    'unit2_unit3': [
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
            'teleoperator_if_fail': True,
        },
        {
            'name': 'Automatic door unit2 exit',
            'type': 'automatic_door',
            'after_door_point': {
                'x': float(unit_3_entrance[0]),
                'y': float(unit_3_entrance[1]),
                'angle': float(unit_3_entrance[2]),
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            'tags_ids': [25],
            'tags_sizes': [0.12],
        },
        {
            'name': 'Automatic door unit3 entrance',
            'type': 'automatic_door',
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
    
    'unit3_unit4': [
        {
            'name': 'Automatic door unit3 exit',
            'type': 'automatic_door',
            'after_door_point': {
                'x': float(unit_4_entrance[0]),
                'y': float(unit_4_entrance[1]),
                'angle': float(unit_4_entrance[2]),
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            'tags_ids': [25],
            'tags_sizes': [0.12],
        },
        {
            'name': 'Navigation to unit4 entrance',
            'type': 'nav_to_point',
            'point' : {
                'x': float(unit_4_entrance[0]),
                'y': float(unit_4_entrance[1]),
                'angle': float(unit_4_entrance[2]),
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            'teleoperator_if_fail': True,
        },
        {
            'name': 'Automatic door unit4 entrance',
            'type': 'automatic_door',
            'after_door_point': {
                'x': float(unit_4[0]),
                'y': float(unit_4[1]),
                'angle': float(unit_4[2]),
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            'tags_ids': [25],
            'tags_sizes': [0.12],
        },
        {
            'name': 'Navigation to unit4',
            'type': 'nav_to_point',
            'point' : {
                'x': float(unit_4[0]),
                'y': float(unit_4[1]),
                'angle': float(unit_4[2]),
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            'teleoperator_if_fail': True,
        },
    ],
    
    'unit4_elev': [
        {
            'name': 'Navigation to unit4 exit',
            'type': 'nav_to_point',
            'point' : {
                'x': float(unit_4_exit[0]),
                'y': float(unit_4_exit[1]),
                'angle': float(unit_4_exit[2]),
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            'teleoperator_if_fail': True,
        },
        {
            'name': 'Automatic door unit4 exit',
            'type': 'automatic_door',
            'after_door_point': {
                'x': float(wait_elevator_l[0]),
                'y': float(wait_elevator_l[1]),
                'angle': float(wait_elevator_l[2]),
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
                'x': float(wait_elevator_l[0]),
                'y': float(wait_elevator_l[1]),
                'angle': float(wait_elevator_l[2]),
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            'teleoperator_if_fail': True,
        },
    ],

}
