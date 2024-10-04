from app.utils import (
    schemas,
    )
from app.utils.logger import get_logger

logger = get_logger(__name__)


class NavigationMap:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(NavigationMap, cls).__new__(cls)
            return cls._instance

        raise ValueError("Can't instantiate a new Map")

    def __init__(
            self,
            map_size: schemas.MapSize
            ):
        self._x_size = map_size.x_size
        self._y_size = map_size.y_size

    @property
    def x_size(self):
        return self._x_size

    @x_size.setter
    def x_size(self, value):
        raise AttributeError(f"Can't redefine `x_size` to {value} "
                             "as it is an immutable property of Map")

    @property
    def y_size(self):
        return self._y_size

    @y_size.setter
    def y_size(self, value):
        raise AttributeError(f"Can't redefine `y_size` to {value} "
                             "as it is an immutable property of Map")


