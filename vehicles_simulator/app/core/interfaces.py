"""
This file contains all interfaces, implemented as abstract classes, used
within the Vehicle class.
"""
from typing import List
from abc import ABC, abstractmethod
from app.utils import schemas


# --- Vehicle class dependencies interfaces ---


class NavigationManager(ABC):
    @abstractmethod
    def initialize_new_task(self, destination: schemas.Location) -> None:
        pass

    @abstractmethod
    def move_to_destination(self):
        pass

    @property
    @abstractmethod
    def destination_reached(self):
        pass


class TasksManager(ABC):
    @property
    @abstractmethod
    def task_state(self) -> schemas.TaskState:
        pass

    @abstractmethod
    def get_new_task(self) -> schemas.Location:
        pass

    @abstractmethod
    def initialize_new_task(self, task: schemas.Location) -> None:
        pass

    @abstractmethod
    def destination_reached(self) -> None:
        pass


class TrackerManager(ABC):
    @abstractmethod
    def get_current_status(self) -> schemas.TrackerStatus:
        pass

    @abstractmethod
    def update(self) -> None:
        pass


# --- Navigation class interfaces ---


class AllowedZoneManager(ABC):

    @property
    @abstractmethod
    def out_of_zone(self):
        pass

    @property
    @abstractmethod
    def zone_borders_breached(self):
        pass

    @abstractmethod
    def update_state(self):
        pass


class DestinationTracker(ABC):

    @property
    @abstractmethod
    def destination(self) -> schemas.Location:
        pass

    @abstractmethod
    def get_heading_directions(self) -> List[schemas.Direction]:
        pass

    @property
    @abstractmethod
    def destination_reached(self) -> None:
        pass

    @property
    @abstractmethod
    def distance_to_destination(self) -> None:
        pass

    @abstractmethod
    def update_state(self) -> None:
        """Make tracker update its state according to current locatoin"""


class HeadingDirectionsInterface(ABC):

    @property
    @abstractmethod
    def heading_directions(self) -> List[schemas.Direction]:
        pass

    @abstractmethod
    def update_heading_directions(self):
        pass


class LocationService(ABC):

    @property
    @abstractmethod
    def nav_map(self):
        pass

    @property
    @abstractmethod
    def current_location(self):
        pass

    @abstractmethod
    def update_location(self, shift: schemas.Shift):
        pass


class MovementManager(ABC):
    @abstractmethod
    def increase_speed(self):
        pass

    @abstractmethod
    def decrease_speed(self):
        pass

    @abstractmethod
    def turn(self, direction: schemas.Direction):
        pass

    @abstractmethod
    def move(self):
        pass
