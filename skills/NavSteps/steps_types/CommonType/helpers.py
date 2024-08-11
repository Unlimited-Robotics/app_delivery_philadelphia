import typing
if typing.TYPE_CHECKING:
    from src.app import RayaApplication

from raya.exceptions import *
from ...PartialsFSM.CommonFSM import CommonHelpers


class Helpers(CommonHelpers):

    def __init__(self, app: 'RayaApplication'):
        super().__init__(app)
