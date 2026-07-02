import sys

from loguru import logger

from app.config.settings import settings

logger.remove()

logger.add(
    sys.stdout,
    level=settings.log_level,
    colorize=True,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
           "<level>{level}</level> | "
           "<cyan>{name}</cyan>:<cyan>{function}</cyan> | "
           "{message}",
)

logger.add(
    "logs/app.log",
    rotation="10 MB",
    retention="10 days",
    level=settings.log_level,
)

__all__ = ["logger"]