"""Contains implementation of BasicMovementManager"""
import random
from decouple import config
from app.core.interfaces import MovementManager
from app.utils import schemas
from app.utils.logger import get_logger

logger = get_logger(__name__)

MAX_SPEED = config('MAX_SPEED', cast=int)
TURN_DISTANCE_BASE = config('TURN_DISTANCE_BASE', cast=int)
TURN_DISTANCE_OFFSET = config('TURN_DISTANCE_OFFSET', cast=int)
TURN_SPEED_THRESHOLD = config('TURN_SPEED_THRESHOLD', cast=int)
SPEED_CHANGE_STEP = config('SPEED_CHANGE_STEP', cast=int)
RANDOM_SEED = config('RANDOM_SEED', cast=int)

random.seed(RANDOM_SEED)


class BasicMovementManager(MovementManager):
    """
    Class responsible for:
     - performing vehicle movement
     - tracking related telemetry

    Key logic:

    - Turning:
        Class responds on external turn attempts. If a turn is allowed,
        it changes the vehicle's heading direction. Otherwise it logs a
        warning and keeps the heading direction maintained.

        A turn is allowed if both following conditions are met:
        1. Speed equals or less than a defined threshold.
        2. Distance until next turn is equal to 0.
        This intends to make simulation closer to real world conditions.

    - Speed change:
        A vehicle can change its speed only gradually, by a defined
        change stap per each movement call. The logic whether increase
        or decrease the speed is implemented in the 
        `_decide_speed_change` method.
    """
    def __init__(
            self,
            current_direction: schemas.Direction = schemas.Direction.UP,
            max_speed: int = MAX_SPEED,
            current_speed: int = 0,
            distance_until_turn_allowed: int = 0,
            can_turn: bool = True,
            ) -> None:

        self.max_speed: int = max_speed
        self.current_speed: int = current_speed
        self.current_direction: schemas.Direction = current_direction
        self.can_turn: bool = can_turn
        self.distance_until_turn_allowed: int = distance_until_turn_allowed
        self.shift: schemas.Shift

    def increase_speed(self) -> None:
        """Increases vehicle speed by 1 if within max_speed limit"""
        self.current_speed = min(self.current_speed + SPEED_CHANGE_STEP,
                                 self.max_speed)
        logger.debug(f" Increased speed to {self.current_speed}")

    def decrease_speed(self) -> None:
        """Decreases vehicle speed by 1 until 1"""
        self.current_speed = max(self.current_speed - SPEED_CHANGE_STEP, 1)
        logger.debug(f"Decreased speed to {self.current_speed}")

    def turn(self, direction: schemas.Direction) -> None:
        """Try to make a turn or report why can't otherwise"""
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
        elif self.current_speed > TURN_SPEED_THRESHOLD:
            logger.warning("Can't make turn, because speed too high: %i"
                           " will decrease speed instead", self.current_speed)
            self.decrease_speed()

    def move(self) -> schemas.Shift:
        """
        High level method that implements vehicle movement forward
        logic.

        Result of move is calculating a shift value, that is a change of
        the vehicle location on the map.

        Steps:
        1. Decide if speed should be changed.
        2. Calculate vehicle shift.
        3. Decrease value of the distance until next turn is allowed.
        4. Update turn possibility.
        """
        self._decide_speed_change()
        self.shift = self._get_move_shift()
        self.distance_until_turn_allowed -= 1
        self._check_can_turn()
        return self.shift

    def _decide_speed_change(self) -> None:
        """
        Implements logic of speed change decision.

        If distance value until next turn possibility is greater than
        current speed, then increase speed. Decrease otherwise.
        """
        logger.debug(f'Curr_speed: {self.current_speed}')
        if self.distance_until_turn_allowed > self.current_speed:
            self.increase_speed()
        else:
            self.decrease_speed()

    def _get_move_shift(self) -> schemas.Shift:
        """Calculate the move shift based on current speed."""
        single_shift = schemas.Movement[self.current_direction.name].value
        move_shift = schemas.Shift(
            x=single_shift[0] * self.current_speed,
            y=single_shift[1] * self.current_speed)
        return move_shift

    def _check_can_turn(self) -> None:

        """
        Check if a turn is allowed.

        Both conditions a required be met:
        1. Speed equals or less than threshold
        2. Distance until turn allowed is 0
        """
        self.can_turn = all([
            self.current_speed <= TURN_SPEED_THRESHOLD,
            self.distance_until_turn_allowed == 0])

    def _define_distance_until_turn(self) -> int:
        """Simulate retrieveing distance until next turn.

        Currently, for sample purpose, simulation formula is applied.
        """
        return int(random.randint(1, TURN_DISTANCE_BASE) ** 0.5) \
            + TURN_DISTANCE_OFFSET
