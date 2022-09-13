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
    # For saving logger to out.log in server
    logger.add("./logs/out.log", backtrace=True, diagnose=True)
else:
    logger.add(
        sys.stdout,
        colorize=True,
        format="<green>{time} {level} {message}</green>",
        backtrace=True,
        diagnose=True,
        enqueue=True,
    )

logging.getLogger("werkzeug").disabled = True
