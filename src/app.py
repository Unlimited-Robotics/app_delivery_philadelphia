import json

from raya.application_base import RayaApplicationBase
from raya.controllers.navigation_controller import NavigationController
from raya.controllers.leds_controller import LedsController
from raya.controllers.sound_controller import SoundController
from raya.controllers.ui_controller import UIController
from raya.controllers.fleet_controller import FleetController
from raya.controllers.sensors_controller import SensorsController
from raya.controllers.motion_controller import MotionController
from raya.controllers.cameras_controller import CamerasController
from raya.controllers.cv_controller import CVController

from raya.enumerations import FLEET_FINISH_STATUS
from raya.exceptions import RayaSkillAborted
from raya.tools.fsm import RayaFSMAborted
from src.FMSs.main import MainFSM
from src.static import *

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
        self.motion:MotionController = \
                await self.enable_controller('motion')
        self.cameras: CamerasController = \
                await self.enable_controller('cameras')
        self.cv: CVController = await self.enable_controller('cv')
    
        if not self.continue_cart:
            await self.set_gary_footprint(footprint=GARY_FOOTPRINT)
        else:
            await self.set_gary_footprint(footprint=GARY_SELECTED_CART_FOOTPRINT)
        
        self.log.debug('Enabling cameras')
        for camera in CAMERAS_DETECTING_DOOR:
            await self.cameras.enable_camera(camera_name=camera)

        # TODO: Chest disabled
        # self.sensors.create_threshold_listener(
        #     listener_name='chest_button',
        #     callback_async=self.cb_chest_button,
        #     sensors_paths=CHEST_LISTENER_PATHS,
        #     lower_bound=LOWER_BOUNDS_CHEST_THRESHOLD
        # )
    
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

        # elevators
        self.current_floor_map_name = WAREHOUSE_FLOOR
        self.current_target_floor_map_name = None
        
        
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
        self.locations = []
        delivery_location_fake = "{'name': 'test_unit','x': 206, 'y': 532, 'angle': 0.07, 'user_id': '1b3b40d4-2cf0-4ea0-b484-11b7cb721f86', 'map_name': 'philly_hospital__basement2'}"
        cart_location_fake = "{'name': 'cart_4', 'x': 3574, 'y': 402, 'angle': -104, 'user_id': '1b3b40d4-2cf0-4ea0-b484-11b7cb721f86', 'map_name': 'philly_hospital__basement'}"
        
        max_packages = self.get_argument(
            '--max_packages',
            type=int,
            help='Number of packages to deliver',
            required=False,
            default=1
        )
        
        self.run_from_console = self.get_flag_argument(
            '--fake',
            help='If enabled it will run the app from the fleet'
        )
        
        self.continue_cart = self.get_flag_argument(
            '--cart',
            help='If enabled it will set start the app with the footprint of gary with cart attached'
        )
        
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
        
        # get locations
        for index in range(1, max_packages+1):
            if self.run_from_console:
                location = delivery_location_fake
            else:
                location = self.get_argument(
                    f'--location{index}',
                    type=str,
                    help=(
                        'Location to deliver the package(formated as json), '
                        f'ex : {delivery_location_fake}'
                    ),
                    required=False,
                    default='',
                )
            location = location.replace("\'", "\"")
            self.log.info(f'Location: {location}')
            if location != '':
                self.locations.append(json.loads(location))
        
        # get cart number
        if self.run_from_console:
            cart_location = cart_location_fake
        else:
            cart_location: str = self.get_argument(
                '--cart_location',
                type=str,
                help='Location of the cart to attach the packages',
                required=True,
            )
        cart_location = cart_location.replace("\'", "\"")
        self.cart_location = json.loads(cart_location)
        #TODO replace this, it should take the id from the fleet
        self.cart_number = '4'
        
        self.log.warn('App is running with there args:')
        self.log.warn(f'Cart location: {self.cart_location}')
        for location in zip(self.locations):
            self.log.warn(f'\tLocation: {location}')


    async def set_gary_footprint(self, footprint):
        self.log.info(f'Setting robot footprint')
        await self.nav.update_robot_footprint(
            points=footprint
        )
        self.log.info('Robot footprint updated')


    async def cb_chest_button(self):
        self.log.warn('Chest button pressed')
        await self.sound.play_sound(name='success', wait=True)


    async def custom_cancel_sound(self):
        try:
            await self.sound.cancel_all_sounds()
        except Exception:
            pass


    async def custome_turn_off_leds(self):
        try:
            await self.leds.turn_off_all()
        except Exception:
            pass


    def get_current_floor_map_name(self):
        return self.current_floor_map_name


    def get_complete_current_floor_map_name(self):
        floor = self.get_current_floor_map_name()
        return f'{NAV_WAREHOUSE_BUILDING_NAME}__{floor}'


    def get_current_target_floor_map_name(self):
        return self.current_target_floor_map_name
    
    
    def get_complete_target_floor_map_name(self):
        floor = self.get_current_target_floor_map_name()
        return f'{NAV_WAREHOUSE_BUILDING_NAME}__{floor}'


    def current_target_floor_reached(self):
        self.current_floor_map_name = self.current_target_floor_map_name
        self.current_target_floor_map_name = None

