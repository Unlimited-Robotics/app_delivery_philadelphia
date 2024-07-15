from raya.enumerations import POSITION_UNIT, ANGLE_UNIT

NAV = dict()

NAVIGATION_TRY_LIMIT = 1
OBSTACLE_DETECTION_THRESHOLDS = [2, 7]

GARY_FOOTPRINT = [
    [-0.25,  0.32],
    [ 0.25,  0.32],
    [ 0.25, -0.32],
    [-0.25, -0.32]
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
        [-1.13,  0.20],
        [-0.24,  0.20],
        [-0.24,  0.225],
        [ 0.24,  0.225],
        [ 0.24, -0.225],
        [-0.24, -0.225],
        [-0.24, -0.20],
        [-1.13,  -0.20],
]

GARY_SELECTED_CART_FOOTPRINT = GARY_FOOTPRINT_SMALL_CART

def set_nav_data(map_name):
    global NAV_HOME_POSITION_NAME, NAV_WAREHOUSE_ENTRANCE
    global NAV_WAREHOUSE_EXIT, NAV_CART_LOAD_POINT
    global NAV_WAREHOUSE_MAP_NAME, NAV_CART_UNLOAD_POINT
    
    NAV_WAREHOUSE_MAP_NAME = map_name
    NAV_HOME_POSITION_NAME = NAV[map_name]["data"]["NAV_HOME_POSITION_NAME"]
    NAV_WAREHOUSE_ENTRANCE = NAV[map_name]["data"]["NAV_WAREHOUSE_ENTRANCE"]
    NAV_WAREHOUSE_EXIT = NAV[map_name]["data"]["NAV_WAREHOUSE_EXIT"]
    NAV_CART_LOAD_POINT = NAV[map_name]["data"]["NAV_CART_LOAD_POINT"]
    NAV_CART_UNLOAD_POINT = NAV[map_name]["data"]["NAV_CART_UNLOAD_POINT"]

NAVIGATION_OPTIONS = {
    'options': {
        'behavior_tree': 'replan_if_needed_long_footprint'
    }
}

NAVIGATION_OPTIONS_HOME = {
    'options': {
        'behavior_tree': 'navigate_and_replan_if_needed'
    }
}



# --------------------------------------------------
#             Bogota_Office__minigary.101
# --------------------------------------------------

NAV_WAREHOUSE_MAP_NAME = 'Bogota_Office__minigary.101'
NAV_HOME_POSITION_NAME = 'home'

NAV_WAREHOUSE_ENTRANCE = {
        'x':        343.0,
        'y':        430.0,
        'angle':    66.88, 
        'pos_unit': POSITION_UNIT.PIXELS, 
        'ang_unit': ANGLE_UNIT.DEGREES,
        **NAVIGATION_OPTIONS
    }

NAV_WAREHOUSE_EXIT = {
        'x':        367.0,
        'y':        365.0,
        'angle':    -105.5634, 
        'pos_unit': POSITION_UNIT.PIXELS, 
        'ang_unit': ANGLE_UNIT.DEGREES,
        **NAVIGATION_OPTIONS
    }

NAV_CART_LOAD_POINT = {
        'x':        453.0,
        'y':        274.0,
        'angle':    -2.35, 
        'pos_unit': POSITION_UNIT.PIXELS, 
        'ang_unit': ANGLE_UNIT.DEGREES,
        **NAVIGATION_OPTIONS
    }
NAV_CART_UNLOAD_POINT = {
        'x':        453.0,
        'y':        274.0,
        'angle':    -2.35, 
        'pos_unit': POSITION_UNIT.PIXELS, 
        'ang_unit': ANGLE_UNIT.DEGREES,
        **NAVIGATION_OPTIONS
    }


# --------------------------------------------------
#                  elisha__part1
# --------------------------------------------------

NAV_WAREHOUSE_MAP_NAME = 'elisha__part1'
NAV_HOME_POSITION_NAME = 'home'
NAV_WAREHOUSE_ENTRANCE = {
        'x':        324.0,
        'y':        217.0,
        'angle':    178.69,
        'pos_unit': POSITION_UNIT.PIXELS, 
        'ang_unit': ANGLE_UNIT.DEGREES,
        **NAVIGATION_OPTIONS
    }
