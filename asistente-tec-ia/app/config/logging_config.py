import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from .logging_handler import NoSocketIOFilter

def setup_logging():
    LOG_FILE_PATH = "logs/app.log"
    log_dir = os.path.dirname(LOG_FILE_PATH)

    # Crear directorio si no existe
    os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Limpiar cualquier handler existente para evitar duplicados o conflictos
    if logger.hasHandlers():
        logger.handlers.clear()

    no_socketio_filter = NoSocketIOFilter()
    
    file_handler = RotatingFileHandler(
        LOG_FILE_PATH, 
        maxBytes=100000, 
        backupCount=3,
        encoding='utf-8'
    )

    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    file_handler.addFilter(no_socketio_filter)

    # Crear el handler para mostrar en la consola (StreamHandler)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s: %(message)s"))
    #console_handler.addFilter(no_socketio_filter)


    # Añadir ambos handlers al logger raíz
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logging.info("El sistema de logging ha sido configurado.")
