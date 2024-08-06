import time

from typing import NoReturn, TYPE_CHECKING
if TYPE_CHECKING:
    from src.app import RayaApplication

from ..CommonFSM import CommonHelpers
from .constants import *
from .states import *

class Helpers(CommonHelpers):
    
    def __init__(self, app: 'RayaApplication'):
        super().__init__(app=app)
        
        self.__last_failed_state = ''
        self.__last_failed_state_counter = 1
        self.__max_tries = MAX_RETRY_COUNTER_REQUEST_FOR_HELP
        self._ui_response_wait_for_help = None


    def reset_retry_counter(self):
        self.__last_failed_state_counter = 1


    def max_retry_reached(self):
        counter = self.__last_failed_state_counter > self.__max_tries
        if counter:
            self.log.error((
                f'Maximum tries reached for state: '
                f'{self.__last_failed_state}'
            ))
        else:
            self.log.debug((
                f'current try: {self.__last_failed_state_counter} '
                f'of {self.__max_tries}'
            ))
        return counter


    def increase_retry_counter(self):
        self.__last_failed_state_counter += 1

        
    def __set_last_failed_state(self, state: str):
        if self.__last_failed_state != state:
            self.reset_retry_counter()
        self.__last_failed_state = state


    def _get_last_failed_state(self):
        return self.__last_failed_state


    def retry_step(self,
            transitions,
            last_state:str = '',
            max_tries: int = MAX_RETRY_COUNTER_REQUEST_FOR_HELP,
            timeout: float = TIMEOUT_TELEOPERATOR,
        ) -> NoReturn:
        self.__max_tries = max_tries
        self.timeout_teleoperator = timeout
        if last_state != '':
            self.__set_last_failed_state(last_state)
        transitions.set_state(INITIAL_STATE)


    async def display_choice_selector_callback(self, data):
        self.log.debug(f'display_choice_selector_callback: {data}')
        self._ui_response_wait_for_help = data


    def start_timer_teleoperator(self):
        self._start_time = time.time()


    def check_teleoperator_timeout(self):
        if self.timeout_teleoperator < 0:
            return False
        return time.time() - self._start_time > self.timeout_teleoperator
