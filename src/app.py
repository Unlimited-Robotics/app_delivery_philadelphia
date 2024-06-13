from raya.application_base import RayaApplicationBase
from raya.controllers.navigation_controller import NavigationController
from raya.controllers.leds_controller import LedsController
from raya.controllers.sound_controller import SoundController
from raya.controllers.ui_controller import UIController
from raya.controllers.fleet_controller import FleetController
from raya.controllers.sensors_controller import SensorsController

from raya.enumerations import FLEET_FINISH_STATUS
from raya.tools.fsm import RayaFSMAborted
from src.FMSs.main import MainFSM
from src.static.skills import SETUP_ARG_ATTACH_SKILL, SETUP_ARG_DETACH_SKILL

from skills.attach_to_cart import SkillAttachToCart, SkillDetachCart

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


        self.skill_att2cart = None
        self.skill_detach = None
        if self.enable_attach:
            self.log.info('Attaching and detaching skills enabled')
            
            self.log.info('Registering attach skill')
            self.skill_att2cart = self.register_skill(SkillAttachToCart)
            self.log.info('Executing setup for attach skill')
            result = await self.skill_att2cart.execute_setup(
                setup_args=SETUP_ARG_ATTACH_SKILL,
                wait=True
            )
            self.log.info(f'Attach skill setup result: {result}')
            
            self.log.info('Registering detach skill')
            self.skill_detach = self.register_skill(SkillDetachCart)
            self.log.info('Executing setup for detach skill')
            result = await self.skill_detach.execute_setup(
                setup_args=SETUP_ARG_DETACH_SKILL,
                wait=True
            )
            self.log.info(f'Detach skill setup result: {result}')


    async def main(self):
        try:
            await self.fsm_main_task.run_and_await()
            await self.fleet.finish_task(
                result=FLEET_FINISH_STATUS.SUCCESS,
                message='Task finished successfully'
            )
        except RayaFSMAborted as e:
            await self.fleet.finish_task(
                result=FLEET_FINISH_STATUS.FAILED,
                message=(
                    'Fsm Aborted with error '
                    f'[{e.error_code}]: {e.error_msg}'
                )
            )
            self.log.error(
                f'Fsm Aborted with error [{e.error_code}]: {e.error_msg}'
            )


    async def finish(self):
        self.log.info('App finished')
        await self.sleep(5)

    
    def get_arguments(self):
        max_packages = 2
        self.locations = []
        
        self.enable_attach = self.get_argument(
            '--enable_attach',
            type=bool,
            help=(
                'Enable attach the cart packages to the robot otherwhise '
                'the robot will wait for the chest to be pressed.'
            ),
            required=False,
            default=True,
        )
        
        for index in range(1, max_packages+1):
            location = self.get_argument(
                f'--location{index}',
                type=str,
                help=('Location to deliver the packages, '
                    f'ex: --location{index} '
                    f'"[381, 655, 1.57, \'point{index}\']"'
                ),
                required=False,
                default='',
            )
            self.log.info(f'Location: {location}')
            if location != '':
                self.log.warn(f'locations:{location}')
                location = location.strip('[]')
                location = location.split(',')
                location_coordinates = [float(axys.strip()) for axys in location[:3]]\

                location_name = location[3].strip() if len(location) > 3 else ''
                location_map = location[4].strip() if len(location) > 4 else ''
                location_coordinates.append(location_name)
                location_coordinates.append(location_map)

                self.locations.append(location_coordinates)
        self.locations = [[565.0, 218.0, 0.0]]
        self.log.info('App is running with there args:')
        for location in zip(self.locations):
            self.log.info(f'\tLocation: {location}')
