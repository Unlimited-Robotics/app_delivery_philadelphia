from .constants import *

from raya.enumerations import POSITION_UNIT, ANGLE_UNIT

WAREHOUSE_ZONE_NAME = 'warehouse'

NAV_CART_LOAD_POINT_OPTIONS = {
    'pos_unit': POSITION_UNIT.PIXELS, 
    'ang_unit': ANGLE_UNIT.DEGREES,
    **NAVIGATION_OPTIONS_WITHOUT_CART
}

NAV_WAREHOUSE_ENTRANCE = {
        'x':        2010.0,
        'y':        879.0,
        'angle':    -2.9266371161831866,
        'pos_unit': POSITION_UNIT.PIXELS,
        'ang_unit': ANGLE_UNIT.RADIANS,
        **NAVIGATION_OPTIONS_WITH_CART
    }

NAV_WAREHOUSE_EXIT = {
        'x':        1761.0,
        'y':        904.0,
        'angle':    0.22435328773765226,
        'pos_unit': POSITION_UNIT.PIXELS,
        'ang_unit': ANGLE_UNIT.RADIANS,
        **NAVIGATION_OPTIONS_WITH_CART
    }

NAV_CART_UNLOAD_POINT = {
        'x':        605.0,
        'y':        1141.0,
        'angle':    -2.922,
        'pos_unit': POSITION_UNIT.PIXELS,
        'ang_unit': ANGLE_UNIT.RADIANS,
        **NAVIGATION_OPTIONS_WITH_CART
    }

FLOOR__00 = {
    'max_elevators': 3,
    'waiting_elevator': {
        'x': 2833.0,
        'y': 706.0,
        'angle': 0.2177464694155388,
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
                        'x': 3364.0,
                        'y': 513.0,
                        'angle': 1.8016715566010912,
                        'pos_unit': POSITION_UNIT.PIXELS,
                        'ang_unit': ANGLE_UNIT.RADIANS,
                        **NAVIGATION_OPTIONS_WITH_CART
                    },
                    'farthest_point': {
                        'x': 3376.0,
                        'y': 565.0,
                        'angle': 1.7998981911927987,
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
                        'x': 3230.0,
                        'y': 539.0,
                        'angle': 1.810375662278539,
                        'pos_unit': POSITION_UNIT.PIXELS,
                        'ang_unit': ANGLE_UNIT.RADIANS,
                        **NAVIGATION_OPTIONS_WITH_CART
                    },
                    'farthest_point': {
                        'x': 3242.0,
                        'y': 593.0,
                        'angle': 1.8100282560620327,
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
                        'x': 3105.0,
                        'y': 568.0,
                        'angle': 1.8079203614959949,
                        'pos_unit': POSITION_UNIT.PIXELS,
                        'ang_unit': ANGLE_UNIT.RADIANS,
                        **NAVIGATION_OPTIONS_WITH_CART
                    },
                    'farthest_point': {
                        'x': 3114.0,
                        'y': 618.0,
                        'angle': 1.8034004002899453,
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
