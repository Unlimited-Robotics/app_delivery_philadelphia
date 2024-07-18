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

GARY_FOOTPRINT_BIG_CART = [
    [-1.60,  0.32],
    [ 0.25,  0.32],
    [ 0.25, -0.32],
    [-1.60, -0.32]
]

GARY_FOOTPRINT_MEDIUM_CART = [
    [-1.28,  0.32],
    [ 0.25,  0.32],
    [ 0.25, -0.32],
    [-1.28, -0.32]
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

NAV_WAREHOUSE_BUILDING_NAME = 'philly_hospital'
NAV_HOME_POSITION_NAME = 'home'
WAREHOUSE_FLOOR = 'basement'
WAREHOUSE_MAP_NAME = f'{NAV_WAREHOUSE_BUILDING_NAME}__{WAREHOUSE_FLOOR}'
NAV_WAREHOUSE_ENTRANCE = {
        'x':        1841.0,
        'y':        436.0,
        'angle':    -0.4119695245183761,
        'pos_unit': POSITION_UNIT.PIXELS, 
        'ang_unit': ANGLE_UNIT.DEGREES,
        **NAVIGATION_OPTIONS_WITH_CART
    }
NAV_WAREHOUSE_EXIT = {
        'x':        2008.0,
        'y':        484.0,
        'angle':    179.133528312283026,
        'pos_unit': POSITION_UNIT.PIXELS, 
        'ang_unit': ANGLE_UNIT.DEGREES,
        **NAVIGATION_OPTIONS_WITH_CART
    }
NAV_CART_UNLOAD_POINT = {
        'x':        3190.0,
        'y':        478.0,
        'angle':    1.7,
        'pos_unit': POSITION_UNIT.PIXELS, 
        'ang_unit': ANGLE_UNIT.DEGREES,
        **NAVIGATION_OPTIONS_WITH_CART
    }

FLOORS = {
    'basement': {
        'max_elevators': 3,
        'waiting_elevator': {
            'x': 971.0,
            'y': 449.0,
            'angle': -175.3,
            'pos_unit': POSITION_UNIT.PIXELS,
            'ang_unit': ANGLE_UNIT.DEGREES,
            **NAVIGATION_OPTIONS_WITH_CART
        },
        'elevator': {
            '1': {
                'entering': {
                    'x': 667.0,
                    'y': 545.0,
                    'angle': -90.0,
                    'pos_unit': POSITION_UNIT.PIXELS,
                    'ang_unit': ANGLE_UNIT.DEGREES,
                    **NAVIGATION_OPTIONS_WITH_CART
                },
                'leaving': {
                    'x': 667.0,
                    'y': 480.0,
                    'angle': -90.0,
                    'pos_unit': POSITION_UNIT.PIXELS,
                    'ang_unit': ANGLE_UNIT.DEGREES,
                    **NAVIGATION_OPTIONS_WITH_CART
                }
            },
            '2': {
                'entering': {
                    'x': 536.0,
                    'y': 545.0,
                    'angle': -90.0,
                    'pos_unit': POSITION_UNIT.PIXELS,
                    'ang_unit': ANGLE_UNIT.DEGREES,
                    **NAVIGATION_OPTIONS_WITH_CART
                },
                'leaving': {
                    'x': 536.0,
                    'y': 480.0,
                    'angle': -90.0,
                    'pos_unit': POSITION_UNIT.PIXELS,
                    'ang_unit': ANGLE_UNIT.DEGREES,
                    **NAVIGATION_OPTIONS_WITH_CART
                }
            },
            '3': {
                'entering': {
                    'x': 401.0,
                    'y': 545.0,
                    'angle': -90.0,
                    'pos_unit': POSITION_UNIT.PIXELS,
                    'ang_unit': ANGLE_UNIT.DEGREES,
                    **NAVIGATION_OPTIONS_WITH_CART
                },
                'leaving': {
                    'x': 401.0,
                    'y': 480.0,
                    'angle': -90.0,
                    'pos_unit': POSITION_UNIT.PIXELS,
                    'ang_unit': ANGLE_UNIT.DEGREES,
                    **NAVIGATION_OPTIONS_WITH_CART
                }
            },
        }
    },
    'basement2': {
        'max_elevators': 3,
        'waiting_elevator': {
            'x': 227.0,
            'y': 529.0,
            'angle': 0.0828,
            'pos_unit': POSITION_UNIT.PIXELS,
            'ang_unit': ANGLE_UNIT.DEGREES,
            **NAVIGATION_OPTIONS_WITH_CART
        },
        'elevator': {
            '1': {
                'entering': {
                    'x': 667.0,
                    'y': 545.0,
                    'angle': -90.0,
                    'pos_unit': POSITION_UNIT.PIXELS,
                    'ang_unit': ANGLE_UNIT.DEGREES,
                    **NAVIGATION_OPTIONS_WITH_CART
                },
                'leaving': {
                    'x': 667.0,
                    'y': 480.0,
                    'angle': -90.0,
                    'pos_unit': POSITION_UNIT.PIXELS,
                    'ang_unit': ANGLE_UNIT.DEGREES,
                    **NAVIGATION_OPTIONS_WITH_CART
                }
            },
            '2': {
                'entering': {
                    'x': 536.0,
                    'y': 545.0,
                    'angle': -90.0,
                    'pos_unit': POSITION_UNIT.PIXELS,
                    'ang_unit': ANGLE_UNIT.DEGREES,
                    **NAVIGATION_OPTIONS_WITH_CART
                },
                'leaving': {
                    'x': 536.0,
                    'y': 480.0,
                    'angle': -90.0,
                    'pos_unit': POSITION_UNIT.PIXELS,
                    'ang_unit': ANGLE_UNIT.DEGREES,
                    **NAVIGATION_OPTIONS_WITH_CART
                }
            },
            '3': {
                'entering': {
                    'x': 401.0,
                    'y': 545.0,
                    'angle': -90.0,
                    'pos_unit': POSITION_UNIT.PIXELS,
                    'ang_unit': ANGLE_UNIT.DEGREES,
                    **NAVIGATION_OPTIONS_WITH_CART
                },
                'leaving': {
                    'x': 401.0,
                    'y': 480.0,
                    'angle': -90.0,
                    'pos_unit': POSITION_UNIT.PIXELS,
                    'ang_unit': ANGLE_UNIT.DEGREES,
                    **NAVIGATION_OPTIONS_WITH_CART
                }
            },
        }
    },
} 
