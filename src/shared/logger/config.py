import logging
import sys
from pathlib import Path

# Determine log level from environment
LOG_LEVEL = "INFO"

# Create logs directory if it doesn't exist
LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

# Configure logging format
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Create logger
logger = logging.getLogger("ajla")
logger.setLevel(getattr(logging, LOG_LEVEL))

# Console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(getattr(logging, LOG_LEVEL))
console_formatter = logging.Formatter(LOG_FORMAT)
console_handler.setFormatter(console_formatter)

# File handler
file_handler = logging.FileHandler(LOG_DIR / "ajla.log")
file_handler.setLevel(getattr(logging, LOG_LEVEL))
file_formatter = logging.Formatter(LOG_FORMAT)
file_handler.setFormatter(file_formatter)

# Add handlers to logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for a specific module."""
    return logging.getLogger(f"ajla.{name}")
