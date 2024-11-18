import logging

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:     %(message)s",
)
logging.basicConfig(filename="logs/error.log", level=logging.ERROR)
