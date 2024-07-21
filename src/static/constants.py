from __future__ import annotations

NAV_WAREHOUSE_ZONE_NAME = 'warehouse'

TIME_TO_WAIT_AFTER_BUTTON_PRESS = 0.1
TIME_BEETWEEN_NOTIFICATIONS_PACKAGE_ARRIVED = 10.0
TIME_PASSING_THROUGH_DOOR = 25.0

TIMEOUT_REQUEST_FOR_HELP = 5.0

CHEST_LISTENER_PATHS = ['/chest_button']

# door
CAMERAS_DETECTING_DOOR = ['nav_bottom']
DOOR_TAG_EXIT = 25
DOOR_TAG_ENTRANCE = 26
DOOR_TAGS = {
    'tag36h11': [DOOR_TAG_EXIT, DOOR_TAG_ENTRANCE],
}
DOOR_MODEL_PARAM = {
    'families': 'tag36h11',
    'nthreads': 4,
    'quad_decimate': 2.0,
    'quad_sigma': 0.0,
    'decode_sharpening': 0.25,
    'refine_edges': 1,
    'tag_size': 0.12,
}
DOOR_TAG_CALLBACK_TIMER = 4.0
DOOR_TAG_TIMEOUT = 10.0
