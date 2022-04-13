import logging
import logging.config

logging.config.fileConfig(
    fname='extensions/logger.cfg',
)

logger = logging.getLogger(__name__)
