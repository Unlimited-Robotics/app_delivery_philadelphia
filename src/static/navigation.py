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

def set_nav_data(map_name):
    global NAV_HOME_POSITION_NAME, NAV_WAREHOUSE_ENTRANCE
    global NAV_WAREHOUSE_EXIT, NAV_CART_LOAD_POINT
    global NAV_WAREHOUSE_BUILDING_NAME, NAV_CART_UNLOAD_POINT
    
    NAV_WAREHOUSE_BUILDING_NAME = map_name
    NAV_HOME_POSITION_NAME = NAV[map_name]["data"]["NAV_HOME_POSITION_NAME"]
    NAV_WAREHOUSE_ENTRANCE = NAV[map_name]["data"]["NAV_WAREHOUSE_ENTRANCE"]
    NAV_WAREHOUSE_EXIT = NAV[map_name]["data"]["NAV_WAREHOUSE_EXIT"]
    NAV_CART_LOAD_POINT = NAV[map_name]["data"]["NAV_CART_LOAD_POINT"]
    NAV_CART_UNLOAD_POINT = NAV[map_name]["data"]["NAV_CART_UNLOAD_POINT"]

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
        'x':        3142.0,
        'y':        490.0,
        'angle':    -2.53,
        'pos_unit': POSITION_UNIT.PIXELS, 
        'ang_unit': ANGLE_UNIT.DEGREES,
        **NAVIGATION_OPTIONS_WITH_CART
    }


# TODO CHANGE NAV_OPTIONS
NAV_ELEVATOR_WAITING_POINT = [
    {
        'x':        3562.0,
        'y':        338.0,
        'angle':    -90.0,
        'pos_unit': POSITION_UNIT.PIXELS, 
        'ang_unit': ANGLE_UNIT.DEGREES,
        **NAVIGATION_OPTIONS_WITH_CART   
    },
    {
        'x':        3562.0,
        'y':        338.0,
        'angle':    0.0,
        'pos_unit': POSITION_UNIT.PIXELS, 
        'ang_unit': ANGLE_UNIT.DEGREES,
        **NAVIGATION_OPTIONS_WITH_CART
    },
    {
        'x':        3562.0,
        'y':        338.0,
        'angle':    90.0,
        'pos_unit': POSITION_UNIT.PIXELS, 
        'ang_unit': ANGLE_UNIT.DEGREES,
        **NAVIGATION_OPTIONS_WITH_CART
    }
]

NAV_ELEVATOR_LEAVING_POINT = [
    {
        'x':        3529.0,
        'y':        291.0,
        'angle':    2.27,
        'pos_unit': POSITION_UNIT.PIXELS, 
        'ang_unit': ANGLE_UNIT.DEGREES,
        **NAVIGATION_OPTIONS_WITH_CART   
    },
    {
        'x':        3529.0,
        'y':        291.0,
        'angle':    2.27,
        'pos_unit': POSITION_UNIT.PIXELS, 
        'ang_unit': ANGLE_UNIT.DEGREES,
        **NAVIGATION_OPTIONS_WITH_CART
    },
    {
        'x':        3529.0,
        'y':        291.0,
        'angle':    2.27,
        'pos_unit': POSITION_UNIT.PIXELS, 
        'ang_unit': ANGLE_UNIT.DEGREES,
        **NAVIGATION_OPTIONS_WITH_CART
    }
]

