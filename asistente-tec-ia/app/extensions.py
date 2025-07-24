import os
import shutil
import logging
from flask_socketio import SocketIO
from .services.constants_process import UPLOAD_USER_PATH

socketio = SocketIO()

def clean_upload_folder():
    if os.path.exists(UPLOAD_USER_PATH):
        logging.info(f"Limpiando la carpeta de uploads: {UPLOAD_USER_PATH}")
        for filename in os.listdir(UPLOAD_USER_PATH):
            file_path = os.path.join(UPLOAD_USER_PATH, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path) # Elimina archivos y enlaces simbólicos
                    logging.info(f"Eliminando archivo: {file_path}")
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path) # Elimina subdirectorios
            except Exception as e:
                logging.error(f'Error al eliminar {file_path}: {e}')
