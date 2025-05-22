import logging
from logging.handlers import RotatingFileHandler

def setup_logging():
    LOG_DIRECTORY = "logs/app.log"
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    
    handler = RotatingFileHandler(LOG_DIRECTORY, maxBytes=100000, backupCount=3)
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

    logging.getLogger().addHandler(handler)
