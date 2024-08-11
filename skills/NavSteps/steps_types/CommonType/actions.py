import typing
if typing.TYPE_CHECKING:
    from src.app import RayaApplication

from ...PartialsFSM.CommonFSM import CommonActions
from .helpers import Helpers


class Actions(CommonActions):

    def __init__(self, app: 'RayaApplication', helpers: Helpers):
        super().__init__(app=app, helpers=helpers)
