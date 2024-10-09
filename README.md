# This is a vehicles-monitoring simulation project

The project simulates a fleet of autonomous vehicles with tracker that regurlary sends telemetry to an endpoint.

## Project consists of the following components

_Project in progress_

__Vehicles simulator__ application. (`vehicles_simulator` folder)

    This simulates fleet of vehicles. To do it a number of vehilces is instantinated and each runs in infinite loop of getting a task with destination, reaching destination, reporting and getting a new one. 
    Besides that, each vehicle regulary sends telemetry to an endpoint

__Telemetry monitoring__ _in progress_

    Collecting telemetry is implemented leveraging AWS. 
    Specifically, an SQS is set up as an endpoint for receiving telemetry. This allows:
    - asyncroneously collect data
    - decouple sender from reciever 
    - guarantee that each message is collected and stored

## Highlights:

_TBD_

# Stack

Language: __Python__
Data validation: __Pydantic__
Infrastructure-as-Code: __Terraform__, __terraformlocal__, __localstack__
Infrastructure: 
    Message brocker: __AWS SQS__
    NoSQL database: __AWS DynamoDB__
Testing, linting: __Pytest__, __MyPy__, __pylint__, __flake8__

## Prerequisites:

To run this project, you should have these tools installed:
__Git, Python, PIP, Make, Docker__
It is assumed that you run on __MacOS__. Otherwise you might need adjust accordingly. 

## Install

_(Please check the prerequisites first;)_

To install the app, you need to install dependencies and manually activate the virtual environment. These are the steps: 

__1.__ Clone a repo in a new folder:

```sh
git clone [put repo address here]
```

__2.__ Open terminal in the project root folder and execute:
```sh 
make install
```

__3.__ Activate the virtual environment by execution: 
```sh
source .venv/bin/activate
```

Now you are good to go.👍

## How to use

_TBD_

# Enjoy;)