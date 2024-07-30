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

NAV_WAREHOUSE_BUILDING_NAME = 'philly_hospital'
NAV_HOME_POSITION_NAME = 'home'
WAREHOUSE_FLOOR = 'basement'
WAREHOUSE_MAP_NAME = f'{NAV_WAREHOUSE_BUILDING_NAME}__{WAREHOUSE_FLOOR}'
NAV_WAREHOUSE_ENTRANCE = {
        'x':        1824.0,
        'y':        430.0,
        'angle':    -18.06,
        'pos_unit': POSITION_UNIT.PIXELS, 
        'ang_unit': ANGLE_UNIT.DEGREES,
        **NAVIGATION_OPTIONS_WITH_CART
    }
NAV_WAREHOUSE_EXIT = {
        'x':        2016.0,
        'y':        472.0,
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
                'localization': {
                  'inside_elevator': {
                    'x': 398.0,
                    'y': 342.0,
                    'angle': -90.0,
                    'pos_unit': POSITION_UNIT.PIXELS,
                    'ang_unit': ANGLE_UNIT.DEGREES,
                  },
                  'outside_elevator': {
                        'divisions': 3,
                        'closest_point': {
                            'x': 397.0,
                            'y': 530.0,
                            'angle': -90.0,
                            'pos_unit': POSITION_UNIT.PIXELS,
                            'ang_unit': ANGLE_UNIT.DEGREES,
                        },
                        'farthest_point': {
                            'x': 398.0,
                            'y': 443.0,
                            'angle': -90.0,
                            'pos_unit': POSITION_UNIT.PIXELS,
                            'ang_unit': ANGLE_UNIT.DEGREES,
                        },
                  }
                },
                'entry_point': {
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
            '2': {
                'localization': {
                  'inside_elevator': {
                    'x': 537.0,
                    'y': 344.0,
                    'angle': -90.0,
                    'pos_unit': POSITION_UNIT.PIXELS,
                    'ang_unit': ANGLE_UNIT.DEGREES,
                  },
                  'outside_elevator': {
                        'divisions': 3,
                        'closest_point': {
                            'x': 537.0,
                            'y': 533.0,
                            'angle': -90.0,
                            'pos_unit': POSITION_UNIT.PIXELS,
                            'ang_unit': ANGLE_UNIT.DEGREES,
                        },
                        'farthest_point': {
                            'x': 537.0,
                            'y': 445.0,
                            'angle': -90.0,
                            'pos_unit': POSITION_UNIT.PIXELS,
                            'ang_unit': ANGLE_UNIT.DEGREES,
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
                'localization': {
                  'inside_elevator': {
                    'x': 670.0,
                    'y': 341.0,
                    'angle': -90.0,
                    'pos_unit': POSITION_UNIT.PIXELS,
                    'ang_unit': ANGLE_UNIT.DEGREES,
                  },
                  'outside_elevator': {
                        'divisions': 3,
                        'closest_point': {
                            'x': 668.0,
                            'y': 533.0,
                            'angle': -90.0,
                            'pos_unit': POSITION_UNIT.PIXELS,
                            'ang_unit': ANGLE_UNIT.DEGREES,
                        },
                        'farthest_point': {
                            'x': 667.0,
                            'y': 446.0,
                            'angle': -90.0,
                            'pos_unit': POSITION_UNIT.PIXELS,
                            'ang_unit': ANGLE_UNIT.DEGREES,
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
                'leaving': {
                    'x': 667.0,
                    'y': 480.0,
                    'angle': -90.0,
                    'pos_unit': POSITION_UNIT.PIXELS,
                    'ang_unit': ANGLE_UNIT.DEGREES,
                    **NAVIGATION_OPTIONS_WITH_CART
                }
            },
        }
    },
    '7': {
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
                  'inside_elevator': {
                    'x': 436.0,
                    'y': 2175.0,
                    'angle': 1.8395248997063303,
                    'pos_unit': POSITION_UNIT.PIXELS,
                    'ang_unit': ANGLE_UNIT.RADIANS,
                  },
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
                'leaving': {
                    'x': 409.0,
                    'y': 2052.0,
                    'angle': 1.8419213429531647,
                    'pos_unit': POSITION_UNIT.PIXELS,
                    'ang_unit': ANGLE_UNIT.RADIANS,
                    **NAVIGATION_OPTIONS_WITH_CART
                }
            },
            '2': {
                'localization': {
                  'inside_elevator': {
                    'x': 302.0,
                    'y': 2217.0,
                    'angle': 1.8395248997063303,
                    'pos_unit': POSITION_UNIT.PIXELS,
                    'ang_unit': ANGLE_UNIT.RADIANS,
                  },
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
                'leaving': {
                    'x': 276.0,
                    'y': 2092.0,
                    'angle': 1.8247921510537317,
                    'pos_unit': POSITION_UNIT.PIXELS,
                    'ang_unit': ANGLE_UNIT.RADIANS,
                    **NAVIGATION_OPTIONS_WITH_CART
                }
            },
            '3': {
                'localization': {
                  'inside_elevator': {
                    'x': 172.0,
                    'y': 2253.0,
                    'angle': 1.8395248997063303,
                    'pos_unit': POSITION_UNIT.PIXELS,
                    'ang_unit': ANGLE_UNIT.RADIANS,
                  },
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
                'leaving': {
                    'x': 147.0,
                    'y': 2126.0,
                    'angle': 1.7867585067125054,
                    'pos_unit': POSITION_UNIT.PIXELS,
                    'ang_unit': ANGLE_UNIT.RADIANS,
                    **NAVIGATION_OPTIONS_WITH_CART
                }
            },
        },
        'units': {
            'unit1' : '7E',
            'unit2' : '7W'
        },
    },
} 

COST_MAPS_CONFIG = {
    'costmap_format': 'cost.[initial_point]_[final_point]',
    'default_costmap_name': 'map',
    'unit_identifier': 'unit',
}
