from raya.enumerations import POSITION_UNIT, ANGLE_UNIT

class Point:
    
    def __init__(self, **kwargs) -> None:
        self.x: float = \
            kwargs.pop('x')
        self.y: float = \
            kwargs.pop('y')
        self.angle: float = \
            kwargs.pop('angle')
        self.ang_unit: ANGLE_UNIT = \
            kwargs.pop('ang_unit', ANGLE_UNIT.DEGREES)
        self.pos_unit: POSITION_UNIT = \
            kwargs.pop('pos_unit', POSITION_UNIT.PIXELS)

        self.nav_options = kwargs


    def to_dict(self) -> dict:
        return {
            'x': self.x,
            'y': self.y,
            'angle': self.angle,
            'ang_unit': self.ang_unit,
            'pos_unit': self.pos_unit,
            **self.nav_options
        }


    def get_only_coordinates(self) -> dict:
        return {
            'x': self.x,
            'y': self.y,
            'angle': self.angle,
            'ang_unit': self.ang_unit,
            'pos_unit': self.pos_unit,
        }
