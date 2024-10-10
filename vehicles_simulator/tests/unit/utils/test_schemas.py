import pytest
from pydantic import ValidationError
from app.utils.schemas import (
    Direction,
    Movement,
    Shift,
)

@pytest.mark.parametrize(
        "direction", [
            'Up',
            'Down',
            'Left',
            'Right'
        ]
)
def test_direction_created_correctly(direction):
    assert Direction(direction).value == direction


def test_direction_values():
    assert Direction.LEFT.value == 'Left'
    assert Direction.RIGHT.value == 'Right'
    assert Direction.UP.value == 'Up'
    assert Direction.DOWN.value == 'Down'

    assert Direction('Left') == Direction.LEFT
    assert Direction('Right') == Direction.RIGHT
    assert Direction('Up') == Direction.UP
    assert Direction('Down') == Direction.DOWN


@pytest.mark.parametrize(
        "movement", [
            Movement.UP,
            Movement.DOWN,
            Movement.LEFT,
            Movement.RIGHT,
        ]
)
def test_movement_step_1(movement):
    assert abs(movement.value[0]) + abs(movement.value[1]) == 1, (
        f"Expected sum of move shifts to be 1, got "
        f"{abs(movement.value[0]) + abs(movement.value[1])}, "
        f"movement: {movement.name, movement.value}"
    )


@pytest.mark.parametrize(
    "x, y", [
        (1, 1.1),
        (1.1, 1),
        (1.1, 1.1),
        ]
)
def test_shift_negative(x, y):
    with pytest.raises(ValidationError) as exec_info:
        Shift(x=x, y=y)

    expected_error_message = ("Input should be a valid integer, got "
                              "a number with a fractional part")
    assert expected_error_message in str(exec_info.value), (
        f"Expected error message containing {expected_error_message}, "
        f"got: {str(exec_info.value)}")
