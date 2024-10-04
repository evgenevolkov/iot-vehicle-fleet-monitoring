# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=import-error
import random
from decouple import config
from app.core.interfaces import (
    TrackerManager,
    TasksManager,
    NavigationManager,
    )
from app.utils import (
    schemas,
    )
from app.utils.logger import get_logger


RANDOM_SEED = int(config('RANDOM_SEED'))
random.seed(RANDOM_SEED)
logger = get_logger(__name__)


class Vehicle:

    def __init__(
            self,
            navigation_manager: NavigationManager,
            tasks_manager: TasksManager,
            tracker_manager: TrackerManager,
            ):

        self.navigation_manager = navigation_manager
        self.tasks_manager = tasks_manager
        self.tracker_manager = tracker_manager

    def get_current_location(self):
        return self.navigation_manager.current_location

    def get_current_tracker_status(self):
        return self.tracker_manager.get_current_status()

    def get_current_task_status(self):
        return self.tasks_manager.task_state

    def run_execution_step(self):
        """main execution logic"""

        self.tracker_manager.update()

        # if task_state is idle, try to get a new task
        if self.tasks_manager.task_state == schemas.TaskState.IDLE:
            logger.debug("In %s mode. Trying to get new task",
                         schemas.TaskState.IDLE.value)
            new_task = self.tasks_manager.get_new_task()
            if new_task is None:
                logger.debug("Failed to get new task")
            else:
                logger.debug("Succesfully received a new task %s", new_task)
                self.tasks_manager.initialize_new_task(new_task)
                self.navigation_manager.initialize_new_task(
                    destination=new_task)
                logger.debug("Succesfully set a new task: %s",
                             self.navigation_manager.destination)
            return

        # if task in progress then make move
        if self.tasks_manager.task_state == schemas.TaskState.IN_PROGRESS:
            logger.debug("Initializing movement")
            self.navigation_manager.move_to_destination()

        if self.navigation_manager.destination_reached:
            self.tasks_manager.destination_reached()

        # if reached destination then make tasks manager to react
        if self.navigation_manager.destination_reached:
            logger.debug("Reached destination")
            self.tasks_manager.destination_reached()

        logger.debug(
            "Current distance: %s",
            self.navigation_manager.distance_to_destination)