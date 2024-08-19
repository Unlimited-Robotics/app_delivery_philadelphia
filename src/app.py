from copy import deepcopy
import json

from raya.application_base import RayaApplicationBase
from raya.controllers.navigation_controller import NavigationController
from raya.controllers.leds_controller import LedsController
from raya.controllers.sound_controller import SoundController
from raya.controllers.ui_controller import UIController
from raya.controllers.fleet_controller import FleetController
from raya.controllers.motion_controller import MotionController
from raya.controllers.cameras_controller import CamerasController
from raya.controllers.cv_controller import CVController
from raya.controllers.robot_skills_controller import RobotSkillsController

from raya.enumerations import FLEET_FINISH_STATUS
from raya.exceptions import RayaSkillAborted
from raya.tools.fsm import RayaFSMAborted
from raya.utils.internal_filesystem import resolve_path
from src.FMSs.main import MainFSM
from src.static import *
from src.static.app_errors import AppError

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
        self.motion:MotionController = \
                await self.enable_controller('motion')
        self.cameras: CamerasController = \
                await self.enable_controller('cameras')
        self.cv: CVController = \
                await self.enable_controller('cv')
        self.robot_skills: RobotSkillsController = \
                await self.enable_controller('robot_skills')
        
        await self.ui.show_animation(**UI_SCREEN_NAVIGATING)
    
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

        # await self.fleet.finish_task(
        #         result=FLEET_FINISH_STATUS.FAILED,
        #         message='Hola Elisha'
        #     )
        
        # self.finish_app()
        
        
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
            # floor2
            "{'name': 'CICU',           'map_name': 'Main__Floor 02' , 'user_id': '1b3b40d4-2cf0-4ea0-b484-11b7cb721f86' }", 
            "{'name': 'MRICU HIGH',     'map_name': 'Main__Floor 02' , 'user_id': '1b3b40d4-2cf0-4ea0-b484-11b7cb721f86' }", 
            "{'name': 'MICU',           'map_name': 'Main__Floor 02' , 'user_id': '1b3b40d4-2cf0-4ea0-b484-11b7cb721f86' }", 
            "{'name': 'MRICU ELBOW',    'map_name': 'Main__Floor 02' , 'user_id': '1b3b40d4-2cf0-4ea0-b484-11b7cb721f86' }", 
            
            # floor4            
            "{'name': 'BURN',  'map_name': 'Main__Floor 04' , 'user_id': '1b3b40d4-2cf0-4ea0-b484-11b7cb721f86' }", 
            "{'name': '4E',    'map_name': 'Main__Floor 04' , 'user_id': '1b3b40d4-2cf0-4ea0-b484-11b7cb721f86' }", 
            "{'name': '4W',    'map_name': 'Main__Floor 04' , 'user_id': '1b3b40d4-2cf0-4ea0-b484-11b7cb721f86' }", 

            # # floor5
            "{'name': '5E',    'map_name': 'Main__Floor 05' , 'user_id': '1b3b40d4-2cf0-4ea0-b484-11b7cb721f86' }", 
            "{'name': '5W',    'map_name': 'Main__Floor 05' , 'user_id': '1b3b40d4-2cf0-4ea0-b484-11b7cb721f86' }", 

            # floor6
            "{'name': '6E',    'map_name': 'Main__Floor 06' , 'user_id': '1b3b40d4-2cf0-4ea0-b484-11b7cb721f86' }", 
            "{'name': '6W',    'map_name': 'Main__Floor 06' , 'user_id': '1b3b40d4-2cf0-4ea0-b484-11b7cb721f86' }", 
            
            # floor7
            "{'name': '7E',      'map_name': 'Main__Floor 07' , 'user_id': '1b3b40d4-2cf0-4ea0-b484-11b7cb721f86' }", 
            "{'name': '7W',      'map_name': 'Main__Floor 07' , 'user_id': '1b3b40d4-2cf0-4ea0-b484-11b7cb721f86' }", 
        
            # floor8
            "{'name': '8W',    'map_name': 'Main__Floor 08' , 'user_id': '1b3b40d4-2cf0-4ea0-b484-11b7cb721f86' }", 
            "{'name': '8E',    'map_name': 'Main__Floor 08' , 'user_id': '1b3b40d4-2cf0-4ea0-b484-11b7cb721f86' }", 

            # floor9
            "{'name': '9E',    'map_name': 'Main__Floor 09' , 'user_id': '1b3b40d4-2cf0-4ea0-b484-11b7cb721f86' }", 
            "{'name': '9W',    'map_name': 'Main__Floor 09' , 'user_id': '1b3b40d4-2cf0-4ea0-b484-11b7cb721f86' }", 
        ]
        park_location_fake = "{'name': 'Parking A', 'user_id': '1b3b40d4-2cf0-4ea0-b484-11b7cb721f86', 'map_name': 'Main__Basement'}"
        
        start_delivery_index = self.get_argument(
            '--index',
            type=int,
            required=False,
            default=1
        )
        
        max_packages = self.get_argument(
            '--max_packages',
            type=str,
            help='Number of packages to deliver',
            required=False,
            default='18'
        )
        max_packages = int(max_packages)
        
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
        self.continue_with_cart_footprint = True
        
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
            default='home_elev'
        )
        
        self.default_last_package = self.get_argument(
            '--last_unit_visited',
            type=str,
            required=False,
            default='elev'
        )
        
        # get locations
        for index in range(start_delivery_index, max_packages+1):
            try:
                if self.run_from_console:
                    location = delivery_location_fake[index-1]
                else:
                    location = self.get_argument(
                        f'--location{index}',
                        type=str,
                        help=(
                            'Location to deliver the package(formated as json), '
                        ),
                        required=False,
                        default='',
                    )
                
                location = location.replace("\'", "\"")
                if location != '':
                    location = json.loads(location)
                    if location['map_name'] == 'Main__Basement':
                        return
                    self.replace_map_name(location=location)
                    floor_number = location['map_name'].split('__')[-1]
                    unit_to_internal = {value: key for key, value in FLOORS[floor_number]['units'].items()}
                    try:
                        location['unit_internal_name'] = unit_to_internal[location['name']]
                    except KeyError:
                        location['unit_internal_name'] = '__'
                    self.locations.append(location)
                    
            except IndexError:
                self.log.error(f'Index {index} out of range')
                break

        # Order points
        order = {}
        for index, item in enumerate(self.locations):
            if item["map_name"] not in order:
                order[item["map_name"]] = index
        seen = set()
        sorted_data = []
        for item in sorted(self.locations, key=lambda x: (order[x["map_name"]], x["unit_internal_name"])):
            identifier = (item["map_name"], item["unit_internal_name"])
            if identifier not in seen:
                seen.add(identifier)
                sorted_data.append(item)
        self.locations = sorted_data
        
        # get cart number
        if self.run_from_console:
            self.selected_parking = park_location_fake
        else:
            self.selected_parking: str = self.get_argument(
                '--target_goal',
                type=str,
                help='Parking spot of the robot',
                required=True,
            )

        # format selected parking
        self.selected_parking = self.selected_parking.replace("\'", "\"")
        self.selected_parking = json.loads(self.selected_parking)
        self.selected_parking['name'] = self.selected_parking['name'].split(' ')[1]
        
        # show info about the app
        self.log.warn('App is running with there args:')
        self.log.warn(f'Selected parking: {self.selected_parking}')
        for location in zip(self.locations):
            self.log.warn(f'\tLocation: {location}')


    def replace_map_name(self, location):
        _ , floor = location['map_name'].split('__')
        _, floor_number = floor.split(' ')
        location['map_name'] = f'{NAV_MAP_NAME}__{floor_number}'


    async def set_gary_footprint(self, footprint):
        self.log.info(f'Setting robot footprint')
        await self.nav.update_robot_footprint(
            points=footprint
        )
        self.log.info('Robot footprint updated')


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


    def get_unit_name(self, package_point_name, floor = ''):
        current_floor = floor
        if floor == '':
            current_floor = self.get_current_floor_map_name()
        
        self.log.debug((
            f'Replacing name of unit \'{package_point_name}\' '
            f'on floor \'{current_floor}\'.'
        ))

        try:
            units = FLOORS[current_floor]['units']
            key_unit_list = list(units.keys())
            val_unit_list = list(units.values())
            
            position = val_unit_list.index(package_point_name)
            alias_name = key_unit_list[position]
            self.log.debug((
                f'The unit name \'{package_point_name}\' is the unit alias '
                f'\'{alias_name}\' of the floor \'{current_floor}\''
            ))
            return alias_name
        except Exception as e:
            self.log.error((
                f'Error getting the get_current_unit: {package_point_name}'
            ))
            return 'elev'


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


    async def show_navigating_to_floor(self):
        copy_ui_screen = deepcopy(UI_SCREEN_NAV_TO_FLOOR)
        floor = self.get_current_target_floor_map_name()
        
        if floor == WAREHOUSE_FLOOR:
            message = 'On My Way Home'
        else:
            message = copy_ui_screen['title'].replace(
                '[floor]', floor
            )

        copy_ui_screen['title'] = message
        await self.ui.show_animation(**copy_ui_screen)


    def convert_image_to_base64(self, image_path):
        import base64
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        return encoded_string.decode('utf-8')


    def delivery_options(self):
        screen = deepcopy(UI_SCREEN_OPTIONS_DELIVERY_ARRIVED)
        
        for option in screen['data']:
            option['imgSrc'] = f'data:image/png;base64, \
                {self.convert_image_to_base64(resolve_path(option["imgSrc"]))}'
        return screen
