from .constants import *

from raya.enumerations import POSITION_UNIT, ANGLE_UNIT

elevator_1_max = [3364, 513, 1.8016715566010912]
elevator_1_min = [3376, 565, 1.7998981911927987]
elevator_2_max = [3230, 539, 1.810375662278539]
elevator_2_min = [3242, 593, 1.8100282560620327]
elevator_3_max = [3105, 568, 1.8079203614959949]
elevator_3_min = [3114, 618, 1.8034004002899453]
home_1 = [343, 1371, -2.960683543029332]
home_2 = [354, 1417, -2.9408081170309224]
nav_to_cart_point = [289, 1271, 1.7904618881618362]
nav_to_cart_point_2 = [323, 1256, 2.1685452268524346]
wait_elevator = [2833, 706, 0.2177464694155388]
warehouse_entrance = [2010, 879, -2.9266371161831866]
warehouse_exit = [1761, 904, 0.22435328773765226]
warehouse_exit_c = [1748, 895, 0.26536295227317463]
cart_unload_point = [605, 1141, -2.922]

WAREHOUSE_ZONE_NAME = 'warehouse'

NAV_CART_LOAD_POINT_OPTIONS = {
    'pos_unit': POSITION_UNIT.PIXELS, 
    'ang_unit': ANGLE_UNIT.DEGREES,
    **NAVIGATION_OPTIONS_WITHOUT_CART
}

NAV_WAREHOUSE_ENTRANCE = {
        'x':        float(warehouse_entrance[0]),
        'y':        float(warehouse_entrance[1]),
        'angle':    float(warehouse_entrance[2]),
        'pos_unit': POSITION_UNIT.PIXELS,
        'ang_unit': ANGLE_UNIT.RADIANS,
        **NAVIGATION_OPTIONS_WITH_CART
    }

NAV_WAREHOUSE_EXIT = {
        'x':        float(warehouse_exit[0]),
        'y':        float(warehouse_exit[1]),
        'angle':    float(warehouse_exit[2]),
        'pos_unit': POSITION_UNIT.PIXELS,
        'ang_unit': ANGLE_UNIT.RADIANS,
        **NAVIGATION_OPTIONS_WITH_CART
    }

NAV_CART_UNLOAD_POINT = {
        'x':        float(cart_unload_point[0]),
        'y':        float(cart_unload_point[1]),
        'angle':    float(cart_unload_point[2]),
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

BASEMENT_ROUTES = {
    'attach_elev': [
        {
            'name': 'Navigation to warehouse exit',
            'type': 'nav_to_point',
            'point' : {
                **NAV_WAREHOUSE_EXIT
            },
            'teleoperator_if_fail': True,
        },
        {
            'name': 'Automatic door warehouse',
            'type': 'automatic_door',
            'zone_name': WAREHOUSE_ZONE_NAME,
            'after_door_point': {
                **FLOOR__00['waiting_elevator']
            },
            'tags_ids': [25],
            'tags_sizes': [0.12],
        },
        {
            'name': 'Navigation to waiting elevator',
            'type': 'nav_to_point',
            'point' : {
                **FLOOR__00['waiting_elevator']
            },
            'teleoperator_if_fail': True,
        },
    ],
    'elev_detach': [
        {
            'name': 'Navigation to warehouse entrance',
            'type': 'nav_to_point',
            'point' : {
                **NAV_WAREHOUSE_ENTRANCE
            },
            'teleoperator_if_fail': True,
        },
        {
            'name': 'Automatic door warehouse',
            'type': 'automatic_door',
            'zone_name': WAREHOUSE_ZONE_NAME,
            'after_door_point': {
                **NAV_CART_UNLOAD_POINT
            },
            'tags_ids': [26],
            'tags_sizes': [0.12],
        },
        {
            'name': 'Navigation to detaching point',
            'type': 'nav_to_point',
            'point' : {
                **NAV_CART_UNLOAD_POINT
            },
            'teleoperator_if_fail': True,
        }
    ],
    
    'home': [
        {
            'name': 'Navigation to home',
            'type': 'nav_to_point',
            'point' : {}, # it uses the home position from the map
            'teleoperator_if_fail': True,
        },
    ],
    'cart_point': [
        {
            'name': 'Navigation to cart point',
            'type': 'nav_to_point',
            'point' : {}, # it uses the cart position from the parameter of the app
            'teleoperator_if_fail': True,
        },
    ]
    
}
