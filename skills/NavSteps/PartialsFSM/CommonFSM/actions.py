import typing
if typing.TYPE_CHECKING:
    from src.app import RayaApplication

from raya.tools.fsm import BaseActions

from .helpers import CommonHelpers


class CommonActions(BaseActions):

    def __init__(self, app: 'RayaApplication', helpers: CommonHelpers):
        super().__init__()
        self.app = app
        self.helpers = helpers
        self.log = self.helpers.get_logger()
    
    
    async def aborted(self, error, msg):
        pass