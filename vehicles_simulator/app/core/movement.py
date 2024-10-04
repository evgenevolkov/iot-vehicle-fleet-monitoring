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


