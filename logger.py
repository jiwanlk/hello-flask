import logging
from dotenv import load_dotenv
import os
from loguru import logger
import sys

load_dotenv()
IS_PROD = os.getenv("ENVIRO") == "prod"
new_level = logger.level("WORKER", no=10, color="<RED>", icon="👷")

logger.remove()
if IS_PROD:
    logger.add("test.log", retention="1 month", level="INFO")
else:
    logger.add(sys.stderr, format="{time} - {level} - {message}", level="DEBUG")

logging.getLogger("werkzeug").disabled = True
