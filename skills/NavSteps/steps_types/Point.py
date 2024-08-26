from raya.enumerations import POSITION_UNIT, ANGLE_UNIT

class Point:
    
    def __init__(self, *args, **kwargs) -> None:
        self.x: float = float(args[0] if args else kwargs.pop('x'))
        self.y: float = float(args[1] if args else kwargs.pop('y'))
        self.angle: float = float(args[2] if args else kwargs.pop('angle'))
        self.ang_unit: ANGLE_UNIT = \
            kwargs.pop('ang_unit', ANGLE_UNIT.RADIANS)
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
