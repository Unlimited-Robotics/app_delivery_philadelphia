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
            range_degrees_tag_visible: int = RANGE_DEGREES_TAG_VISIBLE,
            
            timeout: float = 60.0,
            custom_ui_screen: dict = UI_SCREEN_WAIT_FOR_DOOR_OPEN,
            phone_call_timeout: float = -1.0,
            phone_call_user_id: str = None,
            door_tag_timeout: float = DOOR_TAG_TIMEOUT,
            
            delay_after_door_opened: float = DELAY_AFTER_DOOR_OPENED,
            fleet_call_message: str = FLEET_CALL_MESSAGE,
            door_close_timeout: float = DOOR_CLOSE_TIMEOUT,
            time_before_first_call: float = TIME_BEFORE_FIRST_CALL,
            time_beetween_calls: float = TIME_BEETWEEN_CALLS,
            
            sound_open_door_name: str = SOUND_OPEN_DOOR_NAME,
            sound_thanks_door_name: str = SOUND_THANKS_DOOR_NAME,
            leds_door_open_animation: str = LEDS_DOOR_OPEN_ANIMATION,
            
        ) -> None:
        self.name = name
        self.zone_name = zone_name
        self.after_door_point: Point = Point(**after_door_point)
        self.tags_ids = tags_ids
        self.tags_family = tags_family
        self.tags_sizes = tags_sizes
        self.range_degrees_tag_visible = range_degrees_tag_visible
        self.timeout = timeout
        self.custom_ui_screen = custom_ui_screen
        self.door_tag_timeout = door_tag_timeout
        
        self.phone_call_timeout = phone_call_timeout
        self.phone_call_user_id = phone_call_user_id
        self.delay_after_door_opened = delay_after_door_opened
        self.fleet_call_message = fleet_call_message
        self.door_close_timeout = door_close_timeout
        self.time_before_first_call = time_before_first_call
        self.time_beetween_calls = time_beetween_calls
        
        self.sound_open_door_name = sound_open_door_name
        self.sound_thanks_door_name = sound_thanks_door_name
        self.leds_door_open_animation = leds_door_open_animation
        
        self._door_tags = dict()
        self._door_tags[f'tag{self.tags_family}'] = self.tags_ids
        
        self._door_tags_model = {
            'families' : f'tag{self.tags_family}',
            'nthreads' : 4,
            'quad_decimate' : 2.0,
            'quad_sigma': 0.0,
            'decode_sharpening' : 0.25,
            'refine_edges' : 1,
            'tag_size' : self.tags_sizes[0],
        }
        
        self._model = dict()
        self._model['name'] = 'apriltags_cpp'
        self._model['model_params'] = self._door_tags_model
        
        self.fsm = AutomaticDoorFSM(
            self_object=self,
            name=self.name, 
            log_transitions=True,
        )
