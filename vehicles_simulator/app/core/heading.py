"""
Implements the HeadingDirectionManager class.

The HeadingDirectionManager defines next turn direction.
Decision making relies external direction providers, that can be
destination, allowed zone, etc.

Desision for the next turn is done in two steps.
1. Define direction probabilities.
   To calculate provavilities, HeadingDirectionManager starts with equal
   probability for each direction, then sequentially queries heading
   providers and modifies provider suggested directions by the
   provider's weight.

2. Define heading direction.
   The heading direction is selected using a weighted random selector
   based on probabilities from step 1.

A heading direction provider can be registered on runtime.
"""
from typing import Dict, List
import random
from app.core.interfaces import HeadingDirectionsInterface
from app.utils import schemas
from app.utils.logger import get_logger

logger = get_logger(__name__)


class HeadingDirectionManager:
    def __init__(self):
        self.heading_providers: List[Dict[str, object]] = []
        self.heading_direction: schemas.Direction = schemas.Direction.UP

    def register_heading_provider(
            self,
            provider: HeadingDirectionsInterface,
            provider_name: str,
            provider_weight: float
            ) -> None:
        """Register a heading direction provider"""
        self.heading_providers.append({
            'entity': provider,
            'name': provider_name,
            'weight': provider_weight
        })

    def _get_heading_probabilities(self):
        heading_probabilities = {
            schemas.Direction.UP: 10,
            schemas.Direction.DOWN: 10,
            schemas.Direction.LEFT: 10,
            schemas.Direction.RIGHT: 10
        }

        """
        Iterate over providers, modify  heading directions and apply to
        base probabilities modified by provider's weight.
        """
        for provider in self.heading_providers:
            provider['entity'].update_heading_directions()
            provider_headings = provider['entity'].heading_directions
            heading_probabilities = {
                direction: probability * provider['weight']
                if direction in provider_headings else probability
                for direction, probability
                in heading_probabilities.items()
            }

        return heading_probabilities

    def _generate_next_direction(self):
        heading_probabilities = self._get_heading_probabilities()
        logger.debug("heading probabilities: %s", str(heading_probabilities))
        """
        Define heading direction.

        To do it collect each direction probability and use weighted
        random generator to make final decision. 
        """
        heading_direction = random.choices(
            population=[k for k, v in heading_probabilities.items()],
            weights=heading_probabilities.values(),
            k=1)[0]  # unpack from list

        # logger.debug("self.current_location %s", str(self.current_location))
        logger.debug("Direction: %s", heading_direction.value)
        return heading_direction

    def update_heading_direction(self) -> schemas.Direction:
        self.heading_direction = self._generate_next_direction()
        """Update heading direction relying on internal logic"""
