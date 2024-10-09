# Core

This folder contains implementation of the `Vehicle` and its dependencies.

## Implementation overview:

__`Vehicle`__ class is a primary orchestrator class. It defines vehicle behaviour relying on dependency classes states and by cordination them. 
It relies on 3 dependancies:

- __`TasksManager`__ - responsible for receiving a task from external source (emulated) and attempting to receive a new task once current is done.

- __`NavigationManager`__ - responsible for driving a vehicle to the destination.

- __`TrackerManager`__ - responsible for tracking telemetry data from other classes and sending it to an endpoint. 

Some of these classes have own dependencies:

__`NavigationManager`__ - 
    - __`LocationService`__ - tracks vehicle location.
    - __`MovementManager`__ - responsible for vehicle movement. Handles vehicle speed and turn control.
    - __`AllowedZoneManager`__ - tracks if vehicle is located within the allowed zone. Defines heading direction to allowed zone is out.
    - __`HeadingDirectionManager`__ - defines vehicle heading direction. 

__`TrackerManager`__
   - __`SQSMessageSender`__ - sends telemetry data to endpoint.

#### Dependencies Structure

_Cross dependencies are not shown for clarity_

Vehicle_factory 
├─ Vehicle 
│  ├─ TasksManager 
│  ├─ NavigationManager 
│  │ ├─ LocationService 
│  │ │  ├─ NavigationMap
│  │ ├─ MovementManager 
│  │ ├─ HeadingDirectionManager 
│  │ ├─ AllowedZoneManager 
│  ├─ TrackerManager 
│  │  ├─ MessageSender

# Folder contents

## Interfaces

__`interfaces.py`__ - contains all interfaces, implemented as abstract classes, used within 
    Vehicle class and its dependencies.

## High level modules

__`vehicle.py`__ - implements `Vehicle` class. It is the topmost class that orchestrates vehicle behaviour.

__`vehicle_factory.py`__ - implements factory that instantiates a vehicle. It instantiates all required dependancies. 
    Exposes the `create_vehicle` method that is convenient to instantiate a `Vehicle` instance.

## Files that define concrete implementations of the Vehicle class dependencies and their dependencies

- __`heading.py`__ - contains `BasicHeadingDirectionManager` class that is a concrete implementation of the `HeadingDirectionManager` class. Responsible for defining a vehicle heading. It is a dependency of `BasicNavigationManager` class.

- __`location.py`__ - contains `BasicLocationService` class, that is a concrete implementation of the `LocationService` class. Also contains its dependency `NavigationMap` class.

- __`movement.py`__ - contains `BasicMovementManager` class that is a concrete implementation of the `MovementManager` class. Responsible for movement of the vehilce.

- __`navigation.py`__ - contains `BasicNavigationManager` class that is a concrete implementation of the `NavigationManager` class. Also contains its dependencies `BasicDestinationTracker`, `BasicAllowedZoneManager` classes.

- __`send.py`__ - contains implementation of the `SQSMessageSender` class. It is a dependency of the `BasicTrackerManager` class.

- __`tracker.py`__ - contains implementation of the `BasicTrackerManager` class that is a concrete implementation of the `TrackerManager` class.
