from pathlib import Path

from loguru import logger

from app.core.config import settings

# Create logs directory if it doesn't exist
Path("logs").mkdir(exist_ok=True)

logger.remove()

logger.add(
    "logs/fraudshield.log",
    rotation="10 MB",
    retention="30 days",
    level=settings.log_level,
    enqueue=True,
)

logger.add(
    sink=lambda msg: print(msg, end=""),
    level=settings.log_level,
)

app_logger = logger