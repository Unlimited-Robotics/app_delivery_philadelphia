from src.FMSs.TakeCart.helpers import Helpers as ParkCartHelpers
from src.app import RayaApplication


class Helpers(ParkCartHelpers):

    def __init__(self, app: RayaApplication):     
        super().__init__(app)
