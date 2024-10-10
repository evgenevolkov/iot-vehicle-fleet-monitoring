"""
Vehicle simulator app entry point.

Instantiates vehicles and runs each in a asynchronous loop.
"""
import asyncio
from asyncio import Semaphore
import random
from decouple import config
from app.core.vehicle import Vehicle
from app.core.vehicle_factory import create_vehicle
from app.utils.logger import get_logger


RANDOM_SEED = config('RANDOM_SEED', cast=int)

logger = get_logger(__name__)
random.seed(RANDOM_SEED)


async def vehicle_execution_loop(
        vehicle: Vehicle,
        rounds: int,
        run_infinitely: bool,
        sleep_min: float,
        sleep_max: float,
        semaphore: Semaphore,
        ):
    """Vehicle execution coroutine"""
    i = rounds
    while run_infinitely or i > 0:
        async with semaphore:
            vehicle.run_execution_step()
            sleep_duration = round(random.uniform(
                sleep_min, sleep_max), 1)
            logger.debug("%s execution step is done, sleep_time: %s",
                         vehicle.vehicle_id, sleep_duration)
            await asyncio.sleep(sleep_duration)
            i -= 1


async def main():
    """
    App entry point.

    Spawns coroutines and executes them asynchronously.
    """
    concurrency_limit = config('CONCURRENCY_LIMIT', cast=int, default=10)
    run_infinitely = config('RUN_INFINITELY', cast=bool)
    rounds = config('ROUNDS', cast=int)
    qty_vehicles = config('QTY_VEHICLES', cast=int)
    sleep_min = config('SLEEP_TIME_MIN_SEC', cast=float)
    sleep_max = config('SLEEP_TIME_MAX_SEC', cast=float)

    semaphore = Semaphore(concurrency_limit)

    # instantiate vehicles:
    vehicles = [create_vehicle() for _ in range(qty_vehicles)]

    async with asyncio.TaskGroup() as tg:
        _ = [
                tg.create_task(vehicle_execution_loop(
                    vehicle=vehicle,
                    rounds=rounds,
                    run_infinitely=run_infinitely,
                    sleep_min=sleep_min,
                    sleep_max=sleep_max,
                    semaphore=semaphore))
                for vehicle in vehicles
            ]


if __name__ == '__main__':
    asyncio.run(main())
