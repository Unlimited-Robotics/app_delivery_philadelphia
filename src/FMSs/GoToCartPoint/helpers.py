from src.app import RayaApplication

class Helpers:

    def __init__(self, app: RayaApplication):        
        self.app = app


    async def check_if_inside_zone(self):
        return await self.app.nav.is_in_zone(zone_name='warehouse')


    async def check_for_chest_button(self):
        sensors_data = self.app.sensors.get_all_sensors_values()
        button_chest = sensors_data['chest_button']
        if button_chest!=0:
            await self.app.sound.play_sound(name='success', wait=True)
            return True
        return False


    async def nav_feedback_async(self, code, msg, distance_to_goal, speed):
        if code == 9:
            self.app.log.debug('Obstacle detected')
            await self.app.sound.play_sound(name='error', wait=True)
            
        self.app.log.debug(
            f'nav_feedback_async: {code}, {msg}, {distance_to_goal}, {speed}'
        )


    async def nav_feedback_door_async(self, code, msg, distance, speed):
        if code == 9:
            self.app.log.debug('Obstacle detected, the door is closed')
            await self.app.sound.play_sound(name='error', wait=True)
            await self.app.nav.cancel_navigation()
        self.app.log.debug(
            'nav_feedback_door_async: '
            f'{code}, {msg}, {distance}, {speed}'
        )

        
    async def nav_finish_async(self, code, msg):
        self.app.log.debug(
            f'nav_finish_async: {code}, {msg}'
        )
