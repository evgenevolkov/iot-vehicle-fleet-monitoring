import random
from app.core.interfaces import TrackerManager
from app.utils import schemas


class BasicTrackerManager(TrackerManager):

    def __init__(
            self,
            statuses_probs: dict[schemas.TrackerStatus: float],
            current_status: schemas.TrackerStatus =
                schemas.TrackerStatus.ONLINE,
            ):
        self.statuses_probs = statuses_probs
        self.current_status = current_status

        self.statuses_values = list(statuses_probs.keys())
        self.statuses_weights = statuses_probs.values()

    def _generate_status(self) -> schemas.TrackerStatus:
        """Mimic ocassional loss of connection with tracker"""

        generated_status = random.choices(
            population=self.statuses_values,
            weights=self.statuses_weights,
            k=1
        )

        return generated_status

    def get_current_status(self) -> schemas.TrackerStatus:
        return self.current_status

    def update(self) -> None:
        """Generates a new status value based on dict of status and
        probabilies of a value to be set."""
        self.current_status = self._generate_status()
