from app.core.interfaces import LocationService
from app.utils import schemas
from app.utils.logger import get_logger

logger = get_logger(__name__)


class NavigationMap:
    """
    Class maintains a navigation map.

    It is a singleton to guarantee all vehciles locations are consistant.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(NavigationMap, cls).__new__(cls)
            return cls._instance

        raise ValueError("Can't instantiate a new Map")

    def __init__(
            self,
            map_size: schemas.MapSize
            ) -> None:
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


class BasicLocationService(LocationService):
    """Class responsible for tracking vehicle location and maintaining
    nevigatin map.
    """
    def __init__(
            self,
            nav_map: NavigationMap,
            current_location: schemas.Location = schemas.Location(x=1, y=1),
            ) -> None:
        self.nav_map: NavigationMap = nav_map
        self._current_location: schemas.Location = current_location

    @property
    def nav_map(self):
        return self._nav_map

    @nav_map.setter
    def nav_map(self, nav_map: NavigationMap):
        self._nav_map = nav_map

    @property
    def current_location(self):
        return self._current_location

    @current_location.setter
    def current_location(self, location: schemas.Location):
        self._current_location = location

    def override_current_location(self, location: schemas.Location) -> None:
        """Helper method to redefine location of a vehicle"""
        self.current_location = location
        logger.warning("Location overriden to %s", str(location))

    def update_location(self, shift: schemas.Shift) -> None:
        """Updates a vehicle location given vehicle shift"""
        new_location = schemas.Location(
            x=self.current_location.x + shift.x,
            y=self.current_location.y + shift.y
        )
        self.current_location = new_location
        logger.info("Vehicle moved to %s", self.current_location)
