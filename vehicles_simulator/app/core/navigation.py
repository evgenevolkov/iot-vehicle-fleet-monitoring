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


class BasicDestinationTracker(DestinationTracker):
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
        self.update_destination_reached_state()
        self.update_distance_to_destination()

    def get_heading_directions(self) -> List[schemas.Direction]:
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
        self.out_of_zone = False
        self.zone_borders_breached = []
