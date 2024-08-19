from .constants import *

from raya.enumerations import POSITION_UNIT, ANGLE_UNIT

elevator_1_max = [3364, 513, 1.8016715566010912]
elevator_1_min = [3376, 565, 1.7998981911927987]
elevator_2_max = [3230, 539, 1.810375662278539]
elevator_2_min = [3242, 593, 1.8100282560620327]
elevator_3_max = [3105, 568, 1.8079203614959949]
elevator_3_min = [3114, 618, 1.8034004002899453]
home_A = [343, 1371, -2.960683543029332]
home_B = [354, 1417, -2.9408081170309224]
parking_A = [289, 1271, 1.7904618881618362]
parking_B = [323, 1256, 2.1685452268524346]
wait_elevator = [2833, 706, 0.2177464694155388]
warehouse_entrance = [2010, 879, -2.9266371161831866]
warehouse_exit = [1761, 904, 0.22435328773765226]
warehouse_exit_c = [1748, 895, 0.26536295227317463]
cart_unload_point = [605, 1141, -2.922]

WAREHOUSE_ZONE_NAME = 'warehouse'

Home_Elev = [
    [
        # [654, 1123, 0.19739555984988075],
        # [1362, 978, 0.23501221572065709],
        warehouse_exit
    ],
    [
        # [2215, 805, 0.2055846397552597],
        # [2524, 742, 0.2299044281319047],
        wait_elevator
    ]
]

Elev_Home = [
    [
        [2794, 686, -2.9345199764727616],
        [2505, 742, -2.905568974963896],
        warehouse_entrance
    ],
    [
        [1674, 900, -2.916315874375738],
        [919, 1063, -2.93121081081974],
        cart_unload_point
    ]
]


NAV_CART_LOAD_POINT_OPTIONS = {
    'pos_unit': POSITION_UNIT.PIXELS, 
    'ang_unit': ANGLE_UNIT.RADIANS,
    **NAVIGATION_OPTIONS_WITHOUT_CART
}

NAV_CART_OPTIONS = {
    'pos_unit': POSITION_UNIT.PIXELS, 
    'ang_unit': ANGLE_UNIT.RADIANS,
    **NAVIGATION_OPTIONS_WITH_CART
}

FLOOR__00 = {
    'waiting_elevator': {
        'x': float(wait_elevator[0]),
        'y': float(wait_elevator[1]),
        'angle': float(wait_elevator[2]),
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
    }
}

WAREHOUSE_DOOR = {
    'tags_ids': [25],
    'tags_sizes': [0.12],
    'phone_call_user_id': '[CSR_USER_ID]'
}

BASEMENT_ROUTES = {
    'go_to_elevators_after_attach': [
        {
            'name': 'Navigation to warehouse exit',
            'type': 'nav_to_point',
            'points': Home_Elev[0],
            'teleoperator_if_fail': True,
            'nav_options': NAV_CART_OPTIONS
        },
        {
            'name': 'Manual door warehouse',
            'type': 'manual_door',
            'zone_name': WAREHOUSE_ZONE_NAME,
            'after_door_point': {
                'x': float(Home_Elev[1][0][0]),
                'y': float(Home_Elev[1][0][1]),
                'angle': float(Home_Elev[1][0][2]),
                **NAV_CART_OPTIONS
            },
            **WAREHOUSE_DOOR
        },
        {
            'name': 'Navigation to waiting elevator',
            'type': 'nav_to_point',
            'points': Home_Elev[1],
            'teleoperator_if_fail': True,
            'nav_options': NAV_CART_OPTIONS
        },
    ],
    'go_to_detach_point': [
        {
            'name': 'Navigation to warehouse entrance',
            'type': 'nav_to_point',
            'points': Elev_Home[0],
            'teleoperator_if_fail': True,
            'nav_options': NAV_CART_OPTIONS
        },
        {
            'name': 'Manual door warehouse',
            'type': 'manual_door',
            'zone_name': WAREHOUSE_ZONE_NAME,
            'after_door_point': {
                'x': float(Elev_Home[1][0][0]),
                'y': float(Elev_Home[1][0][1]),
                'angle': float(Elev_Home[1][0][2]),
                **NAV_CART_OPTIONS
            },
            **WAREHOUSE_DOOR
        },
        {
            'name': 'Navigation to detaching point',
            'type': 'nav_to_point',
            'points': Elev_Home[1],
            'teleoperator_if_fail': True,
            'nav_options': NAV_CART_OPTIONS
        }
    ],
    
    'go_to_home': [
        {
            'name': 'Navigation to home',
            'type': 'nav_to_point',
            'point' : {}, # it uses the home position from the map
            'teleoperator_if_fail': True,
        },
    ],
    'go_to_parking_cart_point': [
        {
            'name': 'Navigation to cart point',
            'type': 'nav_to_point',
            'point' : {}, # it uses the cart position from the parameter of the app
            'teleoperator_if_fail': True,
        },
    ]  
}
