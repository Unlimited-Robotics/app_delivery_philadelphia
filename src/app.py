from raya.application_base import RayaApplicationBase
from raya.controllers.navigation_controller import NavigationController
from raya.controllers.leds_controller import LedsController
from raya.controllers.sound_controller import SoundController
from raya.controllers.ui_controller import UIController
from raya.controllers.fleet_controller import FleetController
from raya.controllers.sensors_controller import SensorsController

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
        try:
            await self.fsm_main_task.run_and_await()
        except RayaFSMAborted as e:
            self.log.error(
                f'Fsm Aborted with error [{e.error_code}]: {e.error_msg}'
            )


    async def finish(self):
        self.log.info('App finished')

    
    def get_arguments(self):
        # TODO (Camilo): Change to --location1 X.X,X.X --floor1 basement ...
        n = 2
        self.locations = []
        self.floor = []
        
        for index in range(1, n+1):
            location = self.get_argument(
                f'--location{index}',
                type=str,
                help=('Location to deliver the packages, '
                      f'ex: --location{index} ""'
                ),
                required=True,
            )
            floor = self.get_argument(
                f'--floor{index}',
                type=str,
                help=('Floor to deliver the packages, '
                      f'ex: --floor{index} ""'
                ),
                required=True,
            )
            location = location.strip("()")
            location = list(map(float, location.split(",")))
            self.locations.append(location)
            self.floor.append(floor)
        
        self.log.info('App is running with there args:')
        self.log.info(f'\tLocations: {self.locations}')
        self.log.info(f'\tFloors: {self.floor}')
