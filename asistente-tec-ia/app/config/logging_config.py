import os
import logging
from logging.handlers import RotatingFileHandler

def setup_logging():
    LOG_DIRECTORY = "logs/app.log"
    
    log_path = LOG_DIRECTORY
    log_dir = os.path.dirname(log_path)

    # Crear directorio si no existe
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

        # Crear archivo vacío si no existe
    if not os.path.exists(log_path):
        open(log_path, 'a').close()
    
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    
    handler = RotatingFileHandler(LOG_DIRECTORY, maxBytes=100000, backupCount=3)
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

    logging.getLogger().addHandler(handler)
