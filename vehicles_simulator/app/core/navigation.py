"""
Contains implementation of the BasicNavigationManager class and its 
dependency BasicNavigationManager
"""
import math
from typing import List
from app.core.heading import HeadingDirectionManager
from app.core.interfaces import (
    AllowedZoneManager,
    DestinationTracker,
    LocationService,
    MovementManager,
    NavigationManager,
)
from app.utils import (
    schemas,
    )
from app.utils.logger import get_logger


logger = get_logger(__name__)


class BasicNavigationManager(NavigationManager):
    """Manages communication and track state related to navigation"""
    def __init__(
            self,
            allowed_zone_manager: AllowedZoneManager,
            destination_tracker: DestinationTracker,
            heading_selector: HeadingDirectionManager,
            location_service: LocationService,
            movement_manager: MovementManager,
            ):

        self.allowed_zone_manager = allowed_zone_manager
        self.destination_tracker = destination_tracker
        self.heading_selector = heading_selector
        self.location_service = location_service
        self.movement_manager = movement_manager

    @property
    def current_direction(self):
        return self.movement_manager.current_direction.value

    @property
    def current_location(self):
        return self.location_service.current_location

    @property
    def current_speed(self):
        return self.movement_manager.current_speed

    @property
    def destination(self):
        return self.destination_tracker.destination

    @destination.setter
    def destination(self, location: schemas.Location):
        self.destination_tracker.destination = location

    @property
    def destination_reached(self):
        return self.destination_tracker.destination_reached

    @property
    def distance_to_destination(self):
        return self.destination_tracker.distance_to_destination

    @property
    def distance_until_turn_allowed(self):
        return self.movement_manager.distance_until_turn_allowed

    @property
    def out_of_zone(self):
        return self.allowed_zone_manager.out_of_zone

    def move_to_destination(self):
        """Main script to try to get to destination"""
        if self.destination_reached:
            logger.warning("Got `move` command while already at destination")
            self._update_statuses()
            return

        # try to turn if allowed
        if self.movement_manager.can_turn:
            logger.debug("Can turn: current speed: %s, distance to turn %s",
                         self.current_speed, self.distance_until_turn_allowed)
            self.heading_selector.update_heading_direction()
            self.movement_manager.turn(self.heading_selector.heading_direction)
        movement_shift = self.movement_manager.move()
        self.update_location(movement_shift)
        self._update_statuses()

    def initialize_new_task(self, destination: schemas.Location):
        """High level method that implements new task acceptance"""
        self.destination = destination
        self._update_statuses()

    def get_turn_direction(self):
        """Method to get heading direction. Relies on dependency."""
        self.heading_selector.update_heading_direction()
        return self.heading_selector.heading_direction

    def update_location(self, shift: schemas.Shift):
        """Method to uodate location and class statuses"""
        self.location_service.update_location(shift)
        self._update_statuses()

    def _update_statuses(self):
        """Implements statuss updates"""
        self.destination_tracker.update_state()
        self.allowed_zone_manager.update_state()


