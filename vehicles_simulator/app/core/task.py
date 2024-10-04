import random
from random import randrange
from typing import Union
import logging
from decouple import config
from app.utils import schemas
from app.core.interfaces import TasksManager

logger = logging.getLogger()

NAVIGATION_MAP_X_SIZE = config('NAVIGATION_MAP_X_SIZE')
NAVIGATION_MAP_Y_SIZE = config('NAVIGATION_MAP_Y_SIZE')


class BasicTasksManager(TasksManager):

    def __init__(self, fail_get_task_probability: float = 0.95):
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
        self.current_task = task
        self.task_state = schemas.TaskState.IN_PROGRESS

    def destination_reached(self):
        self.task_state = schemas.TaskState.IDLE

    def _generate_random_location(self, task_nav_map) -> schemas.Location:

        x = randrange(start=0, stop=task_nav_map.x_size)
        y = randrange(start=0, stop=task_nav_map.y_size)

        return schemas.Location(x=x, y=y)

    def _fail_to_get_task(self) -> bool:
        return random.random() < self.fail_get_task_probability
