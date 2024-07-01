from raya.enumerations import POSITION_UNIT, ANGLE_UNIT

NAV = dict()

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
    [-1.23,  0.32],
    [ 0.25,  0.32],
    [ 0.25, -0.32],
    [-1.23, -0.32]
]

GARY_SELECTED_CART_FOOTPRINT = GARY_FOOTPRINT_MEDIUM_CART

def set_nav_data(map_name):
    global NAV_HOME_POSITION_NAME, NAV_WAREHOUSE_ENTRANCE
    global NAV_WAREHOUSE_EXIT, NAV_CART_POINT
    global NAV_WAREHOUSE_MAP_NAME
    
    NAV_WAREHOUSE_MAP_NAME = map_name
    NAV_HOME_POSITION_NAME = NAV[map_name]["data"]["NAV_HOME_POSITION_NAME"]
    NAV_WAREHOUSE_ENTRANCE = NAV[map_name]["data"]["NAV_WAREHOUSE_ENTRANCE"]
    NAV_WAREHOUSE_EXIT = NAV[map_name]["data"]["NAV_WAREHOUSE_EXIT"]
    NAV_CART_POINT = NAV[map_name]["data"]["NAV_CART_POINT"]
    # return NAV_HOME_POSITION_NAME, NAV_WAREHOUSE_ENTRANCE, NAV_WAREHOUSE_EXIT, NAV_CART_POINT

NAVIGATION_OPTIONS = {
    'options': {
        'behavior_tree': 'navigate_long_footprint'
    }
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
NAV_CART_POINT = {
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
        "NAV_CART_POINT": NAV_CART_POINT,
    }
}


# --------------------------------------------------
#             philly_hospital__basement
# --------------------------------------------------

NAV_WAREHOUSE_MAP_NAME = 'hospital_02'
NAV_HOME_POSITION_NAME = 'home'
NAV_WAREHOUSE_ENTRANCE = {
        'x':        1683.0,
        'y':        701.0,
        'angle':    146.95,
        'pos_unit': POSITION_UNIT.PIXELS, 
        'ang_unit': ANGLE_UNIT.DEGREES,
        **NAVIGATION_OPTIONS
    }
NAV_WAREHOUSE_EXIT = {
        'x':        1518.0,
        'y':        633.0,
        'angle':    -0.03853223357465533,
        'pos_unit': POSITION_UNIT.PIXELS, 
        'ang_unit': ANGLE_UNIT.DEGREES,
        **NAVIGATION_OPTIONS
    }
NAV_CART_POINT = {
        'x':        1457.0,
        'y':        631.0,
        'angle':    -0.0048924850246489515,
        'pos_unit': POSITION_UNIT.PIXELS, 
        'ang_unit': ANGLE_UNIT.DEGREES,
        **NAVIGATION_OPTIONS
    }

NAV[NAV_WAREHOUSE_MAP_NAME] = {
    "data": {
        "NAV_HOME_POSITION_NAME": NAV_HOME_POSITION_NAME,
        "NAV_WAREHOUSE_ENTRANCE": NAV_WAREHOUSE_ENTRANCE,
        "NAV_WAREHOUSE_EXIT": NAV_WAREHOUSE_EXIT,
        "NAV_CART_POINT": NAV_CART_POINT,
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

NAV_CART_POINT = {
        'x':        453.0,
        'y':        274.0,
        'angle':    -2.35, 
        'pos_unit': POSITION_UNIT.PIXELS, 
        'ang_unit': ANGLE_UNIT.DEGREES,
        **NAVIGATION_OPTIONS
    }


set_nav_data('hospital_02')



