import typing
if typing.TYPE_CHECKING:
    from src.app import RayaApplication
    from . import CommonFSM

from raya.logger import RaYaLogger
from raya.exceptions import RayaCommandAlreadyRunning, RayaFileDoesNotExist, RayaCommandTimeout

from .constants import DELAY_BEETWEEN_SOUND_LOOP, LEDS_GARY_SPEAKING


class CommonHelpers():
    
    def __init__(self, app: 'RayaApplication'):
        self.app = app
        self._fsm: CommonFSM
        self.log: RaYaLogger


    def __setattr__(self, name, value):
        if name == '_fsm':
            super().__setattr__(name, value)
            if value is not None:
                self._log = value
        else:
            super().__setattr__(name, value)


    def get_logger(self) -> RaYaLogger:
        return self._fsm.log
    

    @property
    def log(self):
        return self.get_logger()


    async def custom_cancel_sound(self):
        try:
            await self.app.sound.cancel_all_sounds()
        except Exception:
            pass


    async def custom_animation(self, wait=True, **kwargs):
        try:
            await self.app.leds.animation(**kwargs, wait=wait)
        except Exception:
            pass


    async def custom_turn_off_leds(self, group = ''):
        if group != '':
            try:
                await self.app.leds.turn_off_group(group)
            except Exception:
                pass
        else:
            try:
                await self.app.leds.turn_off_all()
            except Exception:
                pass


    def sound_finish_callback(self, code, msg):
        pass

    
    async def gary_play_audio(self, 
            audio: dict, 
            animation_head_leds: dict = LEDS_GARY_SPEAKING,
            wait: bool = False
        ):
        try:
            if not self.app.sound.is_playing():
                await self.custom_turn_off_leds(group='head')
                await self.app.sleep(DELAY_BEETWEEN_SOUND_LOOP)
                await self.app.sound.play_sound(
                    **audio,
                    wait=False,
                    callback_finish=self.sound_finish_callback
                )
                await self.custom_animation(
                    **animation_head_leds, 
                    wait=False
                )
            if wait:
                await self.custom_animation(
                    **animation_head_leds, 
                    wait=False
                )
                while self.app.sound.is_playing():
                    await self.app.sleep(0.5)
                await self.custom_turn_off_leds(group='head')
        except RayaFileDoesNotExist:
            self.log.error(
                f'Audio file \'{audio}\' not found'
            )
        except RayaCommandAlreadyRunning:
            pass
        except RayaCommandTimeout:
            pass
