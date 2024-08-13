from .floors import *

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
        [-1.22,  0.22],
        [-0.24,  0.22],
        [-0.24,  0.27],
        [ 0.24,  0.27],
        [ 0.24, -0.27],
        [-0.24, -0.27],
        [-0.24, -0.22],
        [-1.22, -0.22],
    ]

GARY_SELECTED_CART_FOOTPRINT = GARY_FOOTPRINT_SMALL_CART

# --------------------------------------------------
#             philly_hospital__basement
# --------------------------------------------------


WAREHOUSE_FLOOR = '00'
NAV_HOME_POSITION_NAME = 'home_1'
MAP_VERSION = 'v2'
NAV_MAP_NAME = f'phillytemplehosp_{MAP_VERSION}'
WAREHOUSE_MAP_NAME = f'{NAV_MAP_NAME}__{WAREHOUSE_FLOOR}'

COST_MAPS_CONFIG = {
    'costmap_format': 'cost.[initial_point]_[final_point]',
    'default_costmap_name': 'map',
    'unit_identifier': 'unit',
}

FLOORS = {
    '00': FLOOR__00,
    '02': FLOOR__02,
    '04': FLOOR__04,
    '05': FLOOR__05,
    '06': FLOOR__06,
    '07': FLOOR__07,
    '08': FLOOR__08,
    '09': FLOOR__09,
}

SKILL_NAVIGATION = {
    '00': {**BASEMENT_ROUTES},
    '02': {**FLOOR_02_ROUTES},
    '04': {**FLOOR_04_ROUTES},
    '05': {**FLOOR_05_ROUTES},
    '06': {**FLOOR_06_ROUTES},
    '07': {**FLOOR_07_ROUTES},
    '08': {**FLOOR_08_ROUTES},
    '09': {**FLOOR_09_ROUTES},
}
