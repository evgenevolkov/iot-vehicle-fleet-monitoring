# pylint: disable=import-error
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
import pytest
from app.core.vehicle import Vehicle
from app.core.task import BasicTasksManager
from app.core.tracker import BasicTrackerManager
from app.core.location import NavigationMap, BasicLocationService
from app.core.navigation import (
    BasicDestinationTracker,
    BasicAllowedZoneManager,
    HeadingDirectionManager,
    BasicNavigationManager,
    )
from app.core.movement import BasicMovementManager
from app.utils import (
    schemas,
    )
from app.utils.logger import get_logger

logger = get_logger(__name__)


@pytest.fixture(name="vehicle", scope="function")
def vehicle_fixture():
    """Create an instance of a vehicle"""

    # tasks
    tasks_manager = BasicTasksManager(
        fail_get_task_probability=0.0
    )

    # navigation
    map_size = schemas.MapSize(x_size=100, y_size=100)
    nav_map = NavigationMap(map_size=map_size)
    initial_location = schemas.Location(x=1, y=1)
    location_service = BasicLocationService(
        nav_map=nav_map,
        current_location=initial_location)

    destination_tracker = BasicDestinationTracker(
        location_service=location_service,
    )
    allowed_zone_manager = BasicAllowedZoneManager(
        location_service=location_service
    )

    heading_selector = HeadingDirectionManager()
    movement_manager = BasicMovementManager()

    navigation_manager = BasicNavigationManager(
        allowed_zone_manager=allowed_zone_manager,
        destination_tracker=destination_tracker,
        heading_selector=heading_selector,
        location_service=location_service,
        movement_manager=movement_manager,
    )

    # tracker
    statuses_probabilities = {
        schemas.TrackerStatus.ONLINE: 1.0,
        schemas.TrackerStatus.OFFLINE: 0.0,
    }
    tracker_manager = BasicTrackerManager(
        statuses_probs=statuses_probabilities,
        tasks_manager=tasks_manager,
        navigation_manager=navigation_manager,
    )

    test_vehicle = Vehicle(
        tracker_manager=tracker_manager,
        tasks_manager=tasks_manager,
        navigation_manager=navigation_manager,
        )

    yield test_vehicle


def compare_values(param_name, current, expected):
    assert expected == current, (
        f"Expected {param_name} to be {expected}, got {current}"
    )


@pytest.mark.parametrize(
    "param_name, current_func, expected", [(
        "current_tracker_status",
        lambda vehicle: vehicle.get_current_tracker_status(),
        schemas.TrackerStatus.ONLINE
        ),
        (
        "current_location",
        lambda vehicle: vehicle.get_current_location(),
        schemas.Location(x=1, y=1)
        ),
        (
        "current_task_status",
        lambda vehicle: vehicle.get_current_task_status(),
        schemas.TaskState.IDLE
        ),
    ]
)
def test_can_initialize_a_vehicle(
        param_name, current_func, expected, vehicle):
    """Check if values are set as expacted on istantiation"""
    assert vehicle is not None, (
        "Expected vehicle to be instantiated, got None"
    )

    # compare_values(param_name, current, expected)
    current = current_func(vehicle)
    assert expected == current, (
        f"Expected {param_name} to be {expected}, got {current}"
    )


def test_vehicle_can_move(vehicle):
    """Test vehicle can properly change its position"""

    assert vehicle.get_current_location() is not None, (
        f"Expected to get value, got {vehicle.get_current_location()}"
    )
    assert vehicle.get_current_tracker_status() is not None, (
        f"Expected to get value, got {vehicle.get_current_tracker_status()}"
    )
    assert vehicle.get_current_task_status() is not None, (
        f"Expected to get value, got {vehicle.get_current_task_status()}"
    )

    location_before_move = vehicle.get_current_location()
    vehicle.navigation_manager.destination = schemas.Location(x=100, y=100)
    vehicle.run_execution_step()
    vehicle.run_execution_step()
    location_after_move = vehicle.get_current_location()

    assert location_before_move != location_after_move, (
        "Expected to be in different location after 2 moves")
