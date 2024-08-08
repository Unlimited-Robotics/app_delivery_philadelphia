from .constants import *

from raya.enumerations import POSITION_UNIT, ANGLE_UNIT

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
