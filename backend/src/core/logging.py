import logging
from .config import settings

# Set up basic logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Get logger for the application
logger = logging.getLogger(settings.APP_NAME)