NAV_WAREHOUSE_EXIT = {
        'x':        234.0,
        'y':        217.0,
        'angle':    -6.19,
        'pos_unit': POSITION_UNIT.PIXELS, 
        'ang_unit': ANGLE_UNIT.DEGREES,
        **NAVIGATION_OPTIONS
    }
NAV_CART_LOAD_POINT = {
        'x':        170.0,
        'y':        217.0,
        'angle':    -93.94,
        'pos_unit': POSITION_UNIT.PIXELS, 
        'ang_unit': ANGLE_UNIT.DEGREES,
        **NAVIGATION_OPTIONS
    }
NAV_CART_UNLOAD_POINT = {
        'x':        170.0,
        'y':        217.0,
        'angle':    -93.94,
        'pos_unit': POSITION_UNIT.PIXELS, 
        'ang_unit': ANGLE_UNIT.DEGREES,
        **NAVIGATION_OPTIONS
    }

NAV[NAV_WAREHOUSE_MAP_NAME] = {
    "data": {
        "NAV_HOME_POSITION_NAME": NAV_HOME_POSITION_NAME,
        "NAV_WAREHOUSE_ENTRANCE": NAV_WAREHOUSE_ENTRANCE,
        "NAV_WAREHOUSE_EXIT": NAV_WAREHOUSE_EXIT,
        "NAV_CART_LOAD_POINT": NAV_CART_LOAD_POINT,
    }
}


# --------------------------------------------------
#             philly_hospital__basement
# --------------------------------------------------

NAV_WAREHOUSE_MAP_NAME = 'philly_hospital__basement'
NAV_HOME_POSITION_NAME = 'home'
NAV_WAREHOUSE_ENTRANCE = {
        'x':        1841.0,
        'y':        436.0,
        'angle':    -0.4119695245183761,
        'pos_unit': POSITION_UNIT.PIXELS, 
        'ang_unit': ANGLE_UNIT.DEGREES,
        **NAVIGATION_OPTIONS
    }
NAV_WAREHOUSE_EXIT = {
        'x':        2019.0,
        'y':        472.0,
        'angle':    179.133528312283026,
        'pos_unit': POSITION_UNIT.PIXELS, 
        'ang_unit': ANGLE_UNIT.DEGREES,
        **NAVIGATION_OPTIONS
    }
NAV_CART_LOAD_POINT = {
        'x':        3595.0,
        'y':        411.0,
        'angle':    -97.7,
        'pos_unit': POSITION_UNIT.PIXELS, 
        'ang_unit': ANGLE_UNIT.DEGREES,
        **NAVIGATION_OPTIONS_HOME
    }
# NAV_CART_LOAD_POINT = {
#         'x':        3527.0,
#         'y':        419.0,
#         'angle':    -92.12,
#         'pos_unit': POSITION_UNIT.PIXELS, 
#         'ang_unit': ANGLE_UNIT.DEGREES,
#         **NAVIGATION_OPTIONS_HOME
#     }
NAV_CART_UNLOAD_POINT = {
        'x':        3591.0,
        'y':        310.0,
        'angle':    -0.1,
        'pos_unit': POSITION_UNIT.PIXELS, 
        'ang_unit': ANGLE_UNIT.DEGREES,
        **NAVIGATION_OPTIONS
    }

NAV[NAV_WAREHOUSE_MAP_NAME] = {
    "data": {
        "NAV_HOME_POSITION_NAME": NAV_HOME_POSITION_NAME,
        "NAV_WAREHOUSE_ENTRANCE": NAV_WAREHOUSE_ENTRANCE,
        "NAV_WAREHOUSE_EXIT": NAV_WAREHOUSE_EXIT,
        "NAV_CART_LOAD_POINT": NAV_CART_LOAD_POINT,
    }
}
set_nav_data('philly_hospital__basement')



