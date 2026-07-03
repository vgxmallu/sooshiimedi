import logging
from config import LOG_CHANNEL 

logging.basicConfig(
    level=getattr(logging, LOG_CHANNEL),
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

logger = logging.getLogger("VGX")
