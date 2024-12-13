import logging
import os
from datetime import datetime


log_directory = "logs"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

log_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")


console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(log_format)


error_log_path = os.path.join(log_directory, "error.log")
file_handler = logging.FileHandler(error_log_path)
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(log_format)


logger.addHandler(console_handler)
logger.addHandler(file_handler)