FLOORS = {
    'basement': {
        'max_elevators': 3,
        'waiting_elevator': {
            'x': 971.0,
            'y': 449.0,
            'angle': -3.083,
            'pos_unit': POSITION_UNIT.PIXELS,
            'ang_unit': ANGLE_UNIT.DEGREES,
            **NAVIGATION_OPTIONS_WITH_CART
        },
        'elevator': {
            '1': {
                'ENTERING': {
                    'x': 667.0,
                    'y': 512.0,
                    'angle': -1.5729,
                    'pos_unit': POSITION_UNIT.PIXELS,
                    'ang_unit': ANGLE_UNIT.DEGREES,
                    **NAVIGATION_OPTIONS_WITH_CART
                },
                'LEAVING': {
                    'x': 667.0,
                    'y': 512.0,
                    'angle': 1.5729,
                    'pos_unit': POSITION_UNIT.PIXELS,
                    'ang_unit': ANGLE_UNIT.DEGREES,
                    **NAVIGATION_OPTIONS_WITH_CART
                }
            },
            '2': {
                'ENTERING': {
                    'x': 536.0,
                    'y': 512.0,
                    'angle': -1.587,
                    'pos_unit': POSITION_UNIT.PIXELS,
                    'ang_unit': ANGLE_UNIT.DEGREES,
                    **NAVIGATION_OPTIONS_WITH_CART
                },
                'LEAVING': {
                    'x': 536.0,
                    'y': 512.0,
                    'angle': -1.587,
                    'pos_unit': POSITION_UNIT.PIXELS,
                    'ang_unit': ANGLE_UNIT.DEGREES,
                    **NAVIGATION_OPTIONS_WITH_CART
                }
            },
            '3': {
                'ENTERING': {
                    'x': 401.0,
                    'y': 510.0,
                    'angle': -1.557,
                    'pos_unit': POSITION_UNIT.PIXELS,
                    'ang_unit': ANGLE_UNIT.DEGREES,
                    **NAVIGATION_OPTIONS_WITH_CART
                },
                'LEAVING': {
                    'x': 401.0,
                    'y': 510.0,
                    'angle': -1.557,
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
                'ENTERING': {
                    'x': 667.0,
                    'y': 512.0,
                    'angle': -1.5729,
                    'pos_unit': POSITION_UNIT.PIXELS,
                    'ang_unit': ANGLE_UNIT.DEGREES,
                    **NAVIGATION_OPTIONS_WITH_CART
                },
                'LEAVING': {
                    'x': 667.0,
                    'y': 512.0,
                    'angle': 1.5729,
                    'pos_unit': POSITION_UNIT.PIXELS,
                    'ang_unit': ANGLE_UNIT.DEGREES,
                    **NAVIGATION_OPTIONS_WITH_CART
                }
            },
            '2': {
                'ENTERING': {
                    'x': 536.0,
                    'y': 512.0,
                    'angle': -1.587,
                    'pos_unit': POSITION_UNIT.PIXELS,
                    'ang_unit': ANGLE_UNIT.DEGREES,
                    **NAVIGATION_OPTIONS_WITH_CART
                },
                'LEAVING': {
                    'x': 536.0,
                    'y': 512.0,
                    'angle': -1.587,
                    'pos_unit': POSITION_UNIT.PIXELS,
                    'ang_unit': ANGLE_UNIT.DEGREES,
                    **NAVIGATION_OPTIONS_WITH_CART
                }
            },
            '3': {
                'ENTERING': {
                    'x': 401.0,
                    'y': 510.0,
                    'angle': -1.557,
                    'pos_unit': POSITION_UNIT.PIXELS,
                    'ang_unit': ANGLE_UNIT.DEGREES,
                    **NAVIGATION_OPTIONS_WITH_CART
                },
                'LEAVING': {
                    'x': 401.0,
                    'y': 510.0,
                    'angle': -1.557,
                    'pos_unit': POSITION_UNIT.PIXELS,
                    'ang_unit': ANGLE_UNIT.DEGREES,
                    **NAVIGATION_OPTIONS_WITH_CART
                }
            },
        }
    },
} 


NAV[NAV_WAREHOUSE_BUILDING_NAME] = {
    "data": {
        "NAV_HOME_POSITION_NAME": NAV_HOME_POSITION_NAME,
        "NAV_WAREHOUSE_ENTRANCE": NAV_WAREHOUSE_ENTRANCE,
        "NAV_WAREHOUSE_EXIT": NAV_WAREHOUSE_EXIT,
        "NAV_CART_LOAD_POINT": NAV_CART_LOAD_POINT,
        "NAV_CART_UNLOAD_POINT": NAV_CART_UNLOAD_POINT
    }
}
set_nav_data('philly_hospital__basement')



