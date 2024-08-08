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
from raya.controllers.robot_skills_controller import RobotSkillsController

from raya.enumerations import FLEET_FINISH_STATUS
from raya.exceptions import RayaSkillAborted
from raya.tools.fsm import RayaFSMAborted
from src.FMSs.main import MainFSM
from src.static import *

from skills.NavSteps import SkillNavSteps
from skills.attach_to_cart import SkillAttachToCart, SkillDetachCart

from raya.exceptions import *

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
        self.cv: CVController = \
                await self.enable_controller('cv')
        self.robot_skills: RobotSkillsController = \
                await self.enable_controller('robot_skills')
    
        if not self.continue_with_cart_footprint:
            await self.set_gary_footprint(footprint=GARY_FOOTPRINT)
        else:
            await self.set_gary_footprint(footprint=GARY_SELECTED_CART_FOOTPRINT)

        if self.set_costmap:
            initial_point , final_point = self.set_costmap.split('_')
            await self.change_costmap_to_point(
                initial_point=initial_point,
                final_point=final_point,
            )
        
        # FSMs
        self.fsm_main_task = MainFSM(
                log_transitions=True,
            )

        # Skills
        self.skill_nav_steps = self.register_skill(SkillNavSteps)
        setup_args = {}
        result = await self.skill_nav_steps.execute_setup(
            setup_args=setup_args
        )
        self.log.warn(f'setup skill_nav_steps result: {result}')
        
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
            self.log.debug(f'Attach skill setup result: {result}')
            
            self.log.debug('Registering detach skill')
            self.skill_detach = self.register_skill(SkillDetachCart)
            self.log.debug('Executing setup for detach skill')
            result = await self.skill_detach.execute_setup(
                setup_args=SETUP_ARG_DETACH_SKILL,
                wait=True
            )
            self.log.debug(f'Detach skill setup result: {result}')

        # elevators
        self.current_floor_map_name = self.current_floor
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
        delivery_location_fake = [
            # "{'name': '7E',  'x': 1027, 'y': 593, 'angle': 13.75, 'user_id': '1b3b40d4-2cf0-4ea0-b484-11b7cb721f86', 'map_name': 'phillytemplehosp_v2__07'}", 
            # "{'name': '7W',  'x': 1642, 'y': 2266, 'angle': 15.47, 'user_id': '1b3b40d4-2cf0-4ea0-b484-11b7cb721f86', 'map_name': 'phillytemplehosp_v2__07'}", 

            "{'name': 'unit1',  'x': 519,   'y': 573,    'angle': 92.94,    'user_id': '1b3b40d4-2cf0-4ea0-b484-11b7cb721f86',      'map_name': 'phillytemplehosp_v2__02'}", 
            "{'name': 'unit2',  'x': 1895,  'y': 282,    'angle': 93.58,    'user_id': '1b3b40d4-2cf0-4ea0-b484-11b7cb721f86',      'map_name': 'phillytemplehosp_v2__02'}", 
            "{'name': 'unit3',  'x': 2063,  'y': 1027,   'angle': -106.31,  'user_id': '1b3b40d4-2cf0-4ea0-b484-11b7cb721f86',      'map_name': 'phillytemplehosp_v2__02'}", 
            "{'name': 'unit4',  'x': 3510,  'y': 1208,   'angle': -105.04,  'user_id': '1b3b40d4-2cf0-4ea0-b484-11b7cb721f86',      'map_name': 'phillytemplehosp_v2__02'}", 
        ]
        cart_location_fake = "{'name': 'cart_4', 'x': 289, 'y': 1271, 'angle': 102, 'user_id': '1b3b40d4-2cf0-4ea0-b484-11b7cb721f86', 'map_name': 'phillytemplehosp_v2__00'}"
        
        start_delivery_index = self.get_argument(
            '--index',
            type=int,
            required=False,
            default=1
        )
        
        max_packages = self.get_argument(
            '--max_packages',
            type=int,
            help='Number of packages to deliver',
            required=False,
            default=1
        )
        
        self.current_floor = self.get_argument(
            '--floor',
            type=str,
            help='Current floor of the robot',
            required=False,
            default=WAREHOUSE_FLOOR    
        )
        
        self.run_from_console = self.get_flag_argument(
            '--fake',
            help='If enabled it will run the app from the fleet'
        )
        
        self.continue_with_cart_footprint = self.get_flag_argument(
            '--cart_footprint',
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
        
        self.set_costmap = self.get_argument(
            '--costmap',
            type=str,
            required=False,
            default=None
        )
        
        # get locations
        for index in range(start_delivery_index, max_packages+1):
            if self.run_from_console:
                location = delivery_location_fake[index-1]
            else:
                location = self.get_argument(
                    f'--location{index}',
                    type=str,
                    help=(
                        'Location to deliver the package(formated as json), '
                        f'ex : {delivery_location_fake[index-1]}'
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
        self.cart_number = self.cart_location['name'].split('_')[1]
        self.log.debug(f'Cart location: {self.cart_number}')
        
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


    def get_current_floor_map_name(self):
        return self.current_floor_map_name


    def get_complete_current_floor_map_name(self):
        floor = self.get_current_floor_map_name()
        return f'{NAV_MAP_NAME}__{floor}'


    def get_current_target_floor_map_name(self):
        return self.current_target_floor_map_name
    
    
    def get_complete_target_floor_map_name(self):
        floor = self.get_current_target_floor_map_name()
        return f'{NAV_MAP_NAME}__{floor}'


    def current_target_floor_reached(self):
        self.log.info((
            f'Floor \'{self.current_target_floor_map_name}\' reached.'
        ))
        self.current_floor_map_name = self.current_target_floor_map_name
        self.current_target_floor_map_name = None


    def get_current_unit(self, current_package):
        current_floor = self.get_current_floor_map_name()
        
        if COST_MAPS_CONFIG['unit_identifier'] in current_package:
            try:
                units = FLOORS[current_floor]['units']
                key_unit_list = list(units.keys())
                val_unit_list = list(units.values())
                
                position = val_unit_list.index(current_package)
                final_name = key_unit_list[position]
                return final_name
            except Exception as e:
                self.log.error((
                    f'Error getting the get_current_unit: {current_package}'
                ))
                # TODO fix this
                return 'elev'
        return current_package

    async def change_costmap_to_point(self, initial_point, final_point):
        initial_name = initial_point
        final_name = final_point
        default_costmap_name = 'map'
        try:
            format = COST_MAPS_CONFIG['costmap_format']
            costmap_name = format.replace('[initial_point]', initial_name)
            costmap_name = costmap_name.replace('[final_point]', final_name)
            await self.nav.change_costmap(costmap_name=costmap_name)
            self.log.debug((
                f'Costmap changed to: {costmap_name}, '
                f'initial_point: {initial_point}, '
                f'final_point: {final_point}'
            ))
        except RayaNavFileNotFound:
            self.log.error((
                f'Costmap file \'{costmap_name}\' not found, '
                f'setting default costmap \'{default_costmap_name}\''
            ))
            try:
                await self.nav.change_costmap(
                    costmap_name=default_costmap_name
                )
            except RayaCommandTimeout:
                self.log.error(f'Costmap change timeout')
        except RayaCommandTimeout:
            self.log.error(f'Costmap change timeout')
