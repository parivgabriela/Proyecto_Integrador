import os
from flask import Flask
from .config.config import Config
from .routes.tec_ia_rutas import tec_ia_bot  
from .config.logging_config import setup_logging
from .extensions import socketio, clean_upload_folder
from .services.constants_process import UPLOAD_USER_PATH


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    clean_upload_folder(UPLOAD_USER_PATH)
    app.config['UPLOAD_FOLDER'] = UPLOAD_USER_PATH

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Inicializar extensiones
    socketio.init_app(app)

    # Registrar blueprints
    app.register_blueprint(tec_ia_bot)

    # Configurar logging
    setup_logging()

    return app
