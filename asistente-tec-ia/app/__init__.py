from flask import Flask
from .config.config import Config
from .routes.tec_ia_rutas import tec_ia_bot  
from .config.logging_config import setup_logging
from .extensions import socketio

UPLOAD_USER_PATH = 'uploads/'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['UPLOAD_FOLDER'] = UPLOAD_USER_PATH

    # Inicializar extensiones
    socketio.init_app(app)

    # Registrar blueprints
    app.register_blueprint(tec_ia_bot)

    # Configurar logging
    setup_logging()

    return app
