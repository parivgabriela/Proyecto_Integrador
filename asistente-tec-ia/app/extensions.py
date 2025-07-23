import os
import shutil
from flask_socketio import SocketIO

socketio = SocketIO()

def clean_upload_folder(UPLOAD_FOLDER):
    if os.path.exists(UPLOAD_FOLDER):
        print(f"Limpiando la carpeta de uploads: {UPLOAD_FOLDER}")
        for filename in os.listdir(UPLOAD_FOLDER):
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path) # Elimina archivos y enlaces simbólicos
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path) # Elimina subdirectorios
            except Exception as e:
                print(f'Error al eliminar {file_path}: {e}')
    else:
        print(f"La carpeta de uploads no existe: {UPLOAD_FOLDER}. Creándola...")
        os.makedirs(UPLOAD_FOLDER)

