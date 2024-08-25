from .constants import *

from raya.enumerations import POSITION_UNIT, ANGLE_UNIT

elevator_1_max = [1503, 1650, 3.039086082060112]
elevator_1_min = [1548, 1655, 3.0434133891621333]
elevator_2_max = [1488, 1786, 3.0292446483202538]
elevator_2_min = [1534, 1791, 3.0282907445522356]
elevator_3_max = [1473, 1912, 3.011320817163363]
elevator_3_min = [1518, 1918, 3.008351497760936]
unit_1 = [479, 641, 1.4648119688052967]
unit_1_entrance = [1143, 784, 3.062089912421014]
unit_1_exit = [899, 823, -0.050289970665515694]
unit_2= [1895, 282, 1.4751746773080279]
unit_2_entrance= [1633, 669, -0.11852358247207816]
unit_2_exit= [1813, 488, -1.6529619614275535]
unit_3= [2020, 1022, -1.7124606234721582]
unit_3_entrance= [1880, 754, -0.1102226340696748]
unit_4= [3421, 1185, -1.6408263150621547]
unit_4_entrance= [3156, 909, -0.0853688682740938]
unit_4_exit= [3376, 877, 3.0305143762068605]
wait_elevator_l= [1632, 1399, -1.7295066315196583]
wait_elevator_r= [1542, 1457, -1.6905473579494434]
wait_manual_door= [1227, 1119, 1.4647285698774566]

UNIT_1_ZONE_NAME = 'unit1'
UNIT_2_ZONE_NAME = 'unit2'
UNIT_3_ZONE_NAME = 'unit3'
UNIT_4_ZONE_NAME = 'unit4'
ELEVATORS_ZONE_NAME = 'elevator_zone'

SELECTED_WAITING_ELEVATOR = wait_elevator_l

FLOOR_2_INFO = {
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
        'unit1' : 'CICU',
        'unit2' : 'MRICU HIGH',
        'unit3' : 'MICU',
        'unit4' : 'MRICU ELBOW',
    },
}

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

UNIT_3_DOOR_TAGS = {
    'entrance' : {
        'tags_ids': [203],
        'tags_sizes': [0.10],
    },
    'exit' : {
        'tags_ids': [204],
        'tags_sizes': [0.10],
    },
}
UNIT_3_DOOR_OPTIONS = {
    'zone_name': UNIT_3_ZONE_NAME,
    'phone_call_user_id': '[unit3_user_id]',
}

UNIT_4_DOOR_TAGS = {
    'entrance' : {
        'tags_ids': [201],
        'tags_sizes': [0.10],
    },
    'exit' : {
        'tags_ids': [202],
        'tags_sizes': [0.10],
    },
}
UNIT_4_DOOR_OPTIONS = {
    'zone_name': UNIT_4_ZONE_NAME,
    'phone_call_user_id': '[unit4_user_id]',
}


