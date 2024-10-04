import random
from decouple import config
from app.core.interfaces import (
    MovementManager
    )
from app.utils import (
    schemas,
    )
from app.utils.logger import get_logger

logger = get_logger(__name__)

MAX_SPEED = int(config('MAX_SPEED'))


class BasicMovementManager(MovementManager):

    def __init__(
            self,
            current_direction: schemas.Direction = schemas.Direction.UP,
            max_speed: int = MAX_SPEED,
            current_speed: int = 0,
            distance_until_turn_allowed: int = 0,
            can_turn: bool = True,
            ):

        self.max_speed: int = max_speed
        self.current_speed: int = current_speed
        self.current_direction: schemas.Direction = current_direction
        self.can_turn: bool = can_turn
        self.distance_until_turn_allowed: int = distance_until_turn_allowed
        self.shift: schemas.Shift

    def increase_speed(self):
        self.current_speed = min(self.current_speed + 1, self.max_speed)
        logger.debug(f" Increased speed to {self.current_speed}")

    def decrease_speed(self):
        self.current_speed = max(self.current_speed - 1, 1)
        logger.debug(f"Decreased speed to {self.current_speed}")

    def turn(self, direction: schemas.Direction):
        if self.can_turn:
            self.current_direction = direction
            self.distance_until_turn_allowed = \
                self._define_distance_until_turn()
            logger.debug("Turned: %s", direction.value)
            logger.debug("Distance until turn allowed %s",
                         self.distance_until_turn_allowed)
        elif self.distance_until_turn_allowed > 2:
            logger.warning("Can't make turn because turn is not allowed here")
            logger.debug("Distance until turn allowed %s",
                         self.distance_until_turn_allowed)
            return
        elif self.current_speed > 2:
            logger.warning("Can't make turn, because speed too high: %i"
                           " will decrease speed instead", self.current_speed)
            self.decrease_speed()

    def move(self) -> schemas.Shift:
        self._decide_speed_change()
        self.shift = self._get_move_shift()
        self.distance_until_turn_allowed -= 1
        self._check_can_turn()
        return self.shift

    def _decide_speed_change(self):
        logger.debug(f'Curr_speed: {self.current_speed}')
        if self.distance_until_turn_allowed > self.current_speed:
            self.increase_speed()
        else:
            self.decrease_speed()

    def _get_move_shift(self):
        single_shift = schemas.Movement[self.current_direction.name].value
        move_shift = schemas.Shift(
            x=single_shift[0] * self.current_speed,
            y=single_shift[1] * self.current_speed)
        return move_shift

    def _check_can_turn(self):
        self.can_turn = all([
            self.current_speed <= 1,
            self.distance_until_turn_allowed == 0])

    def _define_distance_until_turn(self):
        return int(random.randint(1, 49) ** 0.5) + 2
