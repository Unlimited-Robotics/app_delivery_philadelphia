from .floors import *

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

PARKING_SPOT_SUFFIX = '[INITIAL]'
NAV_HOME_POSITION_NAME = f'home_{PARKING_SPOT_SUFFIX}'
NAV_PARKING_POSITION_NAME = f'parking_{PARKING_SPOT_SUFFIX}'


COST_MAPS_CONFIG = {
    'costmap_format': 'cost.[initial_point]_[final_point]',
    'default_costmap_name': 'map',
    'unit_identifier': 'unit',
}

WAREHOUSE_FLOOR = 'Basement'

FLOORS = {
    WAREHOUSE_FLOOR: FLOOR__00,
    '2': FLOOR__02,
    '4': FLOOR__04,
    '5': FLOOR__05,
    '6': FLOOR__06,
    '7': FLOOR__07,
    '8': FLOOR__08,
    '9': FLOOR__09,
}

SKILL_NAVIGATION = {
    '2': {**FLOOR_02_ROUTES},
    '4': {**FLOOR_04_ROUTES},
    '5': {**FLOOR_05_ROUTES},
    '6': {**FLOOR_06_ROUTES},
    '7': {**FLOOR_07_ROUTES},
    '8': {**FLOOR_08_ROUTES},
    '9': {**FLOOR_09_ROUTES},
}
