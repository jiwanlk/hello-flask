import logging
from dotenv import load_dotenv
import os
from loguru import logger
import sys

load_dotenv()
IS_PROD = os.getenv("ENVIRO") == "prod"

logger.remove()
if IS_PROD:
    logger.add("record.log", retention="1 month", level="INFO")
else:
    logger.add(sys.stderr, format="{time} - {level} - {message}", level="DEBUG")

logging.getLogger("werkzeug").disabled = True
