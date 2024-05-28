from raya.application_base import RayaApplicationBase
from raya.controllers.navigation_controller import NavigationController
from raya.controllers.leds_controller import LedsController
from raya.controllers.sound_controller import SoundController
from raya.controllers.ui_controller import UIController
from raya.controllers.fleet_controller import FleetController
from raya.controllers.sensors_controller import SensorsController

from raya.exceptions import RayaArgumentError
from raya.tools.fsm import RayaFSMAborted
from src.FMSs.main import MainFSM

class RayaApplication(RayaApplicationBase):

    async def setup(self):
        # Controllers
        self.nav:NavigationController = \
                await self.enable_controller('navigation')
        self.leds:LedsController  = \
                await self.enable_controller('leds')
        self.sound:SoundController = \
                await self.enable_controller('sound')
        self.ui:UIController = \
                await self.enable_controller('ui')
        self.fleet:FleetController = \
                await self.enable_controller('fleet')
        self.sensors:SensorsController = \
                await self.enable_controller('sensors')
    
        # FSMs
        self.fsm_main_task = MainFSM(
                log_transitions=True,
            )


    async def main(self):
        return
        try:
            await self.fsm_main_task.run_and_await()
        except RayaFSMAborted as e:
            self.log.error(
                f'Fsm Aborted with error [{e.error_code}]: {e.error_msg}'
            )


    async def finish(self):
        self.log.info('App finished')

    
    def get_arguments(self):
        max_packages = 2
        self.locations = []
        self.floor = []
        
        for index in range(1, max_packages+1):
            location = self.get_argument(
                f'--location{index}',
                type=str,
                help=('Location to deliver the packages, '
                    f'ex: --location{index} '
                    '"[381, 655, 1.57, \'point{index}\']"'
                ),
                required=False,
                default='',
                list=True
            )
            floor = self.get_argument(
                f'--floor{index}',
                type=str,
                help=('Floor to deliver the packages, '
                    f'ex: --floor{index} ""'
                ),
                required=False,
                default='',
            )
            location_list = []
            for i, element in enumerate(location):
                element = element.strip().strip(',')
                if i == 0:
                    element = element.lstrip('[')
                if i == len(location) - 1:
                    element = element.rstrip(']')
                try:
                    location_list.append(float(element))
                except ValueError:
                    location_list.append(element)
            
            if floor != '':
                self.locations.append(location_list)
                self.floor.append(floor)
        
        self.log.info('App is running with there args:')
        self.log.info(f'\tLocations: {self.locations}')
        self.log.info(f'\tFloors: {self.floor}')
