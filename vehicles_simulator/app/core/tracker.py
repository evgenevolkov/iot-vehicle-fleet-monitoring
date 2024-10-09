"""Contains implementation of BasicTrackerManager class."""
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
            message_sender: MessageSender,
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
        self.message_sender = message_sender

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

    def get_current_status(self) -> schemas.TrackerStatus:
        """Exposed methed to get current connection status"""
        return self.current_status

    def update(self) -> None:
        """Generates a new status value based on dict of status and
        probabilies of a value to be set."""
        self.current_status = self._generate_status()
