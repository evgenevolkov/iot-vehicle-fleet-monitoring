"""Contains implementation of the BasicTaskManager class"""
import random
from random import randrange
from typing import Union
from decouple import config
from app.utils import schemas
from app.core.interfaces import TasksManager
from app.utils.logger import get_logger


logger = get_logger(__name__)

NAVIGATION_MAP_X_SIZE = config('NAVIGATION_MAP_X_SIZE')
NAVIGATION_MAP_Y_SIZE = config('NAVIGATION_MAP_Y_SIZE')
RANDOM_SEED = config('RANDOM_SEED', cast=int)

random.seed(RANDOM_SEED)


class BasicTasksManager(TasksManager):
    """Responsible for getting tasks.

    Simulates retrieval from external source.
    """

    def __init__(self, fail_get_task_probability: float = 0.95) -> None:
        self.task_state: schemas.TaskState = schemas.TaskState.IDLE
        self.current_task: Union[schemas.Location, None] = None
        # to simulate no pendding tasks received
        self.fail_get_task_probability: float = fail_get_task_probability

    @property
    def task_state(self) -> schemas.TaskState:
        return self._task_state

    @task_state.setter
    def task_state(self, state: schemas.TaskState):
        self._task_state = state

    def get_new_task(self) -> Union[schemas.MapSize, None]:
        """Mimic recieving a task from outer source"""

        task_nav_map = schemas.MapSize(
            x_size=NAVIGATION_MAP_X_SIZE,
            y_size=NAVIGATION_MAP_Y_SIZE
        )
        if self._fail_to_get_task():
            logger.warning("Failed to get a new task")
            return None
        new_task = self._generate_random_location(task_nav_map)
        return new_task

    def initialize_new_task(self, task: schemas.Location):
        """High level method that processes a new task"""
        self.current_task = task
        self.task_state = schemas.TaskState.IN_PROGRESS

    def destination_reached(self):
        """High level method to perform steps on reaching destination"""
        self.task_state = schemas.TaskState.IDLE

    def _generate_random_location(self, task_nav_map) -> schemas.Location:
        """Simulates receiving a new task"""
        x = randrange(start=0, stop=task_nav_map.x_size)
        y = randrange(start=0, stop=task_nav_map.y_size)

        return schemas.Location(x=x, y=y)

    def _fail_to_get_task(self) -> bool:
        """Defines if a task is received based on predefine probability.
        """
        return random.random() < self.fail_get_task_probability
