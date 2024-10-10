"""Contains implementation of BasicTrackerManager class."""
from datetime import datetime, timezone
from typing import Optional
import random
from uuid import uuid4, UUID
from app.core.interfaces import (
    TrackerManager,
    TasksManager,
    NavigationManager,
    MessageSender,
    )
from app.utils import schemas
from common.schemas.sqs_messages import VehicleTrackingMessageV1_0_0


class BasicTrackerManager(TrackerManager):
    """Class responcible for centralized tracking of all vehicle
    telemetry.

    Queries all vehicle dependencies to retrieve velues.
    Kepps track of telemetry values.
    Simulates connection loss.
    Sends telemetry to endpoint.
    """
    def __init__(
            self,
            statuses_probs: dict[schemas.TrackerStatus: float],
            tasks_manager: TasksManager,
            navigation_manager: NavigationManager,
            # message_sender: MessageSender,
            vehicle_id: Optional[UUID] = None,
            current_status: schemas.TrackerStatus =
                schemas.TrackerStatus.ONLINE,
            ) -> None:
        self.statuses_probs = statuses_probs
        self.current_status = current_status
        self.vehicle_id = vehicle_id or uuid4()  # assign if not passed

        self.statuses_values = list(statuses_probs.keys())
        self.statuses_weights = statuses_probs.values()
        self.tracking_data = None  # placeholder

        # dependencies
        self.tasks_manager = tasks_manager
        self.navigation_manager = navigation_manager
        # self.message_sender = message_sender

    @property
    def tracking_data(self):
        return self._tracking_data

    @tracking_data.setter
    def tracking_data(self, value):
        self._tracking_data = value

    def _generate_status(self) -> schemas.TrackerStatus:
        """Simulate ocassional loss of connection with tracker"""
        generated_status = random.choices(
            population=self.statuses_values,
            weights=self.statuses_weights,
            k=1
        )

        return generated_status

    def get_current_tracker_status(self) -> schemas.TrackerStatus:
        """Exposed methed to get current connection status"""
        return self.current_status

    def update(self) -> None:
        """Generates a new status value based on dict of status and
        probabilies of a value to be set."""
        self.current_status = self._generate_status()
        self.collect_tracking_data()

    def collect_tracking_data(self) -> None:
        """Main function to collect all traking metrics"""
        self.tracking_data = schemas.TrackingData(
            task_state=self._get_task_state(),
            vehicle_location=self._get_vehicle_location(),
            destination=self._get_destination(),
            vehicle_speed=self._get_vehicle_speed(),
            heading_direction=self._get_heading_direction(),
            distance_to_destination=self._get_distance_to_destination(),
            out_of_zone_status=self._get_out_of_zone_status(),
            created_time=self._get_current_time(),
        )

    def _get_task_state(self) -> str:
        """Helper method to get task manager state"""
        return self.tasks_manager.task_state.value

    def _get_vehicle_location(self) -> schemas.Location:
        """Helper method to get vehicle current location"""
        return self.navigation_manager.current_location

    def _get_destination(self) -> schemas.Location:
        """Helper method to get current destination"""
        return self.navigation_manager.destination

    def _get_vehicle_speed(self) -> int:
        """Helper method to get current speed"""
        return self.navigation_manager.current_speed

    def _get_heading_direction(self) -> schemas.Direction:
        """Helper method to get current heading direction"""
        return self.navigation_manager.heading_direction

    def _get_distance_to_destination(self) -> float:
        """Helper method to get distance to destination"""
        return self.navigation_manager.distance_to_destination

    def _get_out_of_zone_status(self) -> bool:
        """Helper method to get out of zone status"""
        return self.navigation_manager.out_of_zone_status

    def _get_current_time(self) -> datetime:
        """Helper method to get current time"""
        return datetime.now(timezone.utc).isoformat(timespec="milliseconds")

    def send_tracking_data(self) -> None:
        """High level method that orchestrate sending telemetry to the
        endpoint.
        """
        tracking_message = self._generate_tracking_message()
        self._send_message(message=tracking_message)

    def _generate_tracking_message(self) -> None:
        """Helper method to prepare message to be sent to the endpoint.
        Validates message to match schema."""
        self.collect_tracking_data()
        message_data = VehicleTrackingMessageV1_0_0(
            **self.tracking_data.model_dump(),
            schema_version="1.0.0",
            vehicle_id=self.vehicle_id
        )

        message_json = message_data.model_dump_json()
        return message_json

    def _send_message(self, message):
        """Helpor method that performs method sending"""
        # self.message_sender.send_message(message=message)
        pass
