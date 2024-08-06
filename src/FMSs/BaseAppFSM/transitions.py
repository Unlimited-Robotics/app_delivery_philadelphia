from src.PartialsFSM.RetryState import Transitions as RetryTransitions

from src.static import *
from .helpers import CommonHelpers
from src.FMSs.main.errors import *


class CommonTransitions(RetryTransitions):

    def __init__(self, app, helpers: CommonHelpers):
        super().__init__(app=app, helpers=helpers)
        self.helpers: CommonHelpers
