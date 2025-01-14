"""Pedantic data schemas used within the application"""
from enum import Enum
from datetime import datetime
from typing import Literal
from pydantic import (
    BaseModel,
    NonNegativeInt,
    NonNegativeFloat,
    PositiveInt
    )


class Direction(Enum):
    LEFT = 'Left'
    RIGHT = 'Right'
    UP = 'Up'
    DOWN = 'Down'


class Movement(Enum):
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    UP = (0, 1)
    DOWN = (0, -1)


class Shift(BaseModel):
    x: int
    y: int


class TaskState(Enum):
    IDLE = 'Idle'
    IN_PROGRESS = 'In progress'


class TrackerStatus(Enum):
    OFFLINE = "offline"
    ONLINE = "online"


class MapSize(BaseModel):
    x_size: PositiveInt
    y_size: PositiveInt


class Location(BaseModel):
    x: int
    y: int


class Vehicle(BaseModel):
    location: Location
    speed: NonNegativeInt
    tracker_status: Literal[TrackerStatus.ONLINE, TrackerStatus.OFFLINE]


class TrackingData(BaseModel):
    """Schema for metricks that are stored by Tracking module"""
    task_state: Literal['Idle', 'In progress']
    destination: Location
    vehicle_location: Location
    vehicle_speed: NonNegativeInt
    heading_direction: Literal['Up', 'Down', 'Left', 'Right']
    distance_to_destination: NonNegativeFloat
    out_of_zone_status: bool
    created_time: datetime
