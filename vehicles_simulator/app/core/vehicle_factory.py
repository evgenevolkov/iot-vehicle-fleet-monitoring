from app.core.location import NavigationMap, BasicLocationService
from app.core.movement import BasicMovementManager
from app.core.navigation import (
    BasicDestinationTracker,
    BasicAllowedZoneManager,
    HeadingDirectionManager,
    BasicNavigationManager,
    )
from app.core.task import BasicTasksManager
from app.core.tracker import BasicTrackerManager
from app.core.vehicle import Vehicle
from app.utils import schemas
from app.core.send import SQSMessageSender
from decouple import config

TRACKING_SQS_URL = config('TRACKING_SQS_URL')


class BasicVehicleFactory:
    def __init__(
        self,
        map_singleton: NavigationMap,
        default_max_speed=5,
        default_task_fail_prob=0.0
    ):
        self.map_singleton = map_singleton
        self.default_max_speed = default_max_speed
        self.default_task_fail_prob = default_task_fail_prob

    def create_vehicle(
            self,
            max_speed=None,
            initial_location=None,
            task_fail_prob=None
            ):
        """Fectory method to instantiate a vehicle"""

        # Set defaults if not provided
        param_initial_location = initial_location if initial_location \
                                 else schemas.Location(x=1, y=1)
        param_max_speed = max_speed if max_speed else self.default_max_speed
        param_task_fail_prob = task_fail_prob if task_fail_prob \
                                              else self.default_task_fail_prob

        # tasks
        tasks_manager = BasicTasksManager(
            fail_get_task_probability=param_task_fail_prob
        )

        # navigation
        nav_map = self.map_singleton
        initial_location = schemas.Location(x=1, y=1)
        location_service = BasicLocationService(
            nav_map=nav_map,
            current_location=param_initial_location)

        destination_tracker = BasicDestinationTracker(
            location_service=location_service,
        )
        allowed_zone_manager = BasicAllowedZoneManager(
            location_service=location_service
        )

        heading_selector = HeadingDirectionManager()
        heading_selector.register_heading_provider(
            provider=destination_tracker,
            provider_name="Destination",
            provider_weight=10
        )
        movement_manager = BasicMovementManager(
            max_speed=param_max_speed
        )

        navigation_manager = BasicNavigationManager(
            allowed_zone_manager=allowed_zone_manager,
            destination_tracker=destination_tracker,
            heading_selector=heading_selector,
            location_service=location_service,
            movement_manager=movement_manager,
        )

        # tracker
        statuses_probabilities = {
            schemas.TrackerStatus.ONLINE: .8,
            schemas.TrackerStatus.OFFLINE: .2,
        }
        sqs_url = TRACKING_SQS_URL
        message_sender = SQSMessageSender(endpoint_url=sqs_url)
        tracker_manager = BasicTrackerManager(
            statuses_probs=statuses_probabilities,
            tasks_manager=tasks_manager,
            navigation_manager=navigation_manager,
            message_sender=message_sender
        )

        created_vehicle = Vehicle(
            tracker_manager=tracker_manager,
            tasks_manager=tasks_manager,
            navigation_manager=navigation_manager,
            )

        return created_vehicle


singleton_map = NavigationMap(map_size=schemas.MapSize(x_size=100, y_size=100))
vehicle_factory = BasicVehicleFactory(map_singleton=singleton_map)


def create_vehicle(
        max_speed=None,
        initial_location=schemas.Location(x=1, y=1),
        task_fail_prob=None
        ):
    """Exposed method to create vehicles"""
    return vehicle_factory.create_vehicle(
        max_speed=max_speed,
        initial_location=initial_location,
        task_fail_prob=task_fail_prob
    )