FLOOR_02_ROUTES = {
    'elev_unit1': [
        {
            'name': 'Navigation to entrance unit1',
            'type': 'nav_to_point',
            'points': [
                    [1617, 1056, 1.4371440794777028],
                    [1523, 689, 3.038067979079249],
                    unit_1_entrance
                ], ##CHECKED
            'nav_options': {
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
            **UNIT_1_DOOR_OPTIONS,
            **UNIT_1_DOOR_TAGS['entrance']
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
            **UNIT_2_DOOR_OPTIONS,
            **UNIT_2_DOOR_TAGS['entrance']
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
            'teleoperator_if_fail': False,
        },
        {
            'name': 'Door unit3 entrance',
            'type': 'automatic_door',
            'after_door_point': {
                'x': float(unit_3[0]),
                'y': float(unit_3[1]),
                'angle': float(unit_3[2]),
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            **UNIT_3_DOOR_OPTIONS,
            **UNIT_3_DOOR_TAGS['entrance']
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
            'teleoperator_if_fail': False,
        },
    ],
    'elev_unit4': [
        {
            'name': 'Navigation to unit4 entrance',
            'type': 'nav_to_point',
            'points': [
                    [1607, 1133, 1.4020462243745955],
                    [1961, 731, -0.12090276430269138],
                    [2593, 811, -0.1145406967966813],
                    unit_4_entrance
                ], ##CHECKED
            'nav_options': {
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            'teleoperator_if_fail': False,
        },
        {
            'name': 'Door unit4 entrance',
            'type': 'automatic_door',
            'after_door_point': {
                'x': float(unit_4[0]),
                'y': float(unit_4[1]),
                'angle': float(unit_4[2]),
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            **UNIT_4_DOOR_OPTIONS,
            **UNIT_4_DOOR_TAGS['entrance']
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
            **UNIT_1_DOOR_OPTIONS,
            **UNIT_1_DOOR_TAGS['exit']
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
                'angle': float(unit_2[2]),
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            **UNIT_2_DOOR_OPTIONS,
            **UNIT_2_DOOR_TAGS['entrance']
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
    'unit1_unit3': [
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
                'x': float(unit_3_entrance[0]),
                'y': float(unit_3_entrance[1]),
                'angle': float(unit_3_entrance[2]),
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            **UNIT_1_DOOR_OPTIONS,
            **UNIT_1_DOOR_TAGS['exit']
        },
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
            'teleoperator_if_fail': False,
        },
        {
            'name': 'Door unit3 entrance',
            'type': 'automatic_door',
            'after_door_point': {
                'x': float(unit_3[0]),
                'y': float(unit_3[1]),
                'angle': float(unit_3[2]),
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            **UNIT_3_DOOR_OPTIONS,
            **UNIT_3_DOOR_TAGS['entrance']
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
            'teleoperator_if_fail': False,
        },
        ],
    'unit1_unit4': [
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
            'teleoperator_if_fail': True,
        },
        {
            'name': 'Door unit1 exit',
            'type': 'automatic_door',
            'after_door_point': {
                'x': float(1465), ### FIRST PARTIAL POINT
                'y': float(679),
                'angle': float(-0.13722730869487104),
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            **UNIT_1_DOOR_OPTIONS,
            **UNIT_1_DOOR_TAGS['exit']
        },
        {
            'name': 'Navigation to unit4 entrance',
            'type': 'nav_to_point',
            'points': [
                    [1465, 679, -0.13722730869487104],
                    [2203, 769, -0.10520024942055292],
                    [2838,  840, -0.1409040062712096],
                    unit_4_entrance
                ], ##CHECKED
            'nav_options': {
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            'teleoperator_if_fail': False,
        },
        {
            'name': 'Door unit4 entrance',
            'type': 'automatic_door',
            'after_door_point': {
                'x': float(unit_4[0]),
                'y': float(unit_4[1]),
                'angle': float(unit_4[2]),
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            **UNIT_4_DOOR_OPTIONS,
            **UNIT_4_DOOR_TAGS['entrance']
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
            'teleoperator_if_fail': False,
        },
    ],
    
    'unit2_unit3': [
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
                'x': float(unit_3_entrance[0]),
                'y': float(unit_3_entrance[1]),
                'angle': float(unit_3_entrance[2]),
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            **UNIT_2_DOOR_OPTIONS,
            **UNIT_2_DOOR_TAGS['exit']
        },
        {
            'name': 'Door unit3 entrance',
            'type': 'automatic_door',
            'after_door_point': {
                'x': float(unit_3[0]),
                'y': float(unit_3[1]),
                'angle': float(unit_3[2]),
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            **UNIT_3_DOOR_OPTIONS,
            **UNIT_3_DOOR_TAGS['entrance']
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
            'teleoperator_if_fail': False,
        },
    ],
    'unit2_unit4': [
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
                'x': float(unit_4_entrance[0]),
                'y': float(unit_4_entrance[1]),
                'angle': float(unit_4_entrance[2]),
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            **UNIT_2_DOOR_OPTIONS,
            **UNIT_2_DOOR_TAGS['exit']
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
            'teleoperator_if_fail': False,
        },
        {
            'name': 'Door unit4 entrance',
            'type': 'automatic_door',
            'after_door_point': {
                'x': float(unit_4[0]),
                'y': float(unit_4[1]),
                'angle': float(unit_4[2]),
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            **UNIT_4_DOOR_OPTIONS,
            **UNIT_4_DOOR_TAGS['entrance']
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
            'teleoperator_if_fail': False,
        },
    ],
    
    'unit3_unit4': [
        {
            'name': 'Teleoperation to leave the unit',
            'type': 'teleoperation',
        },
        {
            'name': 'Door unit3 exit',
            'type': 'automatic_door',
            'after_door_point': {
                'x': float(unit_4_entrance[0]),
                'y': float(unit_4_entrance[1]),
                'angle': float(unit_4_entrance[2]),
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            **UNIT_3_DOOR_OPTIONS,
            **UNIT_3_DOOR_TAGS['exit']
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
            'teleoperator_if_fail': False,
        },
        {
            'name': 'Door unit4 entrance',
            'type': 'automatic_door',
            'after_door_point': {
                'x': float(unit_4[0]),
                'y': float(unit_4[1]),
                'angle': float(unit_4[2]),
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            **UNIT_4_DOOR_OPTIONS,
            **UNIT_4_DOOR_TAGS['entrance']
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
            'teleoperator_if_fail': False,
        },
    ],
    
    'unit1_elev':  [
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
                'x': float(1462), ## FIRST PARTIAL POINT
                'y': float(689),
                'angle': float(-0.12630811706324024),
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            **UNIT_1_DOOR_OPTIONS,
            **UNIT_1_DOOR_TAGS['exit']
        },
        {
            'name': 'Navigation to waiting elevator',
            'type': 'nav_to_point',
            'points': [
                    [1462, 689, -0.12630811706324024],
                    [1633, 998, -1.7078625011050843],
                    SELECTED_WAITING_ELEVATOR
                ], ##CHECKED
            'nav_options': {
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            'teleoperator_if_fail': False,
        },
    ],
    'unit2_elev':  [
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
            **UNIT_2_DOOR_OPTIONS,
            **UNIT_2_DOOR_TAGS['exit']
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
    'unit3_elev':  [
        {
            'name': 'Teleoperation to leave the unit',
            'type': 'teleoperation',
        },
        {
            'name': 'Door unit3 exit',
            'type': 'automatic_door',
            'after_door_point': {
                'x': float(SELECTED_WAITING_ELEVATOR[0]),
                'y': float(SELECTED_WAITING_ELEVATOR[1]),
                'angle': float(SELECTED_WAITING_ELEVATOR[2]),
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            **UNIT_3_DOOR_OPTIONS,
            **UNIT_3_DOOR_TAGS['exit']
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
    'unit4_elev': [
        {
            'name': 'Teleoperation to leave the unit',
            'type': 'teleoperation',
        },
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
            'teleoperator_if_fail': False,
        },
        {
            'name': 'Door unit4 exit',
            'type': 'automatic_door',
            'after_door_point': {
                'x': float(2818),### FIRST PARTIAL POINT
                'y': float(844),
                'angle': float(3.0639711448524),
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            **UNIT_4_DOOR_OPTIONS,
            **UNIT_4_DOOR_TAGS['exit']
        },
        {
            'name': 'Navigation to waiting elevator',
            'type': 'nav_to_point',
            'points': [
                    [2818, 844, 3.0639711448524],
                    [2139, 763, 3.015625623899914],
                    [1626, 959,-1.6853370235915779],                
                    SELECTED_WAITING_ELEVATOR
                ], ##CHECKED
            'nav_options': {
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
            },
            'teleoperator_if_fail': False,
        },
    ],

}
