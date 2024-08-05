from raya.enumerations import POSITION_UNIT, ANGLE_UNIT

NAV = dict()

NAVIGATION_TRY_LIMIT = 1
OBSTACLE_DETECTION_THRESHOLDS = [2, 7]

GARY_FOOTPRINT = [
    [-0.25,  0.28],
    [ 0.25,  0.28],
    [ 0.25, -0.28],
    [-0.25, -0.28]
]

GARY_FOOTPRINT_SMALL_CART = [
        [-1.21,  0.25],
        [-0.24,  0.25],
        [-0.24,  0.225],
        [ 0.24,  0.225],
        [ 0.24, -0.225],
        [-0.24, -0.225],
        [-0.24, -0.25],
        [-1.21, -0.25],
]

GARY_SELECTED_CART_FOOTPRINT = GARY_FOOTPRINT_SMALL_CART

NAVIGATION_OPTIONS_WITH_CART = {
    'options': {
        'behavior_tree': 'replan_if_needed_long_footprint'
    }
}

NAVIGATION_OPTIONS_WITHOUT_CART = {
    'options': {
        'behavior_tree': 'navigate_and_replan_if_needed'
    },
    'xy_tolerance': 0.05,
}

NAV_CART_LOAD_POINT_OPTIONS = {
        'pos_unit': POSITION_UNIT.PIXELS, 
        'ang_unit': ANGLE_UNIT.DEGREES,
        **NAVIGATION_OPTIONS_WITHOUT_CART
    }

# --------------------------------------------------
#             philly_hospital__basement
# --------------------------------------------------

MAP_VERSION = 'v2'
NAV_MAP_NAME = f'phillytemplehosp_{MAP_VERSION}'
WAREHOUSE_FLOOR = '00'
WAREHOUSE_MAP_NAME = f'{NAV_MAP_NAME}__{WAREHOUSE_FLOOR}'

NAV_HOME_POSITION_NAME = 'home'

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

# TODO change this point
NAV_CART_UNLOAD_POINT = {
        'x':        3190.0,
        'y':        478.0,
        'angle':    1.7,
        'pos_unit': POSITION_UNIT.PIXELS, 
        'ang_unit': ANGLE_UNIT.DEGREES,
        **NAVIGATION_OPTIONS_WITH_CART
    }

COST_MAPS_CONFIG = {
    'costmap_format': 'cost.[initial_point]_[final_point]',
    'default_costmap_name': 'map',
    'unit_identifier': 'unit',
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
                    },
                    'farthest_point': {
                        'x': 3376.0,
                        'y': 565.0,
                        'angle': 1.7998981911927987,
                        'pos_unit': POSITION_UNIT.PIXELS,
                        'ang_unit': ANGLE_UNIT.RADIANS,
                    },
                }
            },
            'entry_point': {
                'x': 3364.0,
                'y': 513.0,
                'angle': 1.7998981911927987,
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.RADIANS,
                **NAVIGATION_OPTIONS_WITH_CART
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
                    },
                    'farthest_point': {
                        'x': 3242.0,
                        'y': 593.0,
                        'angle': 1.8100282560620327,
                        'pos_unit': POSITION_UNIT.PIXELS,
                        'ang_unit': ANGLE_UNIT.RADIANS,
                    },
                }
            },
            'entry_point': {
                'x': 536.0,
                'y': 545.0,
                'angle': -90.0,
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.DEGREES,
                **NAVIGATION_OPTIONS_WITH_CART
            },
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
                    },
                    'farthest_point': {
                        'x': 3114.0,
                        'y': 618.0,
                        'angle': 1.8034004002899453,
                        'pos_unit': POSITION_UNIT.PIXELS,
                        'ang_unit': ANGLE_UNIT.RADIANS,
                    },
                }
            },
            'entry_point': {
                'x': 667.0,
                'y': 545.0,
                'angle': -90.0,
                'pos_unit': POSITION_UNIT.PIXELS,
                'ang_unit': ANGLE_UNIT.DEGREES,
                **NAVIGATION_OPTIONS_WITH_CART
            },
        },
    }
}

FLOOR__07 = {
    'max_elevators': 3,
    'waiting_elevator': {
        'x': 645.0,
        'y': 2016.0,
        'angle': -2.8441741285876745,
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
                        'x': 393.0,
                        'y': 2000.0,
                        'angle': 1.8395248997063303,
                        'pos_unit': POSITION_UNIT.PIXELS,
                        'ang_unit': ANGLE_UNIT.RADIANS,
                    },
                    'farthest_point': {
                        'x': 412.0,
                        'y': 2090.0,
                        'angle': 1.8419213429531647,
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
                        'x': 255.0,
                        'y': 2044.0,
                        'angle': 1.8395248997063303,
                        'pos_unit': POSITION_UNIT.PIXELS,
                        'ang_unit': ANGLE_UNIT.RADIANS,
                    },
                    'farthest_point': {
                        'x': 278.0,
                        'y': 2123.0,
                        'angle': 1.8419213429531647,
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
                        'x': 134.0,
                        'y': 2074.0,
                        'angle': 1.8395248997063303,
                        'pos_unit': POSITION_UNIT.PIXELS,
                        'ang_unit': ANGLE_UNIT.RADIANS,
                    },
                    'farthest_point': {
                        'x': 148.0,
                        'y': 2156.0,
                        'angle': 1.8419213429531647,
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
        'unit1' : '7E',
        'unit2' : '7W'
    },
}


FLOORS = {
    '00': FLOOR__00,
    '07': FLOOR__07
}


SKILL_NAVIGATION = {
    'home_elev': [
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
            'after_door_point': {
                **FLOOR__00['waiting_elevator']
            },
            'tags_ids': [25, 26],
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
    ]
}