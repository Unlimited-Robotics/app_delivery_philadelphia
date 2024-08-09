from ..Point import Point
from . import AutomaticDoorFSM

from .constants import *


class AutomaticDoor:
    
    def __init__(self,
            name: str,
            zone_name: str,
            after_door_point: dict,
            tags_ids: list,
            tags_sizes: list,
            tags_family: str = '36h11',
            timeout: float = 60.0
        ) -> None:
        self.name = name
        self.zone_name = zone_name
        self.after_door_point: Point = Point(**after_door_point)
        self.tags_ids = tags_ids
        self.tags_family = tags_family
        self.tags_sizes = tags_sizes
        self.timeout = timeout
        
        self._door_tags = dict()
        self._door_tags[f'tag{self.tags_family}'] = self.tags_ids
        
        self._door_tags_model = {
            'families' : f'tag{self.tags_family}',
            'nthreads' : 4,
            'quad_decimate' : 2.0,
            'quad_sigma': 0.0,
            'decode_sharpening' : 0.25,
            'refine_edges' : 1,
            # TODO: check if the detector allows tags of different sizes
            'tag_size' : self.tags_sizes[0],
        }
        
        self._model = dict()
        self._model['name'] = 'apriltags'
        self._model['model_params'] = self._door_tags_model
        
        self.fsm = AutomaticDoorFSM(
            self_object=self,
            name=self.name, 
            log_transitions=True,
        )
