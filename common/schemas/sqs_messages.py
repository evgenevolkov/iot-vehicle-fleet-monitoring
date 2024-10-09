"""Data validation for Vehicle tracking message"""
from datetime import datetime, timezone
from typing import Literal
from uuid import UUID
from pydantic import (
    BaseModel,
    Field,
    field_validator,
    NonNegativeFloat,
    NonNegativeInt,
)


class Location(BaseModel):
    """Vehicle location schema"""
    x: int = Field(..., ge=-100, le=200, description="Vehicle horizontal"
                   " position on a map. Should be within expected range")
    y: int = Field(..., ge=-100, le=200, description="Vehicle vertical"
                   " position on a map. Should be within expected range")


class VehicleTrackingMessageV1_0_0(BaseModel):
    """Schema of message send by vehicle to SQS queue"""
    schema_version: Literal['1.0.0'] = Field(
        ..., description="Version of the schema")

    vehicle_id: UUID = Field(
        ..., description="Unique identifier of the vehicle")

    task_state: Literal['Idle', 'In progress'] = Field(
        ..., description="Vehicle task execution state")

    vehicle_location: Location = Field(
        ..., description="Current vehicle location")

    destination: Location = Field(
        ..., description="Current vehicle destination")

    vehicle_speed: NonNegativeInt = Field(
        ..., description="Current vehicle speed. Can't be below zero.")

    distance_to_destination: NonNegativeFloat = Field(
        ..., description="Distance to destination")

    heading_direction: Literal['Up', 'Down', 'Left', 'Right'] = Field(
        ..., description="Vehicle heading direction")

    out_of_zone_status: bool = Field(
        ..., description="Boolean indicator of the vehicle location  within "
        "the allowed location zone")

    created_time: datetime = Field(
        ..., description="Timestamp a log message is created, milliseconds, "
        "UTC timezone")

    @field_validator("created_time")
    @classmethod
    def validate_created_time(cls, value):
        """ensure created time is in the past"""
        current_time = datetime.now(timezone.utc)
        if value > current_time:
            current_time_str = current_time.isoformat(timespec="milliseconds")
            raise ValueError("Expected `created_time` value to be in past, "
                             f" got {value}, current time: {current_time_str}")
        return value

    class ConfigDict:
        extra = 'forbid'  # to prevent unexpected data in the message
