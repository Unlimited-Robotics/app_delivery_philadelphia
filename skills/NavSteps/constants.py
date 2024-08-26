from .steps_types.CommonType import constants as CommonTypeConstants
from .steps_types.NavToPoint import constants as NavToPointConstants
from .steps_types.AutomaticDoor import constants as AutomaticDoorConstants
from .steps_types.Teleoperation import constants as TeleoperationConstants

NAV_TO_POINT_TYPE_NAME = NavToPointConstants.TYPE_NAME
AUTOMATIC_DOOR_TYPE_NAME = AutomaticDoorConstants.TYPE_NAME
TELEOPERATION_TYPE_NAME = TeleoperationConstants.TYPE_NAME

# TODO remove this
TEST_TYPE_NAME = CommonTypeConstants.TYPE_NAME

TYPES_AVAILABLE = [
    NAV_TO_POINT_TYPE_NAME,
    AUTOMATIC_DOOR_TYPE_NAME,
    TELEOPERATION_TYPE_NAME,
    TEST_TYPE_NAME,
]