class BasicDestinationTracker(DestinationTracker):
    """Class responsible for tracking destination.

    Keeps track destination related telemetry:
    - distance to destination
    - if destination is reached

    Can get heading directions to destination.

    A destination is reached if vehicle is within defined range from
    destination.

    Class does not define destination. Instead it accepts setting of
    the destination from extrnal call. 
    No validations or destination definition applied.
    """
    def __init__(
            self,
            location_service: LocationService,
            destination_reached_threshold: int = 3,
            ):

        self.destination: schemas.Location = schemas.Location(x=0, y=0)
        self.destination_reached: bool = False
        self.destination_reached_threshold: int = destination_reached_threshold
        self.distance_to_destination: int = math.inf
        self.heading_directions: List[schemas.Direction] = []
        self.location_service: LocationService = location_service

    @property
    def destination(self) -> schemas.Location:
        return self._destination

    @destination.setter
    def destination(self, location: schemas.Location):
        self._destination = location

    @property
    def destination_reached(self) -> bool:
        return self._destination_reached

    @destination_reached.setter
    def destination_reached(self, value: bool) -> None:
        self._destination_reached = value

    @property
    def destination_reached_threshold(self) -> bool:
        return self._destination_reached_threshold

    @destination_reached_threshold.setter
    def destination_reached_threshold(self, status: bool) -> None:
        self._destination_reached_threshold = status

    @property
    def distance_to_destination(self) -> bool:
        return self._distance_to_destination

    @distance_to_destination.setter
    def distance_to_destination(self, value: bool) -> None:
        self._distance_to_destination = value

    def update_state(self):
        """High level method that orchestrates telemetry update."""
        self.update_destination_reached_state()
        self.update_distance_to_destination()

    def get_heading_directions(self) -> List[schemas.Direction]:
        """Defines heading directions that would move vehicle towards
        the destination.
        """
        diff = self.destination.x - self.location_service.current_location.x
        heading_directions = []
        if diff > self.destination_reached_threshold:
            heading_directions.append(schemas.Direction.RIGHT)
        elif diff < -self.destination_reached_threshold:
            heading_directions.append(schemas.Direction.LEFT)

        diff = self.destination.y - self.location_service.current_location.y
        if diff > self.destination_reached_threshold:
            heading_directions.append(schemas.Direction.UP)
        elif diff < - self.destination_reached_threshold:
            heading_directions.append(schemas.Direction.DOWN)
        return heading_directions

    def update_distance_to_destination(self):
        """Calculates distance to destination and updates corresponding
        property.
        """
        distance = math.sqrt(
            (
                self.location_service.current_location.x
                - self.destination.x
            ) ** 2
            + (
                self.location_service.current_location.y
                - self.destination.y
            ) ** 2
        )
        distance = round(distance, 1)
        self.distance_to_destination = distance

    def update_destination_reached_state(self) -> None:
        """Checks if destination is within threshold and updates
        corresponding property accordingly.
        """
        reached = all([
            abs(self.destination.x
                - self.location_service.current_location.x
                ) <= self.destination_reached_threshold,
            abs(self.destination.y
                - self.location_service.current_location.y
                ) <= self.destination_reached_threshold,
        ])

        self.destination_reached = reached
        logger.debug("Destination reached: %s", str(self.destination_reached))


class BasicAllowedZoneManager(AllowedZoneManager):
    """
    Class responsible for tracking if a vehicle is within allowed zone.

    Maintains boolean `out of zone` indicator property and a list of
    violated borders.
    """
    def __init__(
            self,
            location_service: LocationService
            ):

        self.location_service: LocationService = location_service
        self._out_of_zone: bool = False
        self._zone_borders_breached: List[schemas.Direction] = []

    @property
    def out_of_zone(self):
        return self._out_of_zone

    @out_of_zone.setter
    def out_of_zone(self, status: bool):
        self._out_of_zone = status

    @property
    def zone_borders_breached(self):
        return self._zone_borders_breached

    @zone_borders_breached.setter
    def zone_borders_breached(
            self,
            borders_breached: List[schemas.Direction]
            ):
        self._zone_borders_breached = borders_breached

    def update_state(self):
        """Calculates if any of the borders is breached and updates 
        `out of borders` and violated borders property accordingly.
        """
        self._reset_out_of_zone()

        if self.location_service.current_location.x < 0:
            self.zone_borders_breached.append(schemas.Direction.LEFT)
        elif self.location_service.current_location.x > \
                self.location_service.nav_map.x_size:
            self.zone_borders_breached.append(schemas.Direction.RIGHT)

        if self.location_service.current_location.y < 0:
            self.zone_borders_breached.append(schemas.Direction.DOWN)
        elif self.location_service.current_location.y > \
                self.location_service.nav_map.y_size:
            self.zone_borders_breached.append(schemas.Direction.UP)

        if len(self.zone_borders_breached) > 0:
            self.out_of_zone = True

    def _reset_out_of_zone(self):
        """Helper method to reset properties"""
        self.out_of_zone = False
        self.zone_borders_breached = []
