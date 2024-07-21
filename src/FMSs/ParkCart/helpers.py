from __future__ import annotations

from src.app import RayaApplication
from src.FMSs.GoToCartPoint.helpers import Helpers as ParkCartHelpers


class Helpers(ParkCartHelpers):

    def __init__(self, app: RayaApplication):
        super().__init__(app)
