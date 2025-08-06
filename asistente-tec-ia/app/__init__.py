import os
import logging
from flask import Flask
from .config.config import Config
from .routes.tec_ia_rutas import tec_ia_bot  
from .config.logging_config import setup_logging
from .extensions import socketio, clean_upload_folder
from .services.constants_process import UPLOAD_USER_PATH

def create_app():
    setup_logging()
    logging.info("Iniciando la aplicación Flask.")

    app = Flask(__name__)
    app.config.from_object(Config)

    clean_upload_folder()

    app.config['UPLOAD_FOLDER'] = UPLOAD_USER_PATH
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    STATIC_PDFS_PATH = os.path.join(app.root_path, 'static', 'pdfs')
    app.config['PERMANENT_PDF_FOLDER'] = STATIC_PDFS_PATH
    os.makedirs(app.config['PERMANENT_PDF_FOLDER'], exist_ok=True)

    # Inicializar extensiones
    socketio.init_app(app)

    # Registrar blueprints
    app.register_blueprint(tec_ia_bot)

    return app
