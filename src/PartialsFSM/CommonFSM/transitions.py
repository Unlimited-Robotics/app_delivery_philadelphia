import typing

from raya.tools.fsm import BaseTransitions

if typing.TYPE_CHECKING:
    from src.app import RayaApplication

from .helpers import CommonHelpers


class CommonTransitions(BaseTransitions):

    def __init__(self, app: 'RayaApplication', helpers: CommonHelpers):
        super().__init__()
        self.app = app
        self.helpers = helpers
        self.log = self.helpers.get_logger()


    async def SETUP(self):
        self.log.debug('Transition SETUP')
        self.set_state('END')

    
    async def END(self):
        # this will not be executed, the FSM finished as soon the END state is reached
        self.log.debug('Transition END')
